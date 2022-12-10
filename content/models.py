from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token

class MultiImage(models.Model):
    image =models.ImageField(upload_to ='uploads/')
    
    def __str__(self):
        return self.image
    
class User(AbstractUser):
    created = models.DateTimeField(auto_now_add=True)
    otp = models.IntegerField(null=True,default='0')
    full_name = models.CharField(max_length=30,null=True,default='')
    phone1 = models.CharField(max_length=30,null=True,default='')
    phone2 = models.CharField(max_length=30,null=True,default='')
    validated = models.BooleanField(default=False)
    is_reset_password= models.BooleanField(default=False,verbose_name="Reset Password")
    # def save(self, *args, **kwargs):
        # if not self.pk:
        #     token = Token.objects.create(user=self)
        #     print(token.key) 
        # super().save(*args, **kwargs)  
        # token = Token.objects.create(user=self)
        # print(token.key) 
        # print("done")
    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         # This code only happens if the objects is
    #         # not in the database yet. Otherwise it would
    #         # have pk
    #         pass
    #     token = Token.objects.create(user=self)
    #     print(token.key)
    #     super(User, self).save(*args, **kwargs)
    
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
    identifier = models.UUIDField(unique=True,auto_created=True)
    display = models.ManyToManyField(MultiImage)
    category = models.CharField(max_length=50,choices=choices)
    
    def __str__(self):
        return self.name
    
       

class Banner(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=1000,null=True)
    owner = models.CharField(max_length=30)
    display = models.ImageField(upload_to ='uploads/')
    expire_date =  models.DateTimeField(auto_now_add=False)
    splashscreen =  models.BooleanField()
    home =  models.BooleanField()
    universal = models.UUIDField(auto_created=True,unique=True)
    
    def __str__(self):
        return self.owner
    
class FeaturedAd(models.Model):
    created = models.DateTimeField(auto_now_add=True)    
    link = models.CharField(max_length=1000,null=True)
    owner = models.CharField(max_length=30)
    display = models.ImageField(upload_to ='uploads/')
    expire_date =  models.DateTimeField(auto_now_add=False)
    universal = models.UUIDField(auto_created=True,unique=True)
    
    def __str__(self):
        return self.owner
    
class Visitor(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    universal = models.UUIDField() 
    ip_address_hash =  models.CharField(max_length=100)
    
    def __str__(self):
        return self.ip_address_hash
    
# Create your models here.
