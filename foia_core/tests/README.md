For the time being...

To test out the request API in your python interpretor try the following:

```
import json
import requests

url = 'http://localhost:8000/api/request/'
data = {
  "first_name": "Eric",
  "last_name": "Mill",
  "email": "eric.mill@gsa.gov",
  "body": "My request",
  "documents_start": "August 6, 2014",
  "documents_end": "August 8, 2014",
  "fee_limit": 0,
  "agency": "general-services-administration",
  "office": "headquarters",
  "agency_fields": {
    "region": "1A",
    "contract": "GS-1637848",
  }
}

r = requests.post(url, data=json.dumps(data))
r.json()
```

If it was successful this should output the following:
```
{'requester': 16,
 'fee_limit': 0,
 'status': 'O',
 'date_end': '2014-08-08T00:00:00',
 'date_start': '2014-08-06T00:00:00',
 'request_body': 'My request',
 'custom_fields': {'contract': 'GS-1637848', 'region': '1A'}}
 ```


 If you use this sample data, which is a bad set, it will return a 500:

 ```
data = {
  "first_name": "EricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEricEric",
  "last_name": "Mill",
  "email": "eric.mill@gsa.gov",
  "body": "My request",
  "documents_start": "August 6, 2014",
  "documents_end": "August 8, 2014",
  "fee_limit": 0,
  "agency": "general-services-administration",
  "office": "headquarters",
  "agency_fields": {
    "region": "1A",
    "contract": "GS-1637848",
  }
}
```

```
r.status_code
500

r.json()['error']
'value too long for type character varying(250)\n'
```
