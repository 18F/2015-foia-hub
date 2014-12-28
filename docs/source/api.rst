

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

The information returned for each entity is like the following::

    {
      "objects": [
        {
          "slug": "administration-for-community-living",
          "keywords": null,
          "abbreviation": "ACL",
          "description": "ACL brings together the efforts and achievements of the Administration on Aging, the Administration on Intellectual and Developmental Disabilities, and the HHS Office on Disability to serve as the Federal agency responsible for increasing access to community supports, while focusing attention and resources on the unique needs of older Americans and people with disabilities across the lifespan.",
          "name": "Administration for Community Living",
          "common_requests": [

          ]
        },
        {
          "slug": "administrative-conference-of-the-united-states",
          "keywords": [
            "Administrative practice and procedure",
            "Freedom of information",
            "Privacy"
          ],
          "abbreviation": "ACUS",
          "description": "The Administrative Conference of the United States is an independent federal agency dedicated to improving the administrative process through consensus-driven applied research, providing nonpartisan expert advice and recommendations for improvement of federal agency procedures.  Its membership is composed of innovative federal officials and experts with diverse views and backgrounds from both the private sector and academia.",
          "name": "Administrative Conference of the United States",
          "common_requests": [

          ]
        }
        ...

      ]
    }

""""""""""""""""""""""""""""""""""
GET /api/agency/{{slug}}
""""""""""""""""""""""""""""""""""

where {{slug}} is a slug that identifies an agency.

This returns the following::

    {
        "no_records_about": [

        ],
        "keywords": [
            "Accounting",
            "Administrative practice and procedure",
            "Aged",
            "Air traffic controllers",
            "Alcoholism",
            "Alimony",
            "Archives and records",
            ...
        ],
        "request_form_url": "https://secure.ssa.gov/apps9/eFOIA-FEWeb/internet/main.jsp?action=OPD",
        "office_url": "http://www.ssa.gov/foia/",
        "is_a": "agency",
        "phone": "410-965-1727",
        "zip_code": "21235",
        "name": "Social Security Administration",
        "agency_slug": "social-security-administration",
        "abbreviation": "SSA",
        "public_liaison_email": null,
        "state": "MD",
        "address_lines": [
            "Dawn S. Wiggins",
            "Principal Public FOIA Liaison",
            "Office of the General Counsel, Office of Privacy and Disclosure"
        ],
        "city": "Baltimore",
        "slug": "social-security-administration",
        "emails": [
            "Foia.pa.officers@ssa.gov"
        ],
        "toll_free_phone": null,
        "street": "617 Altmeyer Building",
        "agency_name": "Social Security Administration",
        "person_name": "Rhonda Smith",
        "offices": [

        ],
        "simple_processing_time": 18.0,
        "public_liaison_phone": "410 965-1727",
        "common_requests": [

        ],
        "fax": "410-966-0869",
        "description": "The Social Security Administration's mission is to deliver Social Security services that meet the changing needs of the public.",
        "foia_libraries": [
            {
                "url": "http://www.ssa.gov/foia/readingroom.html",
                "link_text": "FOIA Library"
            }
        ],
        "complex_processing_time": 45.0,
        "public_liaison_name": "Dawn S. Wiggins"
    }


**Processing Times.**

The response for each entity provides two statistics around the processing
times for FOIA requests:

1. simple_processing_time
2. complex_processing_time

Both values are presented in number of working days.

'Simple' and 'Complex' requests are defined as the following by foia.gov:

Complex request: "Complex requests are FOIA requests that an agency anticipates
will involve a voluminous amount of material to review or will be time
consuming to process."

Simple request: "A FOIA request that an agency anticipates will involve a small
volume of material or will be able to processed relatively quickly."

**FOIA Libaries**

The response for each entity provides a foia_libraries list. A FOIA library is
a URL to an online page that lists responsive documents an entity has decided
to make available publicly. This is a list because agencies/offices sometimes
have multiple FOIA libraries.

* url: The URL of the online FOIA library
* link_text: The link text that is associated with that library. This helps a human determine the difference between libraries.

""""""""""""""""""""""""""""""""""
GET /api/office/{{slug}}
""""""""""""""""""""""""""""""""""

where {{slug}} is a slug that identifies an office (a component of an Agency).

This returns the following::

    {
        "office_url": "http://www.ntia.doc.gov/ntiahome/occ/foia.html",
        "agency_description": "The historic mission of the Department of Commerce is \"to foster, promote, and develop the foreign and domestic commerce\" of the United States. This has evolved, as a result of legislative and administrative additions, to encompass broadly the responsibility to foster, serve, and promote the Nation's economic development and technological advancement.",
        "request_form_url": "https://foiaonline.regulations.gov/foia/action/public/home",
        "city": "Washington",
        "is_a": "office",
        "phone": "202-482-1816",
        "zip_code": "20230",
        "name": "National Telecommunications and Information Administration",
        "agency_slug": "department-of-commerce",
        "public_liaison_phone": "202 482-1816",
        "state": "DC",
        "address_lines": [
            "Stacy Cheney",
            "FOIA Officer, Office of the Chief Counsel",
            "Room 4713"
        ],
        "public_liaison_email": null,
        "office_slug": "national-telecommunications-and-information-admini",
        "emails": [
            "eFOIA@ntia.doc.gov"
        ],
        "toll_free_phone": null,
        "id": 180,
        "agency_name": "Department of Commerce",
        "person_name": "Phone: (202) 482-1816",
        "simple_processing_time": 7,
        "slug": "department-of-commerce--national-telecommunications-and-information-admini",
        "fax": "202-501-8013",
        "street": "14th Street and Constitution Avenue, NW",
        "foia_libraries": [],
        "complex_processing_time": 18,
        "public_liaison_name": "Stacy Cheney"
    }
