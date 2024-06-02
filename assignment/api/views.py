
import requests
from django.http import JsonResponse
from .serializers import LocationSerializer
from.models import Location
from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView
from rest_framework import generics,permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer,ResgisterSerializer
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as knoxLoginView
from rest_framework import permissions
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes





@permission_classes([IsAuthenticated])
def searchlocationandsave(request):
    location = request.GET.get('query')
    if not location:
        return JsonResponse({'error': 'Query parameter "query" is missing'}, status=400)
    geocode_url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json&limit=1"

    try:
       
        response = requests.get(geocode_url)
        response.raise_for_status()  
        data = response.json()
        if data:
            latitude = float(data[0]['lat'])
            longitude = float(data[0]['lon'])
            location, created = Location.objects.get_or_create(name=location, defaults={'latitude': latitude, 'longitude': longitude})
            
            if not created:
                location.latitude = latitude
                location.longitude = longitude
                location.save()
            serializer = LocationSerializer(location)
            serialized_data = serializer.data
            serialized_data['latitude'] = latitude
            serialized_data['longitude'] = longitude   
            return JsonResponse({'latitude': latitude, 'longitude': longitude})
        else:
            return JsonResponse({'error': 'Location not found'}, status=404)
    except requests.RequestException as e:
        return JsonResponse({'error': f'Failed to fetch location data: {e}'}, status=500)
    
    
class CreateLocation(ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]
    
    
class RetrieveUpdateDeleteLocation(RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]
    
    

def search(request):
    return render(request, 'location.html')



class RegisterAPI(generics.GenericAPIView):
    serializer_class = ResgisterSerializer

    def post(self,request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True )
        user = serializer.save()
        return Response({'user':UserSerializer(user,context=self.get_serializer_context()).data,
                         "token":AuthToken.objects.create(user)[1]
                         })
    
      
    
    
class LoginAPI(knoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self,request,*args,**kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request,user)
        return super(LoginAPI,self).post(request,format = None)
        
