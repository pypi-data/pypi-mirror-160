### Libreria para conseguir cotizaciones sobre envio de paquetes con la API de shipengine (FedEx)

```python
from fedexrates.rates import Rate

quote_params = {
    "address_from": {
        "zip": "64000",
        "country": "MX"
    },
    "address_to": {
        "zip": "64000",
        "country": "MX"
    },
    "parcel": {
        "length": 25.0,
        "width": 28.0,
        "height": 46.0,
        "distance_unit": "cm",
        "weight": 6.5,
        "mass_unit": "kg"
    }
}
credentials = "TEST_DR6z1zWA0vFKnL+Znjk3FpRlLBEKGpKDg7N/yF7AShY"
rate = Rate(quote_params=quote_params, credentials=credentials)

print(rate.get_rate())
```