

============
Contact APIs
============

----------------
Listing Agencies
----------------

""""""""""""""""""""""""""""""
GET /api/agency/
""""""""""""""""""""""""""""""

Lists all agencies for whom a FOIA request can be submitted. 

It also includes components within those agencies that are large enough (and
well known enough) to have their own FOIA system. Examples are such components are:

* Census Bureau
* Federal Bureau of Investigation

The information returned for each entity is the following::

    {"name": "AMTRAK",
    "description": "The National Railroad Passenger Corporation,
    Amtrak is a government-owned corporation striving to deliver a high quality,
    safe, on-time rail passenger service that exceeds customer expectations. Learn
    all about Amtrak here from every angle.",
    "slug": "amtrak",
    "abbreviation": "NRPC",
    "common_requests": "on-time statistics",
    "simple_processing_time": "3",
    "complex_processing_time": "45",
    "keywords": ["trains"]}


A note on processing times. 

The response for each entity provides two statistics around the processing
times for FOIA requests:

1. simple_processing_time
2. complex_processing_time

Both values are presented in number of days. 

'Simple' and 'Complex' requests are defined as the following by foia.gov:

Complex request: "Complex requests are FOIA requests that an agency anticipates
will involve a voluminous amount of material to review or will be time
consuming to process."

Simple request: "A FOIA request that an agency anticipates will involve a small
volume of material or will be able to processed relatively quickly. 


""""""""""""""""""""""""""""""""""
GET /api/agency/{{slug}}
""""""""""""""""""""""""""""""""""

where {{slug}} is a slug that identifies an agency. 

This returns something like the following::

    {
        "abbreviation": "NRPC",
        "address_lines": [
            "Sharron H. Hawkins",
            "FOIA Officer"
        ],
        "city": "Washington",
        "common_requests": [],
        "description": "The National Railroad Passenger Corporation, Amtrak is a government-owned corporation striving to deliver a high quality, safe, on-time rail passenger service that exceeds customer expectations. Learn all about Amtrak here from every angle.",
        "emails": [
            "foiarequests@amtrak.com"
        ],
        "fax": "202-906-3285",
        "is_a": "agency",
        "keywords": null,
        "name": "AMTRAK",
        "no_records_about": [],
        "office_url": "http://www.amtrak.com/servlet/ContentServer/Page/1241267362261/1241267362261",
        "offices": [],
        "person_name": "Phone: (202) 906-3740",
        "phone": "202-906-3741",
        "public_liaison_email": null,
        "public_liaison_name": "Sharron H. Hawkins",
        "public_liaison_phone": "202 906-3740",
        "request_form_url": null,
        "slug": "amtrak",
        "state": "DC",
        "street": "60 Massachusetts Avenue, NE",
        "toll_free_phone": null,
        "zip_code": "20002"
    }

""""""""""""""""""""""""""""""""""
GET /api/office/{{slug}}
""""""""""""""""""""""""""""""""""

where {{slug}} is a slug that identifies an office (a component of an Agency). 

This returns something like the following::

    {
        "address_lines": [
            "Stacy Cheney",
            "FOIA Officer, Office of the Chief Counsel",
            "Room 4713"
        ],
        "agency_description": "The historic mission of the Department of Commerce is \"to foster, promote, and develop the foreign and domestic commerce\" of the United States. This has evolved, as a result of legislative and administrative additions, to encompass broadly the responsibility to foster, serve, and promote the Nation's economic development and technological advancement.",
        "agency_name": "Department of Commerce",
        "agency_slug": "department-of-commerce",
        "city": "Washington",
        "emails": [
            "eFOIA@ntia.doc.gov"
        ],
        "fax": "202-501-8013",
        "id": 291,
        "is_a": "office",
        "name": "National Telecommunications and Information Administration",
        "office_url": "http://www.ntia.doc.gov/ntiahome/occ/foia.html",
        "person_name": "Phone: (202) 482-1816",
        "phone": "202-482-1816",
        "public_liaison_email": null,
        "public_liaison_name": "Stacy Cheney",
        "public_liaison_phone": "202 482-1816",
        "request_form_url": null,
        "slug": "department-of-commerce--national-telecommunications-and-information-admini",
        "state": "DC",
        "street": "14th Street and Constitution Avenue, NW",
        "toll_free_phone": null,
        "zip_code": "20230"
    }
