from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='trips.index'),
    path('planner/', views.create_trip, name='trips.planner'),
    path('delete/<int:trip_id>/', views.delete_trip, name='trips.delete'),
]
