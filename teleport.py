import requests

def get_teleport_data(city_name):
    ua_endpoint = get_urban_area_endpoint(city_name)
    results = {}
    if ua_endpoint:
        details = get_area_details(ua_endpoint)
        results['details'] = details

    return results

def get_urban_area_endpoint(city_name):
    try:
        cities_endpoint = 'https://api.teleport.org/api/cities/'
        url = f'{cities_endpoint}?search={city_name}'
        r = requests.get(url)
        r = r.json()
        r['_embedded']
        geoname_url = r['_embedded']['city:search-results'][0]['_links']['city:item']['href']
        r2 = requests.get(geoname_url)
        r2 = r2.json()
        ua_endpoint = r2['_links']['city:urban_area']['href']
        return ua_endpoint
    except:
        return None

def get_area_details(ua_endpoint):
    try:
        r = requests.get(ua_endpoint + 'details/')
        r = r.json()
        result = {}
        for cat in r['categories']:
            result[cat['label']] = {}
            for i in cat['data']:
                name = i['label']
                key = [k for k in i.keys() if 'value' in k][0]
                score = i[key]
                result[cat['label']][name] = score
        return result
    except:
        return 'not_found'

def get_area_scores(ua_endpoint):
    try:
        r = requests.get(ua_endpoint + 'scores/')
        r = r.json()
        result = {}
        for i in r['categories']:
            name = i['name']
            score = i['score_out_of_10']
            result[name] = score
        return result
    except:
        return 'not_found'
    
def get_details(city_name, details):
    detail_map = {
        'air_quality': get_air_quality,
        'drinking_water_quality': get_drinking_water_quality
    }
    
    data = get_teleport_data(city_name)
    
    res = {}
    for detail in details:
        if detail in detail_map:
            res[detail] = detail_map[detail](data)
        else:
            res[detail] = 'not_found'
            
    return res

def get_air_quality(data):
    try:
        return data['details']['Environmental Quality']['Air quality [Teleport score]']
    except:
        return 'not_found'
    
def get_drinking_water_quality(data):
    try:
        return data['details']['Environmental Quality']['Drinking water quality [Teleport score]']
    except:
        return 'not_found'

# results = get_details('Seattle', ['air_quality', 'drinking_water_quality'])
# print(results)