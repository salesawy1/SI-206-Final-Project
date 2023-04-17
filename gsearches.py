import requests

params = {
  'access_key': '6325a8d1a25b250d4183ad372333c85f',
  'query': 'mcdonalds'
}

api_result = requests.get('http://api.serpstack.com/search', params)

api_response = api_result.json()

print("Total results: ", api_response['search_information']['total_results'])

for number, result in enumerate(api_response['organic_results'], start=1):
    print("%s. %s" % (number, result['title']))