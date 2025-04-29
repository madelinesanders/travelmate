from abc import ABC, abstractmethod
from datetime import timedelta, date
from weather.open_meteo import get_forecast, get_historical
from weather.utils import get_icon
import time


class WeatherStrategy(ABC):
    @abstractmethod
    def fetch_weather(self, trip, today):
        pass

class ForecastWeatherStrategy(WeatherStrategy):
    def fetch_weather(self, trip, today):
        forecast_window = today + timedelta(days=14)
        forecast_end = min(trip.end_date, forecast_window)
        forecast_json = get_forecast(trip.latitude, trip.longitude, trip.start_date, forecast_end)

        forecast_data = []
        extreme_alerts = []

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
                extreme_alerts.append({"text": f"🔥 High heat on {formatted_date}", "c": round(max_temp, 1), "type": "max"})
            if min_temp <= 0:
                extreme_alerts.append({"text": f"❄️ Freezing temperatures on {formatted_date}", "c": round(min_temp, 1), "type": "min"})
            if code in [95, 96, 99]:
                extreme_alerts.append({"text": f"⛈️ Thunderstorm risk on {formatted_date}", "c": None, "type": "storm"})

        return forecast_data, extreme_alerts, forecast_end + timedelta(days=1)

class HistoricalWeatherStrategy(WeatherStrategy):
    def fetch_weather(self, trip, start_date):
        current = start_date
        historical_data = []

        while current <= trip.end_date:
            hist_json = get_historical(trip.latitude, trip.longitude, current)
            daily = hist_json.get("daily", {})
            if "temperature_2m_max" in daily:
                formatted_date = current.replace(year=current.year - 1).strftime("%B %d, %Y")
                historical_data.append({
                    "date": formatted_date,
                    "raw_date": current.isoformat(),
                    "temp_max": daily["temperature_2m_max"][0],
                    "temp_min": daily["temperature_2m_min"][0],
                    "description": "Historical (same date last year)",
                    "icon_url": get_icon(daily["weathercode"][0])
                })
            current += timedelta(days=1)

        return historical_data, [], None