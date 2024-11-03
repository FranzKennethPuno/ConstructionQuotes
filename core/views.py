# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, "User registered successfully.")
                return redirect('login')  # Redirect to login after registration
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, 'accounts/register.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to homepage after login
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'accounts/login.html')

@login_required
def home(request):
    return render(request, 'accounts/home.html')

def user_logout(request):
    logout(request)
    return redirect('login')


from django import forms
from .models import ProjectElement, Material, ProjectQuotation

class QuotationRequestForm(forms.Form):
    area_size = forms.IntegerField(label="Area Size (sq.m)", required=True)
    element = forms.ModelChoiceField(queryset=ProjectElement.objects.all(), empty_label=None, label="Select Project Element")
    material = forms.ModelChoiceField(queryset=Material.objects.all(), empty_label=None, label="Select Material")

def request_quotation(request):
    if request.method == 'POST':
        form = QuotationRequestForm(request.POST)
        if form.is_valid():
            area_size = form.cleaned_data['area_size']
            selected_element = form.cleaned_data['element']
            selected_material = form.cleaned_data['material']
            return redirect('home')
    else:
        form = QuotationRequestForm()

    return render(request, 'accounts/request_quotation.html', {'form': form})



@login_required
def view_quotations(request):
    quotations = ProjectQuotation.objects.filter(user=request.user)
    return render(request, 'accounts/view_quotations.html', {'quotations': quotations})

# views.py
from django.shortcuts import get_object_or_404

@login_required
def quotation_detail(request, quotation_id):
    quotation = get_object_or_404(ProjectQuotation, id=quotation_id, user=request.user)
    # Here, you'll need to extract materials details from the JSON field if needed.
    return render(request, 'accounts/quotation_detail.html', {'quotation': quotation})


from django.http import JsonResponse
from .models import Material

def get_materials(request, element_id):
    materials = Material.objects.filter(element_id=element_id)
    material_data = [{'id': material.id, 'name': material.name} for material in materials]
    return JsonResponse({'materials': material_data})