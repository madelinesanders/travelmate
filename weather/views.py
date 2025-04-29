from django.shortcuts import render, get_object_or_404
from trips.models import Trip
from datetime import timedelta, date
from calendar import month_name
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
from weather.open_meteo import get_monthly_avg
from travelmate.weather_strategies import ForecastWeatherStrategy, HistoricalWeatherStrategy
from travelmate.ollama_client import generate_packing_list, generate_travel_tips

def forecast(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    today = date.today()
    forecast_window = today + timedelta(days=14)

    forecast_data = []
    historical_data = []
    extreme_alerts = []

    if trip.start_date <= forecast_window:
        strategy = ForecastWeatherStrategy()
        forecast_data, extreme_alerts, current = strategy.fetch_weather(trip, today)

        if current is None:
            current = trip.start_date

        if current <= trip.end_date:
            historical_strategy = HistoricalWeatherStrategy()
            historical_data, _, _ = historical_strategy.fetch_weather(trip, current)
    else:
        historical_strategy = HistoricalWeatherStrategy()
        historical_data, _, _ = historical_strategy.fetch_weather(trip, trip.start_date)

    months = {
        month_name[m].lower(): get_monthly_avg(trip.latitude, trip.longitude, m)
        for m in range(trip.start_date.month, trip.end_date.month + 1)
    }

    location_name = ""
    try:
        geolocator = Nominatim(user_agent="travelmate")
        location = geolocator.reverse((trip.latitude, trip.longitude), language="en")
        if location:
            addr = location.raw.get("address", {})
            city = addr.get("city") or addr.get("town") or addr.get("village") or addr.get("hamlet")
            state = addr.get("state")
            country = addr.get("country")
            location_name = ", ".join(filter(None, [city, state, country]))
    except GeocoderUnavailable:
        location_name = f"{trip.latitude}, {trip.longitude}"

    labels = [entry["date"] for entry in forecast_data]
    max_temps = [entry["temp_max"] for entry in forecast_data]
    min_temps = [entry["temp_min"] for entry in forecast_data]

    return render(request, 'weather/forecast.html', {
        "trip": trip,
        "location_name": location_name,
        "forecast_data": forecast_data,
        "historical_data": historical_data,
        "historical_start": forecast_window + timedelta(days=1),
        "historical_end": trip.end_date,
        "averages": months,
        "labels": labels,
        "max_temps": max_temps,
        "min_temps": min_temps,
        "extreme_alerts": extreme_alerts,
    })

def packing_list(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)

    if not trip.packing_list:
        print("🔵 No packing list yet, generating with Ollama...")
        summary = f"Trip from {trip.start_date} to {trip.end_date} at {trip.location}."
        activities = list(trip.activities.values_list('name', flat=True))

        packing_list_text = generate_packing_list(summary, activities)

        trip.packing_list = packing_list_text
        trip.save()
    else:
        print("🟢 Loading cached packing list from database...")

    return render(request, 'weather/packing_list.html', {
        "trip": trip,
        "packing_list": trip.packing_list,
    })

def travel_tips(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)

    if not trip.travel_tips:
        print("🔵 No travel tips yet, generating with Ollama...")
        summary = f"Trip to {trip.location} from {trip.start_date} to {trip.end_date}."
        travel_tips_text = generate_travel_tips(summary)

        trip.travel_tips = travel_tips_text
        trip.save()
    else:
        print("🟢 Loading cached travel tips from database...")

    return render(request, 'weather/travel_tips.html', {
        "trip": trip,
        "travel_tips": trip.travel_tips,
    })
