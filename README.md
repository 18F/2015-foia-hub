## foia-core

Core interaction between FOIA requestor and FOIA office.

The tentative plan for this repo is a Python API service, whose first pass is to contain -

* Receive and store a FOIA request from [foia-portal](https://github.com/18f/foia-portal).
* Publish received FOIA requests in the direction of the specified FOIA office.
* Send requestors a notice after the opening of a request, along with contact information for the FOIA office that is expected to handle the request.
* Send requestors a notice after the closing of a request, with the nature of the response and the necessary contact information to follow up on or appeal.
* Support the low-fidelity (is it open or closed?) status checking of individual requests in [foia-portal](https://github.com/18f/foia-portal).

This project is to be API-only, no templates. The user-facing portion resides at [foia-portal](https://github.com/18f/foia-portal), a static site.

## Setting up FOIA-Core

Below are some general instructions to setup FOIA-Core. In the future, we will try offer an automated process.

### General info

Repo: https://github.com/18F/foia-core.git

Reqs:
- [Python3](https://docs.python.org/3/)
* [Postgres](http://www.postgresql.org/)
* [virtualenv](http://virtualenv.readthedocs.org/en/latest/) & [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/)
* [git](http://git-scm.com/)

Option reqs:
* [homebrew](http://brew.sh/)

### System setup

Install [homebrew](http://brew.sh/) according to the instuctions on the homepage.

Brew install python3, postgres, and git
```
brew install python3
brew install postgres
brew install git
```

Pip install virtualenv
```
pip install virtualenv
```

Install and setup virtualenv wrapper.
```
pip install virtualenvwrapper
```

Then create a shell startup file [according to these instructions](http://virtualenvwrapper.readthedocs.org/en/latest/install.html#shell-startup-file
). This is so you don't have to enter these settings every time you open a new terminal window.


### Project setup

Create environment to install python dependencies.
```
mkvirtualenv --python=/usr/local/bin/python3 foia-core
```

cd to where you wnant to put the code & pull down the repo
```
git clone https://github.com/18F/foia-core.git
```

cd into the foia-core directory and add that to the virtual environment
```
cd foia-core
add2virtualenv .
```

Install project requirements. (From inside the foia-core folder.)
```
pip install -r requirements.txt
```

Set your django settings module.
```
export DJANGO_SETTINGS_MODULE=foia_core.settings.dev
```


### Database set up

Create foia database
```
createdb foia
```

If you run into the following error:
```
createdb: could not connect to database template1: could not connect to server: No such file or directory
    Is the server running locally and accepting
    connections on Unix domain socket "/var/pgsql_socket/.s.PGSQL.5432"?
```
then try to add the PGHOST settings
```
export PGHOST=localhost
```

Create user foia w/ password foia. (If use something else, make sure to update your local Django settings file appropriately to match.)
```
psql -d foia -c "CREATE USER foia WITH PASSWORD 'foia';"
```


### Getting Started

Sync database using django
(Assumes you have django setting module set & db set up.)
```
django-admin.py syncdb
```

Launch server locally
```
django-admin.py runserver
```
If you want a specific port
```
django-admin.py runserver 0.0.0.0:8080
```

View locally in your browser:
```
http://localhost:8000/data/agency/
```


## Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
