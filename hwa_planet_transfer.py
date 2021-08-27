
import os
from pprint import pprint
import requests
from requests.auth import HTTPBasicAuth
import json

#line 1: add your API key in plain text file (config)
#line 2: add google earth project name
# see https://developers.planet.com/docs/integrations/gee/

with open('config', 'r') as f:
    PLANET_API_KEY = f.readline()
    GEE_PROJECT = f.readline()

search_request = {
    "item_types": [
        "PSScene4Band"
    ],
    "filter": {
        "type": "AndFilter",
        "config": [
            {
                "field_name": "geometry",
                "type": "GeometryFilter",
                "config": {
                    "coordinates": [
                        [
                            [
                                -74.674411,
                                41.886921
                            ],
                            [
                                -74.070216,
                                41.886921
                            ],
                            [
                                -74.070216,
                                42.21141
                            ],
                            [
                                -74.674411,
                                42.21141
                            ],
                            [
                                -74.674411,
                                41.886921
                            ]
                        ]
                    ],
                    "type": "Polygon"
                }
            }
            ,
            {
                "field_name": "acquired",
                "type": "DateRangeFilter",
                "config": {
                    "gte": "2021-01-27T14:17:09Z",
                    "lte": "2021-02-27T14:17:09Z"
                }
            },
            {
                "field_name": "cloud_cover",
                "type": "RangeFilter",
                "config": {
                    "lte": 0.01
                }
            },
            {
                "type": "AssetFilter",
                "config": [
                    "analytic_sr"
                ]
            },
            {
                "type": "AssetFilter",
                "config": [
                    "udm"
                ]
            }
        ]
    }
}

def get_scene_id_list():
    # fire off the POST request
    search_result =   requests.post(
        'https://api.planet.com/data/v1/quick-search',
        auth=HTTPBasicAuth(PLANET_API_KEY, ''),
        json=search_request)
    results_json = json.loads(search_result.content)
    #print(results_json)
    feature_list = results_json['features']
    scene_id_list = [f['id'] for f in feature_list]
    return scene_id_list

delivery_request = {
  "name": "HWA",
  "products": [],
  "delivery": {
    "google_earth_engine": {
      "project": GEE_PROJECT,
      "collection": "test_collection"
    }
  }
}

def put_delivery_request(scene_id_list):
    # https://developers.planet.com/docs/orders/product-bundles-reference/
    # BUNDLE: analytic_sr_udm2
    # Corrected for surface reflectance – recommended for most analytic applications
    product_ = \
        {
        "item_ids": scene_id_list,  # add files here
        "item_type": "PSScene4Band",
        "product_bundle": "analytic_sr"
    }
    delivery_request["products"].append(product_)

    # fire off the POST request
    search_result =   requests.post(
        'https://api.planet.com/compute/ops/orders/v2',
        auth=HTTPBasicAuth(PLANET_API_KEY, ''),
        json=delivery_request)
    results_json = json.loads(search_result.content)
    print(results_json)

if __name__ == '__main__':
    id_ = get_scene_id_list()
    print(len(id_))
    put_delivery_request(id_)