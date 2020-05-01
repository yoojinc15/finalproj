from bs4 import BeautifulSoup
import requests
import json
import secrets  # file that contains your API key
from time import sleep
import os.path
import math

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
    # if request_key in result_dict.keys():
    if os.path.isfile(request_key + '.json'):
        print("Using cache")
        pass
    else:
        print("Fetching")
        result = make_request(baseurl, params)
        save_cache(result, request_key + '.json')
        result_dict[request_key] = result
        print("saved")
        return result


city = "SF"
result_dict = {}
url = "https://api.yelp.com/v3/businesses/search"

"""SF
"""
start_latitude = 37.812368
start_longitude = -122.513110
end_latitude = 37.708291
end_longitude = -122.366566

categories = "food"
radius = 300
limit = 50
offset = 0

latitude = start_latitude
longitude = start_longitude

while latitude > end_latitude and longitude < end_longitude:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "categories": categories,
        "radius": radius,
        "limit": limit,
        "offset": 0
        }
    result = make_request_with_cache(url, params)
    try:
        print(result['total'])
        if result['total'] > 50:
            i = 1
            for i in range(math.ceil(result['total']/50)-1):
                params = {
                    "latitude": latitude,
                    "longitude": longitude,
                    "categories": categories,
                    "radius": radius,
                    "limit": limit,
                    "offset": (i+1)*50
                }
                result = make_request_with_cache(url, params)
    except TypeError:
        print("Type Error")


    latitude = latitude - 0.00208154
    if latitude < end_latitude:
        latitude = start_latitude
        longitude = longitude + 0.00293088

# save_cache(result_dict, city + '.json')
