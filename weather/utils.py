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