import googlemaps
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))

def return_count(term, location):
    geocode_result = gmaps.geocode(location)
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    places_result = gmaps.places_nearby(location=(lat, lng), radius=5000, keyword=term)

    return places_result['results'].length

# print('factories', 'seattle, wa')