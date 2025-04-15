from geopy.geocoders import Nominatim
from geopy.exc import GeopyError

def get_lat_lon_from_location(location_name):
    geolocator = Nominatim(user_agent="my_app")
    try:
        location = geolocator.geocode(location_name)
        if location:
            return location.latitude, location.longitude
    except GeopyError:
        pass
    return None, None

