from django.urls import path
from .import views
urlpatterns =[
	path('', views.Homeview, name='home'),
	path('remove/<city_name>/', views.City_Delete, name='city_remove'),


]