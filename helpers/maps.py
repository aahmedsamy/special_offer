import requests
from django.conf.settings import PLACES_MAPS_API_KEY

class Map():
    """
    set GOOGLE_MAPS_API_KEY in {project_name.settings}
    and edit the line {2} to be like from {project_name.settings} import GOOGLE_MAPS_API_KEY
    """
    def __init__(self):
        self.api_key = PLACES_MAPS_API_KEY
        self.distance_api = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={},{}&destinations={},{}&key={}'
        self.city_id_api = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key={}'
        self.time_api = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins={},{}&destinations={},{}&key={}'
    
    @classmethod
    def convert_distance(cls, distance):
        """
        take the distance in meters and convert it to kilometers if distance >= 1000
        else returns distance  
        """
        if distance >= 1000:
            return "{} km".format(distance/1000)
        return "{} m".format(distance)
        
    @classmethod
    def get_distance(cls, lat1, lon1, lat2, lon2):
        try:
            resp = requests.get(self.distance_api.format(lat1, lon1, lat2,
                lon2, self.api_key))
            if resp.json()['rows'][0]['elements'][0]['status'] == "ZERO_RESULTS":
                return 1000000000
            return int(resp.json()['rows'][0]['elements'][0]['distance']['value'])
        except :
            return 1000000000

    @staticmethod
    def get_city_id(lat, lon):
        try:
            res = requests.get(self.city_id_api.format(
                lat,
                lon,
                self.api_key))
            for res in res.json()['results']:
                for i in res['types']:
                    if i == "administrative_area_level_1":
                        return res['place_id']
            return None
        except:
            return None

    @staticmethod
    def get_time(lat,lon,lat2,lon2):
        try:
            res = requests.get(self.time_api.format(
                    lat, lon, lat2, lon2, self.api_key))
            time = res.json()['rows'][0]['elements'][0]['duration']['text']
            return time
        except :
            return "No routes found"