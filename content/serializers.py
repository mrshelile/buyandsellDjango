from content.models import *
from rest_framework import  serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BannerSerializer(serializers.HyperlinkedModelSerializer):
     class Meta:
        model = Banner
        fields = ['url','created','owner','link','display','expire_date','splashscreen','home','universal']       

class FeaturedAdsSerializer(serializers.HyperlinkedModelSerializer):
     class Meta:
        model = FeaturedAd
        fields = ['url','created','link','display','expire_date','universal']          
        
class ProductSerializer(serializers.HyperlinkedModelSerializer):
     class Meta:
        model = Product
        fields = ['url','created','owner','name','description','price','expire_date','identifier','display','category']          
        
class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'full_name','phone1','is_superuser','is_active')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            is_active=validated_data['is_active'],
            is_superuser=validated_data['is_superuser'],
            phone1=validated_data['phone1'],
            username=validated_data['username'],
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            
        )

        user.set_password(validated_data['password'])
        user.save()

        return user        