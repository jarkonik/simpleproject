import requests
import json



class GoogleDistance:
    def get_distance_data(origin,destinations,apikey):
        parameters = {'destinations': '|'.join(destinations), 'origins': origin, 'sensor': 'false', 'key': apikey}
        data = requests.post('https://maps.googleapis.com/maps/api/distancematrix/json',params=parameters)
        datadict = json.loads(data.content.decode("utf-8"))
        results = {}
        print(datadict)
        if datadict['status']=='OK':
            for city,info in zip(datadict['destination_addresses'],datadict['rows'][0]['elements']):
  
                results[city] = {}
                duration = info.get('duration',{})
                distance = info.get('distance',{})
                results[city]['distance_text'] = distance.get('text','could not find connection')
                results[city]['duration_text'] = duration.get('text','could not find connection')
                results[city]['distance_value'] = distance.get('value',-1)
                results[city]['duration_value'] = duration.get('value',-1)

            return results
        else:
            return None




