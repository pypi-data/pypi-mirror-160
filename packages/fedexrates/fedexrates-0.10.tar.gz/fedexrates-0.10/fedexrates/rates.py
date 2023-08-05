import requests
import json

import datetime

CURRENT_TIME = datetime.datetime.now().isoformat()

class Rate:
    def __init__(self, quote_params=dict, credentials=str):
        self.quote_params = quote_params
        self.credentials = credentials
        self.json_request = self.get_json_request()
        self.response = self.do_request()
        self.json =  self.get_json_response()

    def get_json_request(self):
        unit = {"kg":"kilogram", "cm":"centimeter"}
        weight_unit =  self.quote_params["parcel"]["mass_unit"]
        if(weight_unit in unit):
            weight_unit = unit[weight_unit]
        dimensions_unit =  self.quote_params["parcel"]["distance_unit"]
        if(dimensions_unit in unit):
            dimensions_unit = unit[dimensions_unit]

        from_postal_code =  self.quote_params["address_from"]["zip"]
        from_country_code =  self.quote_params["address_from"]["country"]
        to_postal_code =  self.quote_params["address_to"]["zip"]
        to_country_code =  self.quote_params["address_to"]["country"]
        weight = {
            "value":  self.quote_params["parcel"]["weight"],
            "unit": weight_unit
        }
        dimensions = {
            "unit": dimensions_unit,
            "length":  self.quote_params["parcel"]["length"],
            "width":  self.quote_params["parcel"]["width"],
            "height":  self.quote_params["parcel"]["height"],
        }

        json_request = {
            "carrier_ids": ["se-2634847", "se-2634846", "se-2634848"],
            "from_country_code": from_country_code,
            "from_postal_code": from_postal_code,
            "to_country_code": to_country_code,
            "to_postal_code": to_postal_code, 
            "weight": weight,
            "dimensions": dimensions,
            "confirmation": "none",
            "address_residential_indicator": "unknown",
            "ship_date": CURRENT_TIME
        }
        return json_request

    def do_request(self):
        url = "https://api.shipengine.com/v1/rates/estimate"
        payload = json.dumps(self.json_request)
        headers = {
        'Host': 'api.shipengine.com',
        'API-Key': self.credentials,
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        response_json = response.json()
        return response_json

    def get_json_response(self):
        new_response = []
        for i in self.response:
            if(i['error_messages']==[]):
                price = 0
                price+=i["shipping_amount"]["amount"]
                price+=i["insurance_amount"]["amount"]
                price+=i["confirmation_amount"]["amount"]
                price+=i["other_amount"]["amount"]

                service_level = {
                    "name":i["service_type"],
                    "token":i["service_code"]
                }
                json = {
                    "price":price,
                    "currency":i["shipping_amount"]["currency"].upper(),
                    "service_level":service_level
                }
                new_response.append(json)
        return new_response

    def get_rate(self):
        return self.json