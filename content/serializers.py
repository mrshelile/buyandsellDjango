from content.models import *
from rest_framework import  serializers

class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = '__all__'

class MultiImageSerializer(serializers.ModelSerializer):
    class Meta:
        model= MultiImage
        fields=['id','image']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # read_only_fields = ['url']

class BannerSerializer(serializers.HyperlinkedModelSerializer):

     class Meta:
        model = Banner
        fields = ['id','url','created','owner','link','display','expire_date','splashscreen','home','universal']       

class BannerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields='__all__'        

class FeaturedAdsSerializer(serializers.HyperlinkedModelSerializer):
     class Meta:
        model = FeaturedAd
        fields = ['id','url','created','owner','link','display','expire_date','universal']    

class FeaturedAdsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedAd
        fields='__all__'           
        
class ProductSerializer(serializers.HyperlinkedModelSerializer):
     display = MultiImageSerializer(many=True,required=False)
    #  owner= serializers.PrimaryKeyRelatedField(queryset= User.objects.all(),)
     class Meta:
        model = Product
        fields = ['id','url','created','owner','name','description','price','expire_date','identifier','display','category']          
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields='__all__'
class MulitImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=MultiImage
        fields=['id','url','image','created']
        
class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password','validated', 'otp','email', 'full_name','phone1','is_superuser','is_active')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    
    def create(self, validated_data):
        user = User.objects.create(
            is_active=validated_data['is_active'],
            is_superuser=validated_data['is_superuser'],
            phone1=validated_data['phone1'],
            otp=validated_data['otp'],
            validated=validated_data['validated'],
            username=validated_data['username'],
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            
        )

        user.set_password(validated_data['password'])
        user.save()

        return user   

class PasswordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'otp','email','is_reset_password' )
        write_only_fields = ('password','is_reset_password')
        read_only_fields = ('id','email') 
    
    # def update(self, instance, validated_data):
            
