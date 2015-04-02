

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

""""""""""""""""""""""""""""""
GET /api/agency/?query={{search terms}}
""""""""""""""""""""""""""""""

To search agencies, you can provide the parameter 'query'. A GET request with this query string will initiate a full-text search across the following Agency fields weighted in the following order: name, abbreviation, slug, description, and keywords.

By default, search terms are connect with boolean "AND"; hence, the queries "/api/agency/?query=justice+punishment" and "/api/agency/?query=justice+AND+punishment" only return agencies that have both terms::

    {
       "objects": [
          {
             "keywords": [
                "Accounting",
                "Administrative practice and procedure",
                ...
             ],
             "description": "The Department of Justice works to enforce federal law, to seek just punishment for the guilty, and to ensure the fair and impartial administration of justice.",
             "common_requests": "[]",
             "name": "Department of Justice",
             "abbreviation": "DOJ",
             "slug": "department-of-justice"
          }
       ]
    }

Explicitly using "OR" as in "/api/agency/?query=justice+OR+punishment" expands the search to include agencies that have at least one of the keywords::

    {
       "objects": [
          {
             "keywords": [
                "Accounting",
                "Administrative practice and procedure",
                ...
             ],
             "description": "The Department of Justice works to enforce federal law, to seek just punishment for the guilty, and to ensure the fair and impartial administration of justice.",
             "common_requests": "[]",
             "name": "Department of Justice",
             "abbreviation": "DOJ",
             "slug": "department-of-justice"
          },
          {
             "keywords": [
                "Intergovernmental relations",
                "Investigations",
                ...
             ],
             "description": "As an intelligence-driven and a threat-focused national security organization with both intelligence and law enforcement responsibilities, the mission of the FBI is to protect and defend the United States against terrorist and foreign intelligence threats, to uphold and enforce the criminal laws of the United States, and to provide leadership and criminal justice services to federal, state, municipal, and international agencies and partners.",
             "common_requests": "[]",
             "name": "Federal Bureau of Investigation",
             "abbreviation": "FBI",
             "slug": "federal-bureau-of-investigation"
          },
          {
             "keywords": [
                "Accountants",
                "Accounting",
                ...
             ],
             "description": "The Department of the Treasury manages Federal finances by collecting taxes and paying bills and by managing currency, government accounts and public debt. The Department of the Treasury also enforces finance and tax laws.",
             "common_requests": "[]",
             "name": "Department of the Treasury",
             "abbreviation": "Treasury",
             "slug": "department-of-the-treasury"
          }
          ...(more agencies)
       ]
    }

""""""""""""""""""""""""""""""""""
GET /api/agency/{{slug}}
""""""""""""""""""""""""""""""""""

Where {{slug}} is a slug that identifies an agency.

This returns the following agency data::

    {
       "toll_free_phone": null,
       "description": "The Social Security Administration assigns social security numbers; administers the retirement, survivors, and disability insurance programs known as Social Security; and administers the Supplemental Security Income program for the aged, blind, and disabled.",
       "fax": "410-966-0869",
       "street": "617 Altmeyer Building",
       "is_a": "agency",
       "city": "Baltimore",
       "address_lines": [
          "Dawn S. Wiggins",
          "Principal Public FOIA Liaison",
          "Office of the General Counsel, Office of Privacy and Disclosure"
       ],
       "phone": "410-965-1727",
       "foia_libraries": [
          {
             "url": "http: //www.ssa.gov/foia/readingroom.html",
             "link_text": "FOIA Library"
          }
       ],
       "complex_processing_time": 45.0,
       "no_records_about": [

       ],
       "request_form_url": "https: //secure.ssa.gov/apps9/eFOIA-FEWeb/internet/main.jsp?action=OPD",
       "abbreviation": "SSA",
       "agency_slug": "social-security-administration",
       "person_name": "Rhonda Smith",
       "agency_name": "Social Security Administration",
       "offices": [

       ],
       "office_url": "http: //www.ssa.gov/foia/",
       "common_requests": [

       ],
       "keywords": [
          "Accounting",
          "Administrative practice and procedure",
          "Adult education",
          ...
       ],
       "simple_processing_time": 18.0,
       "zip_code": "21235",
       "emails": [
          "Foia.pa.officers@ssa.gov"
       ],
       "public_liaison_name": "Dawn S. Wiggins",
       "public_liaison_email": null,
       "name": "Social Security Administration",
       "public_liaison_phone": "410-965-1727",
       "state": "MD",
       "slug": "social-security-administration"
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

Where {{slug}} is a slug that identifies an office (a component of an agency).

This returns the following office information::

    {
       "toll_free_phone": null,
       "fax": "202-501-8013",
       "street": "14th Street and Constitution Avenue, NW",
       "city": "Washington",
       "address_lines": [
          "Stacy Cheney",
          "FOIA Officer, Office of the Chief Counsel",
          "Room 4713"
       ],
       "phone": "202-482-1816",
       "foia_libraries": [

       ],
       "complex_processing_time": 18.0,
       "request_form_url": "https: //foiaonline.regulations.gov/foia/action/public/home",
       "agency_slug": "department-of-commerce",
       "person_name": null,
       "agency_name": "Department of Commerce",
       "agency_description": "The historic mission of the Department of Commerce is \"to foster, promote, and develop the foreign and domestic commerce\" of the United States. This has evolved, as a result of legislative and administrative additions, to encompass broadly the responsibility to foster, serve, and promote the Nation's economic development and technological advancement.",
       "is_a": "office",
       "office_url": "http: //www.ntia.doc.gov/ntiahome/occ/foia.html",
       "office_slug": "national-telecommunications-and-information-admini",
       "id": 174,
       "simple_processing_time": 7.0,
       "zip_code": "20230",
       "emails": [
          "eFOIA@ntia.doc.gov"
       ],
       "public_liaison_name": "Stacy Cheney",
       "public_liaison_email": null,
       "name": "National Telecommunications and Information Administration",
       "public_liaison_phone": "202-482-1816",
       "state": "DC",
       "slug": "department-of-commerce--national-telecommunications-and-information-admini"
    }
