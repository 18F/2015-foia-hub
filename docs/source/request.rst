============
Request APIs
============

---------------------
Making a FOIA request
---------------------

""""""""""""""""""""""""""""""
Caveat
""""""""""""""""""""""""""""""

The request API is still a work in progress and does not actually submit FOIA requests.

This starts the process of documenting the API.


""""""""""""""""""""""""""""""
POST /api/request/
""""""""""""""""""""""""""""""

Inputs

A JSON object with at least the following fields:

+-----------+--------------------------------+
| Field     | Description                    |
+===========+================================+
| agency    | The slug for the Agency.       |
+-----------+--------------------------------+
| office    | The slug for the Office.       |
+-----------+--------------------------------+
| first_name| The requester's first name     |
+-----------+--------------------------------+
| last_name | The requester's  last name     |
+-----------+--------------------------------+
| email     | The requester's emailxxx       |
+-----------+--------------------------------+
| body      | The body of the FOIA request   |
+-----------+--------------------------------+

Either ``agency``, or ``agency`` and ``office``, must be provided.

Additional Fields

+-----------------+--------------------------------------------------------+
| Field           | Description                                            |
+=================+========================================================+
| documents_start | The beginning date for the documents requested.        |
+-----------------+--------------------------------------------------------+
| documents_end   | The end date for the documents requested.              |
+-----------------+--------------------------------------------------------+

If you would like to attach a start and end date to the documents you are
requesting, you can do that through documents_start and documents_end. Dates
are represented as strings in the following format: January 01, 1979.

""""""""""""""""""""""""""""""
POST /api/request/
""""""""""""""""""""""""""""""

This simply returns all the requests that have been created in the system.

This currently returns::

    {
       "objects":[
          {
             "tracking_id":1,
             "status":"O"
          },
          {
             "tracking_id":2,
             "status":"O"
          },
          {
             "tracking_id":3,
             "status":"O"
          },
          {
             "tracking_id":4,
             "status":"O"
          }
       ]
    }
