import requests
from datetime import date

def get_forecast(lat, lon, start_date, end_date):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "daily": "temperature_2m_max,temperature_2m_min,weathercode",
        "timezone": "auto"
    }
    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        return res.json()
    except requests.RequestException as e:
        print(f"❌ Forecast API error: {e}")
        return {}

def get_historical(lat, lon, target_date):
    historical_date = date(target_date.year - 1, target_date.month, target_date.day)
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": historical_date.isoformat(),
        "end_date": historical_date.isoformat(),
        "daily": "temperature_2m_max,temperature_2m_min,weathercode",
        "timezone": "auto",
        "past_days": 0
    }
    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        return res.json()
    except requests.RequestException as e:
        print(f"❌ Historical API error: {e}")
        return {}

def get_monthly_avg(lat, lon, month):
    from calendar import monthrange
    import statistics

    year = date.today().year - 1  # Use last year as climate proxy
    start = date(year, month, 1)
    end = date(year, month, monthrange(year, month)[1])

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "daily": "temperature_2m_mean",
        "temperature_unit": "celsius",
        "timezone": "auto"
    }

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        temps = data.get("daily", {}).get("temperature_2m_mean", [])
        if temps:
            return round(statistics.mean(temps), 1)
        return None
    except requests.RequestException as e:
        print(f"❌ Monthly Avg via historical daily failed: {e}")
        return None


