from django.db import models
from content.models import User

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

class ProductAttribute(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attributes')

class ProductAttributeValue(models.Model):
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=255)

class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image =  image =models.ImageField(upload_to ='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    managers = models.ManyToManyField(User, related_name='brands')

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    attributes = models.ManyToManyField(ProductAttributeValue, related_name='products')