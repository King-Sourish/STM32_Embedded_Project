from django.urls import path
from . import views

urlpatterns = [
    path('', views.sensor_data_view, name='sensor_data'),
    path('api/sensor-data/', views.sensor_data_list, name='sensor_data_api'),
    
]
