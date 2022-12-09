from rest_framework import viewsets,generics
from content.serializers import *
from rest_framework.mixins import CreateModelMixin
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
 
class UserProductViewset(generics.ListAPIView):
    serializer_class= ProductSerializer
    
    def get_queryset(self):
        
        # user = get_object_or_404(queryset, pk=pk)
        owner=self.kwargs['owner']
        queryset = Product.objects.filter(owner=owner)
        return queryset
    
    
      
          