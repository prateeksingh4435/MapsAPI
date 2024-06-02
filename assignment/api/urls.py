from django.contrib import admin
from django.urls import path,include
from .import views
from knox import views as knox_views

urlpatterns = [
    path('location/', views.searchlocationandsave, name='location'),
    path('', views.CreateLocation.as_view(), name='location'),
    path('<int:pk>',views.RetrieveUpdateDeleteLocation.as_view()),
    path('map/', views.search, name='map_search'),
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/',knox_views.LogoutView.as_view())
    
    
    
]
