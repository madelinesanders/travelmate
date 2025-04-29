from django.urls import path
from . import views

urlpatterns = [
    path('forecast/<int:trip_id>/', views.forecast, name='weather_forecast'),
    path('packing-list/<int:trip_id>/', views.packing_list, name='packing_list'),
    path('tips/<int:trip_id>/', views.travel_tips, name='travel_tips'),
]