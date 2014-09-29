

============
Contact APIs
============

The two concepts to know here is that there are two entities: (i) Agencies like
the Department of Commerce and (ii) top-tier Offices like the Census Bureau. 

Top tier offices are large enough (and well known enough) to have their own
FOIA system. 

----------------
Listing Agencies
----------------

""""""""""""""""""""""""""""""
/api/agencyoffice/autocomplete
""""""""""""""""""""""""""""""

This API returns a list of all Agencies and top-tier Offices in the system. 
The information returned for each entity is the following::

    {"name": "AMTRAK",
    "description": "The National Railroad Passenger Corporation,
    Amtrak is a government-owned corporation striving to deliver a high quality,
    safe, on-time rail passenger service that exceeds customer expectations. Learn
    all about Amtrak here from every angle.",
    "slug": "amtrak",
    "abbreviation": "NRPC",
    "keywords": ["trains"]}

""""""""""""""""""""""""""""""""""
/api/agencyoffice/contact/{{slug}}
""""""""""""""""""""""""""""""""""

where slug is a slug that identifies an office or agency. 

This returns something like the following::

    {"agency_slug": "amtrak",
    "offices": [{
        "id": 123,
        "request_form": null,
        "fax": "202-906-3285",
        "slug": "amtrak--amtrak-national-railroad-passenger-corporation",
        "public_liaison": "Sharron H. Hawkins, Phone: (202) 906-3740",
        "name": "AMTRAK (National Railroad Passenger Corporation)",
        "emails": "['foiarequests@amtrak.com']",
        "contact": "['Sharron H. Hawkins', 'FOIA Officer', '60 Massachusetts Avenue, NE', 'Washington, DC 20002']",
        "website": "http://www.amtrak.com/servlet/ContentServer/Page/1241267362261/1241267362261",
        "notes": null,
        "service_center": "Phone: (202) 906-3740", "contact_phone": null}],
    "agency_name": "AMTRAK"}
