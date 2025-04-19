
from django.shortcuts import render, get_object_or_404
from trips.models import Trip
from datetime import timedelta, date
from .open_meteo import get_forecast, get_historical, get_monthly_avg
from calendar import month_name
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable

def get_icon(code):
    mapping = {
        0: "wi-day-sunny.svg",
        1: "wi-day-sunny-overcast.svg",
        2: "wi-day-cloudy.svg",
        3: "wi-cloudy.svg",
        45: "wi-day-fog.svg", 48: "wi-day-fog.svg",
        51: "wi-day-rain.svg", 53: "wi-day-rain.svg", 55: "wi-day-rain.svg",
        56: "wi-day-rain.svg", 57: "wi-day-rain.svg",
        61: "wi-day-showers.svg", 63: "wi-day-showers.svg", 65: "wi-day-showers.svg",
        66: "wi-day-rain-wind.svg", 67: "wi-day-rain-wind.svg",
        71: "wi-day-snow.svg", 73: "wi-day-snow.svg", 75: "wi-day-snow.svg",
        77: "wi-day-snow.svg",
        80: "wi-day-showers.svg", 81: "wi-day-showers.svg", 82: "wi-day-showers.svg",
        85: "wi-day-snow.svg", 86: "wi-day-snow.svg",
        95: "wi-day-thunderstorm.svg",
        96: "wi-day-storm-showers.svg",
        99: "wi-day-lightning.svg"
    }
    return f"/static/icons/{mapping.get(code, 'wi-alien.svg')}"

def forecast(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    today = date.today()
    forecast_window = today + timedelta(days=14)

    forecast_data = []
    historical_data = []
    extreme_alerts = []

    if trip.start_date <= forecast_window:
        forecast_end = min(trip.end_date, forecast_window)
        forecast_json = get_forecast(trip.latitude, trip.longitude, trip.start_date, forecast_end)

        for i, day in enumerate(forecast_json.get("daily", {}).get("time", [])):
            max_temp = forecast_json["daily"]["temperature_2m_max"][i]
            min_temp = forecast_json["daily"]["temperature_2m_min"][i]
            code = forecast_json["daily"]["weathercode"][i]
            formatted_date = date.fromisoformat(day).strftime("%B %d, %Y")

            forecast_data.append({
                "date": formatted_date,
                "raw_date": day,
                "temp_max": max_temp,
                "temp_min": min_temp,
                "description": "Forecasted",
                "icon_url": get_icon(code)
            })

            if max_temp >= 35:
                extreme_alerts.append({
                    "text": f"🔥 High heat on {formatted_date}",
                    "c": round(max_temp, 1),
                    "type": "max"
                })
            if min_temp <= 0:
                extreme_alerts.append({
                    "text": f"❄️ Freezing temperatures on {formatted_date}",
                    "c": round(min_temp, 1),
                    "type": "min"
                })
            if code in [95, 96, 99]:
                extreme_alerts.append({
                    "text": f"⛈️ Thunderstorm risk on {formatted_date}",
                    "c": None,
                    "type": "storm"
                })

        current = forecast_end + timedelta(days=1)
    else:
        current = trip.start_date

    while current <= trip.end_date:
        hist_json = get_historical(trip.latitude, trip.longitude, current)
        daily = hist_json.get("daily", {})
        if "temperature_2m_max" in daily:
            formatted_date = current.replace(year=current.year - 1).strftime("%B %d, %Y")
            historical_data.append({
                "date": formatted_date,
                "raw_date": current.isoformat(),
                "temp": daily["temperature_2m_max"][0],
                "description": "Historical (same date last year)",
                "icon_url": get_icon(daily["weathercode"][0])
            })
        current += timedelta(days=1)

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
