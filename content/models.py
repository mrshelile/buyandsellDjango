from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
import uuid 

class MultiImage(models.Model):
    image =models.ImageField(upload_to ='')
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.created)

class User(AbstractUser):
    created = models.DateTimeField(auto_now_add=True)
    otp = models.CharField(null=True,default='',max_length=2000,blank=True)
    full_name = models.CharField(max_length=2000,null=True,default='')
    phone1 = models.CharField(max_length=2000,null=True,default='')
    phone2 = models.CharField(max_length=2000,null=True,default='',blank=True)
    validated = models.BooleanField(default=False)
    is_reset_password= models.BooleanField(default=False,verbose_name="Reset Password")
    email = models.EmailField(unique=True)
    # def save(self, *args, **kwargs):
        # if not self.pk:
        #     token = Token.objects.create(user=self)
        #     print(token.key) 
        # super().save(*args, **kwargs)  
        # token = Token.objects.create(user=self)
        # print(token.key) 
        # print("done")


class Car(models.Model):
    model = models.CharField(max_length=2000)
    year= models.IntegerField()
    fuel= models.CharField(max_length=2000,verbose_name="Fuel Type")
    make = models.CharField(max_length=2000)
    kilos= models.CharField(max_length=2000)
    transmission = models.CharField(max_length=2000)
    
    def __str__(self):
            return str(self.year) +" " +self.model+ " " +self.make
    
class Product(models.Model):
    choices= [
    ('cars', 'cars'),
    ('miscellaneous', 'miscellaneous'),
    ]
    created = models.DateTimeField(auto_now_add=True)
    owner= models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=2000,null=True,default=None,blank=True)
    description = models.TextField(max_length=2000,null=True,default=None,blank=True)
    price =  models.IntegerField()
    expire_date = models.DateTimeField()
    identifier = models.UUIDField(editable=False,default = uuid.uuid4,unique=True,)
    display = models.ManyToManyField(MultiImage,)
    category = models.CharField(max_length=2000,choices=choices)
    car = models.OneToOneField(Car, on_delete=models.CASCADE,null=True,default=None,blank=True)
    
    def __str__(self):
        return  str(self.created)
       

class Banner(models.Model):
    created = models.DateTimeField(auto_now_add=True,null=True)
    link = models.CharField(max_length=2000,null=True,blank=True)
    owner = models.CharField(max_length=2000,null=True)
    display = models.ForeignKey(MultiImage, on_delete=models.CASCADE)
    expire_date =  models.DateTimeField(auto_now_add=False,null=True)
    splashscreen =  models.BooleanField(default=True)
    home =  models.BooleanField(default=True)
    universal = models.UUIDField(editable=False,default = uuid.uuid4,unique=True)
    
    def __str__(self):
        return self.owner
    
class FeaturedAd(models.Model):
    created = models.DateTimeField(auto_now_add=True)    
    link = models.CharField(max_length=2000,null=True,blank=True)
    owner = models.CharField(max_length=2000)
    display = models.ForeignKey(MultiImage, on_delete=models.CASCADE)
    expire_date =  models.DateTimeField(auto_now_add=False)
    universal = models.UUIDField(editable=False,default = uuid.uuid4,unique=True)
    
    def __str__(self):
        return self.owner
    
class Visitor(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    universal = models.UUIDField(editable=False,default = uuid.uuid4,unique=True,) 
    ip_address_hash =  models.CharField(max_length=2000)
    
    def __str__(self):
        return self.ip_address_hash
    
# Create your models here.
