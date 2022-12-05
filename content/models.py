from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    created = models.DateTimeField(auto_now_add=True)
    otp = models.IntegerField(null=True)
    full_name = models.CharField(max_length=30,null=True)
    phone1 = models.CharField(max_length=30,null=True)
    phone2 = models.CharField(max_length=30,null=True)
    
class Product(models.Model):
    choices= [
    ('cars', 'cars'),
    ('others', 'others'),
    ]
    created = models.DateTimeField(auto_now_add=True)
    owner= models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    price =  models.IntegerField()
    expire_date = models.DateTimeField()
    identifier = models.UUIDField()
    display = models.ImageField(upload_to ='uploads/')
    category = models.CharField(max_length=50,choices=choices)
       

class Banner(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=1000,null=True)
    owner = models.CharField(max_length=30,null=True)
    display = models.ImageField(upload_to ='uploads/')
    expire_date =  models.DateTimeField(auto_now_add=False)
    splashscreen =  models.BooleanField()
    home =  models.BooleanField()
    universal = models.UUIDField()

class FeacturedAd(models.Model):
    created = models.DateTimeField(auto_now_add=True)    
    url = models.CharField(max_length=1000,null=True)
    display = models.ImageField(upload_to ='uploads/')
    expire_date =  models.DateTimeField(auto_now_add=False)
    universal = models.UUIDField()
    
class Visitor(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    universal = models.UUIDField() 
    ip_address_hash =  models.CharField(max_length=100)
# Create your models here.
