from django.shortcuts import render, redirect
from .forms import TripForm
from .models import Trip
from django.conf import settings
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from trips.sorting_strategies import (
    SortByStartDateStrategy, SortByEndDateStrategy,
    SortByLocationStrategy, SortByDurationStrategy,
    TripSorter
)

def create_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.latitude = request.POST.get('latitude')
            trip.longitude = request.POST.get('longitude')
            trip.save()
            form.save_m2m()
            return redirect('weather_forecast', trip_id=trip.id)
    else:
        form = TripForm()
    return render(request, 'trips/planner.html', {
        'form': form,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    })

def index(request):
    trips = Trip.objects.filter(user=request.user)

    sort_method = request.GET.get('sort', 'start')  # Get ?sort=start, default to start

    if sort_method == 'start':
        strategy = SortByStartDateStrategy()
    elif sort_method == 'end':
        strategy = SortByEndDateStrategy()
    elif sort_method == 'location':
        strategy = SortByLocationStrategy()
    elif sort_method == 'duration':
        strategy = SortByDurationStrategy()
    else:
        strategy = SortByStartDateStrategy()  # fallback

    sorter = TripSorter(strategy)
    trips = sorter.sort_trips(trips)

    return render(request, 'trips/index.html', {'trips': trips})

def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    trip.delete()
    return redirect('trips.index')