'''
Name: Yoojin Choi   
Uniqname: yjinchoi
'''

from bs4 import BeautifulSoup
import requests
import json
import secrets  # file that contains your API key
from time import sleep
import os.path

def save_cache(cache_dict, file):
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(file, "w")
    fw.write(dumped_json_cache)
    fw.close()


def construct_unique_key(params=''):
    param_strings = []
    connector = '_'
    if params == '':
        unique_key = "none"
    else:
        for k, v in params.items():
            param_strings.append(f'{k}_{v}')
        param_strings.sort()
        unique_key = connector + connector.join(param_strings)
    return unique_key


def make_request(baseurl, params=''):
    sleep(2)
    print(params)
    headers = {
        "Authorization": f'Bearer {secrets.yelp_key}',
    }
    response = requests.get(baseurl, headers = headers, params=params).json()
    return response


def make_request_with_cache(baseurl, params=''):
    request_key = construct_unique_key(params)
    if os.path.isfile("yelp_cache/" + request_key):
        print("Using cache")
        pass
    else:
        print("Fetching")
        result = make_request(baseurl, params)
        save_cache(result, request_key + '.json')
        print("saved")
        pass

url = "https://api.yelp.com/v3/businesses/search"
start_latitude = 37.811747
start_longitude = -122.528932
end_latitude = 37.692587
end_longitude = -122.348859
categories = "food"

longitude = start_longitude
latitude = start_latitude
while latitude > end_latitude and longitude < end_longitude:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "categories": categories
              }
    make_request_with_cache(url, params)
    start_latitude = start_latitude + 0.000025
    start_longitude = start_longitude - 0.000013
    if start_latitude > end_latitude:
        latitude = start_latitude


