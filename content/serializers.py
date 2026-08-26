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
 
class ViewerSeriarializer(serializers.ModelSerializer):
        
    class Meta:
        model = Viewer
        fields = '__all__'       
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # read_only_fields = ['url']

class ViewerSeriarializer(serializers.ModelSerializer):
        
    class Meta:
        model = Viewer
        fields = '__all__'           

class BannerSerializer(serializers.HyperlinkedModelSerializer):

     class Meta:
        model = Banner
        fields = ['id','url','created','title','promotion_type','owner','link','display','expire_date','splashscreen','home','universal']
        read_only_fields = ['id', 'url', 'created', 'universal']

class BannerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id','created','title','promotion_type','owner','link','display','expire_date','splashscreen','home','universal']
        read_only_fields = ['id', 'created', 'owner', 'universal']

    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            validated_data['owner'] = user.full_name or user.username
        return super().create(validated_data)

class PromotionSerializer(serializers.HyperlinkedModelSerializer):
    display_detail = MultiImageSerializer(source='display', read_only=True)

    class Meta:
        model = Promotion
        fields = ['id','url','created','title','promotion_type','owner','link','display','display_detail','expire_date','splashscreen','home','universal']
        read_only_fields = ['id', 'url', 'created', 'universal']

class PromotionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id','created','title','promotion_type','owner','link','display','expire_date','splashscreen','home','universal']
        read_only_fields = ['id', 'created', 'owner', 'universal']

    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            validated_data['owner'] = user.full_name or user.username
        return super().create(validated_data)

class FeaturedAdsSerializer(serializers.HyperlinkedModelSerializer):
     class Meta:
        model = FeaturedAd
        fields = ['id','url','created','owner','link','display','expire_date','universal']    

class FeaturedAdsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedAd
        fields='__all__'           

class PromotionFlyerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = serializers.CharField()
    title = serializers.CharField(allow_blank=True, required=False)
    promotion_type = serializers.CharField(allow_blank=True, required=False)
    link = serializers.CharField(allow_blank=True, required=False)
    image_url = serializers.CharField(allow_blank=True, required=False)
    splashscreen = serializers.BooleanField(required=False)
    home = serializers.BooleanField(required=False)
    owner = serializers.CharField(allow_blank=True, required=False)
    expire_date = serializers.DateTimeField(required=False)

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model= Car
        fields='__all__'  
           
class ProductSerializer(serializers.HyperlinkedModelSerializer):
     viewers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
     display = MultiImageSerializer(many=True,required=False)
     car = CarSerializer(many=False)
    #  owner= serializers.PrimaryKeyRelatedField(queryset= User.objects.all(),)
     class Meta:
        model = Product
        fields = ['id','viewers','url','created','car','owner','name','description','price','expire_date','identifier','display','category']          
          
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['owner', 'created', 'identifier']

    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            raise serializers.ValidationError('Authentication is required to create an ad.')
        validated_data['owner'] = user
        return super().create(validated_data)
class MulitImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=MultiImage
        fields=['id','url','image','created']
        
class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password','validated', 'otp','email', 'full_name','phone1','is_superuser','is_staff','is_active')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        allow_superuser = bool(user and user.is_authenticated and getattr(user, 'is_superuser', False))

        is_superuser = validated_data.get('is_superuser', False)
        is_staff = validated_data.get('is_staff', False)

        if not allow_superuser:
            is_superuser = False
            is_staff = False

        if is_superuser:
            is_staff = True

        user_instance = User.objects.create(
            is_active=validated_data['is_active'],
            is_superuser=is_superuser,
            is_staff=is_staff,
            phone1=validated_data['phone1'],
            otp=validated_data['otp'],
            validated=validated_data['validated'],
            username=validated_data['username'],
            email=validated_data['email'],
            full_name=validated_data['full_name'],
        )

        user_instance.set_password(validated_data['password'])
        user_instance.save()

        return user_instance

class PasswordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'otp','email','is_reset_password' )
        write_only_fields = ('password','is_reset_password')
        read_only_fields = ('id','email') 
    
    # def update(self, instance, validated_data):
            
