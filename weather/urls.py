from django.urls import path
from . import views

urlpatterns = [
    path('forecast/<int:trip_id>/', views.forecast, name='weather_forecast'),
]