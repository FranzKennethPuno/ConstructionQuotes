# models.py
from django.db import models
from django.contrib.auth.models import User

class ProjectElement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="None")
    def __str__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=100)
    element = models.ForeignKey(ProjectElement, on_delete=models.CASCADE, related_name='materials')
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(default=0,max_length=50)

    def __str__(self):
        return self.name

class ProjectQuotation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area_size = models.DecimalField(max_digits=10, decimal_places=2)
    elements = models.ManyToManyField(ProjectElement, related_name='quotations')
    materials = models.JSONField()  # To store material choices
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Quotation #{self.id} by {self.user.username}"


