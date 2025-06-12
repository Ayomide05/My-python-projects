import geopy
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my_app")
location = geolocator.geocode("Brasil")


latitude = location.latitude
longitude = location.longitude

print(latitude, longitude)