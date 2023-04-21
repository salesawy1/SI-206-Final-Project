import googlemaps # https://github.com/googlemaps/google-maps-services-python
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))

def get_location_count(term, location):
    geocode_result = gmaps.geocode(location)
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    places_result = gmaps.places_nearby(location=(lat, lng), radius=5000, keyword=term)

    return len(places_result['results'])

# print(get_location_count('factories', 'seattle, wa'))