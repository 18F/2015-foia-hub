## foia-core

Core interaction between FOIA requestor and FOIA office.

The tentative plan for this repo is a Python API service, whose first pass is to contain -

* Receive and store a FOIA request from [foia-portal](https://github.com/18f/foia-portal).
* Publish received FOIA requests in the direction of the specified FOIA office.
* Send requestors a notice after the opening of a request, along with contact information for the FOIA office that is expected to handle the request.
* Send requestors a notice after the closing of a request, with the nature of the response and the necessary contact information to follow up on or appeal.
* Support the low-fidelity (is it open or closed?) status checking of individual requests in [foia-portal](https://github.com/18f/foia-portal).

This project is to be API-only, no templates. The user-facing portion resides at [foia-portal](https://github.com/18f/foia-portal), a static site.


## Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
