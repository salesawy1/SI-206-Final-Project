import requests

def get_teleport_data(city_name):
    ua_endpoint = get_urban_area_endpoint(city_name)
    results = {}
    if ua_endpoint:
        details = get_area_details(ua_endpoint)
        results['details'] = details
        images = get_area_images(ua_endpoint)
        results['images'] = images
        scores = get_area_scores(ua_endpoint)
        results['scores'] = scores

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

def get_area_images(ua_endpoint):
    try:
        r = requests.get(ua_endpoint + 'images/')
        r = r.json()
        return r['photos']
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

city_name = 'London'
results = get_teleport_data(city_name)
print(results)