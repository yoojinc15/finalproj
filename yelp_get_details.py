import requests
import json
import secrets  # file that contains API key
from time import sleep


def open_cache():
    try:
        with open('SF_businesses_details.json', "r") as j:
            c = json.load(j)
    except:
        c = {}
    return c


def make_request(baseurl, params=''):
    sleep(0.5)
    print(params)
    headers = {
        "Authorization": f'Bearer {secrets.yelp_key}',
    }
    response = requests.get(baseurl, headers=headers, params=params).json()
    return response


def make_request_with_cache(baseurl, id):
    # print("Fetching")
    if id in businesses_details.keys():
        print("cache hit!")
        return businesses_details[id]
    else:
        print("cache miss!")
        result = make_request(baseurl+id)
        return result
    #result = make_request(baseurl, params)
    #return result

businesses_details = {}
city = "SF"
result_dict = {}
url = "https://api.yelp.com/v3/businesses/"

with open('SF_businesses.json', "r") as j:
    list = json.load(j)

businesses_details = open_cache()
i = 1
total = len(list)
for k, v in list.items():
    result = make_request_with_cache(url, k)
    try:
        nid = result["id"]
    except KeyError:
        nid = "fail"
    print(f'[{i}/{total}]...{k} / {nid}')
    businesses_details[k] = result
    with open("SF_businesses_details.json", "w") as j:
        json.dump(businesses_details, j)
    i += 1



