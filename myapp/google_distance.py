import requests
import json




class GoogleDistance:
    def get_distance_data(origin,destinations,apikey):
        parameters = {'destinations': '|'.join(destinations), 'origins': origin, 'sensor': 'false', 'key': apikey}
        data = requests.post('https://maps.googleapis.com/maps/api/distancematrix/json',params=parameters)
        datadict = json.loads(data.content.decode("utf-8"))
        results = {}
        for city,info in zip(datadict['destination_addresses'],datadict['rows'][0]['elements']):
            results[city] = {}
            results[city]['distance_text'] = info['distance']['text'] 
            results[city]['duration_text'] = info['duration']['text']
            results[city]['distance_value'] = info['distance']['value']
            results[city]['duration_value'] = info['duration']['value']
        return results




