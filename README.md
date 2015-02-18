## FOIA Hub

[![Coverage Status](https://coveralls.io/repos/18F/foia-hub/badge.png)](https://coveralls.io/r/18F/foia-hub)

A starting place for FOIA in the US government.

This project is currently working on getting people to the right place in the government to file their FOIA request.

## Outside Contributors

Hello! If you're interested in learning more about this project, check out some related repos and don't be afraid to ask us questions (general questions usually go here: [foia](https://github.com/18F/foia)).

If you'd like to contribute to our project, please check out our [foia-hub](https://github.com/18F/foia-hub) repo. We try to tag things that are easy to pick up without being entrenched in our project with a ["help wanted"](https://github.com/18F/foia-hub/labels/help%20wanted%21) tag. Things in our [backlog](https://github.com/18F/foia-hub/milestones/Backlog) are usually also up for grabs, so let us know if you'd like to pick something up from there.

For those interested in contributing, please check out our [contributing guidelines](https://github.com/18F/foia-hub/blob/master/CONTRIBUTING.md) we use to guide our development processes internally.

## Our Repos

* [foia](https://github.com/18F/foia) - A discussion forum where we can discuss the project. Also includes miscellaneous resources and scrapers.
* [foia-hub](https://github.com/18F/foia-hub) - Where our work happens. We create issues related to each sprint and our backlog here. If you're interested in contribution, please look for "help wanted" tags or ask!

## How is this different from other stuff?

There are some [fantastic open source tools](https://github.com/18F/foia/wiki/Platforms) out there for processing FOIA requests, like Postcode's [RecordTrac](https://github.com/postcode/recordtrac) (which powers [FOI for the City of Oakland](http://records.oaklandnet.com/)) and mySociety's [Alavateli](http://www.alaveteli.org/) (used [all over the world](http://alaveteli.org/deployments/)).

Our platform, while still in its infancy, plans to be heavily optimized for the US federal government. It also plans to *not* be a backend tool for FOIA processing offices. In other words, there's no plans to allow government employees to log in to this system.

Instead, our tool will focus on a small, US-focused user experience, and API-driven integration for looking up FOIA contact information, submitting and receiving requests, and searching for responsive documents.

## Setup

This is a Django app that uses [Postgres](http://www.postgresql.org/) and [Elasticsearch](http://www.elasticsearch.org/), and depends on [Python 3](https://docs.python.org/3/).

**Installing Python 3**: There are multiple approaches to installing Python 3, depending on your personal setup and preferences.

1. You can use [`pyenv`](https://github.com/yyuu/pyenv) to download and install any version of Python to your home directory, and to switch easily between them. This separates your system Pythons from your development Pythons.
2. You can install Python 3 to your system. On OS X, install [Homebrew](http://brew.sh), then run `brew install Python3`. On Ubuntu, install using `apt-get install python3`.

**Installing Postgres**: You can `brew install postgres` (OS X) or `apt-get install postgresql` (Ubuntu).

**Installing Postgres**: You can `brew install elasticsearch` (OS X) or `apt-get install elasticsearch` (Ubuntu).

The instructions below assume you use [pip](http://pip.readthedocs.org/en/latest/), [virtualenv](http://virtualenv.readthedocs.org/en/latest/), and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) to manage dependencies.

### Project setup

Create an environment to install Python dependencies, with virtualenvwrapper.

* If you're using `pyenv`, activate Python 3 and run `mkvirtualenv foia-hub`.

* If you're using a system Python, specify the path to Python like so:

```bash
mkvirtualenv --python=/path/to/python3 foia-hub
```

* Install project requirements.

```bash
pip install -r requirements.txt
```

* **If using Ubuntu**, run the following before psycopg2 installed correctly:

```bash
sudo apt-get install libpq-dev python3-dev
```

* Add the following to your `~/.bashrc` or `~/.bash_profile` (change `/path/to/hub` to your actual path, e.g. `$HOME/projects/foia-hub`):

```bash
export PYTHONPATH=/path/to/hub:$PYTHONPATH
```

* Create a `local_settings.py` file inside `foia-hub/settings`. Start by copying the example:

```bash
cp foia_hub/settings/local_settings.py.example foia_hub/settings/local_settings.py
```

* In development, you may only need to update the password from `CHANGETHIS` to something else.

### Database setup

* Switch to the `postgres` user:

```bash
sudo su - postgres
```

* Create a `foia` database in Postgres:

```bash
createdb foia
```

Note, that the database encoding needs to be UTF8. If your default is set to something else, you can use:

```SQL
create database foia with encoding 'UTF8' LC_COLLATE='en_US.UTF8' LC_CTYPE='en_US.UTF8' TEMPLATE=template0;
```

If you you get a `could not connect to server` error, you could be experiencing a number of issues. Ensure that `$PGHOST` is set to `localhost`, and that the Postgres service has been started.

* Next, create user `foia` with some password:

```bash
psql -d foia -c "CREATE USER foia WITH PASSWORD '<<PASSWORD>>';"
```

* Change database password in local_settings.py:
```python
# Change the password below to the one you use
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'foia',
        'USER': 'foia',
        'PASSWORD': 'CHANGETHIS',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

* Initialize your database schema:

```bash
django-admin.py syncdb
```

### Elasticsearch setup

* Start the Elasticsearch server
```bash
elasticsearch
```

### Loading Contacts Data

Agency contact data is stored in another repository as YAML files.

Clone the repository:

```bash
git clone git@github.com:18F/foia.git
```

Then run the data loading script:

```bash
python manage.py load_agency_contacts /path/to/foia/contacts/data/
```

Note that the data repository is your local clone of:
[https://github.com/18F/foia/tree/master/contacts/data](https://github.com/18F/foia/tree/master/contacts/data])

There's a small bash script which will check for changes to the repository,
and if found, import the new data. This can be useful if combined with a cron
script to run on a routine basis. The script expects to be ran from the
foia-hub repository's root:

```bash
./check-new-data.sh <<path to foia repository>>
```

No repository parameter is needed if both the foia and foia-hub projects are
cloned into the same directory.

Now if you access: [http://localhost:8000/api/agency/](http://localhost:8000/api/agency/]), you'll the list of agencies in JSON format.

### Loading Responsive Documents

***Work in progress***

```bash
python manage.py import_documents
```


### Front-end Dev Environment

We use SASS, Bourbon, and Neat for our front-end stack. To set them up, you
will need ruby (and gem) installed. On a Debian/Linux box, this can be
accomplished via:

```bash
sudo apt-get install ruby
```

You next need to install the appropriate ruby libraries. In this example, we
will install them system wide, though you may prefer bundler, etc.

```bash
sudo gem install neat sass bourbon
```

You will then need to pull down the appropriate sass libraries for bourbon and
neat:

```bash
cd foia_hub/static/sass
bourbon install
neat install
```

While developing you can trigger a recompile or run a "watch" script, which
will recompile as you make Sass changes:

```bash
python manage.py scss   # one-off

python manage.py scss watch   # will run continuously
```

During development, then, you will likely have both `scss watch` and
`runserver`.

## Deploying

Install [Fabric](http://fabfile.org).

Fabric requires **Python 2.7**, so you may wish to make a separate virtualenv (e.g. `fab`) with Python 2.7 locked in it, and then activate it (e.g. `workon fab`) for the purposes of running Fabric commands.

```bash
pip install fabric
```

Make an entry in your `.ssh/config` file for the FOIA development server, and give it a name. Consult with the team if you need that information -- it's not sensitive, but it is subject to change.

Assuming the `.ssh/config` entry is named `foia`, test your configuration  with:

```bash
fab -H foia test
```

Deploy the site with:

```bash
fab -H foia deploy
```

This will check out a new copy of the site on the staging server, install dependencies and run migrations, and adjust some symlinks around to perform a zero-downtime deploy.

## Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright
> and related rights in the work worldwide are waived through the [CC0 1.0
> Universal public domain
> dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication.
> By submitting a pull request, you are agreeing to comply with this waiver of
> copyright interest.
