from rest_framework import viewsets,generics
from content.serializers import *
from rest_framework.mixins import CreateModelMixin
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['email','username']

class CreateUserView(CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserAuthSerializer  

class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer    

class FeaturedAdsViewSet(viewsets.ModelViewSet):
    queryset = FeaturedAd.objects.all()
    serializer_class = FeaturedAdsSerializer 
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name','category',]

class ProductCreateViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    
class MuitiImageViewset(viewsets.ModelViewSet):
    queryset = MultiImage.objects.all()
    serializer_class = MulitImageSerializer
    
    
class UserProductViewset(generics.ListAPIView):
    serializer_class= ProductSerializer
    
    def get_queryset(self):
        # user = get_object_or_404(queryset, pk=pk)
        owner=self.kwargs['owner']
        queryset = Product.objects.filter(owner=owner)
        return queryset

class SendEmailViewset(APIView):
    
    def post(self,request):
        try:
            email = request.data['email']
            subject= request.data['subject']
            body = request.data['body']
        
            send_mail(
                subject,
                body,
                settings.EMAIL_HOST_USER,
                [email]
            )
            return Response({"message":"email is sent"},status=status.HTTP_200_OK)  
        except(Exception):
            return Response({"message":"failed to send email"},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

class OTPUpdateViewset(APIView):
    
    def put(self,request,format=None):
        try:
            user =User.objects.filter(email=request.data['email'])
            if user.values():
                user.update(otp=request.data['otp'],is_reset_password=True)
                return Response({"user is in reset mode"},status=status.HTTP_200_OK)
            raise Exception
        except(Exception):
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdatePasswordViewset(APIView):
    def put(self,request,format=None):
        try:
            user= User.objects.filter(username=request.data['email'])
            
            if  user.values():
                password_validation.validate_password(request.data['password'])
                user.update(is_reset_password=False,password=make_password(request.data['password']),otp='')
                return Response({"message":"password updated"},status=status.HTTP_200_OK)
            raise Exception
        except(Exception):
            return Response({"message":"failed to update password"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ValidateAccByOTpViewset(APIView):
    def put(self,request,format=None):
        try:
            user= User.objects.filter(username=request.data['email'],validated=False)
            
            if  user.values():
                user.update(validated=True,otp='')
                return Response({"message":"account validated"},status=status.HTTP_200_OK)
            raise Exception
        except(Exception):
            return Response({"message":"failed to validate account"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class UploadImages()