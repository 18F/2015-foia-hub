## FOIA Hub

[![Coverage Status](https://coveralls.io/repos/18F/foia-hub/badge.png)](https://coveralls.io/r/18F/foia-hub)

A starting place for FOIA in the US government.

This project is currently working on getting people to the right place in the government to file their FOIA request.

Some related repos:

* [foia](https://github.com/18F/foia) - Discussion forum and miscellaneous resources and scrapers.
* [foia-search](https://github.com/18F/foia-search) - Experimental full text search API over FOIA materials.

## How is this different from other stuff?

There are some [fantastic open source tools](https://github.com/18F/foia/wiki/Platforms) out there for processing FOIA requests, like Postcode's [RecordTrac](https://github.com/postcode/recordtrac) (which powers [FOI for the City of Oakland](http://records.oaklandnet.com/)) and mySociety's [Alavateli](http://www.alaveteli.org/) (used [all over the world](http://alaveteli.org/deployments/)).

Our platform, while still in its infancy, plans to be heavily optimized for the US federal government. It also plans to *not* be a backend tool for FOIA processing offices. In other words, there's no plans to allow government employees to log in to this system.

Instead, our tool will focus on a small, US-focused user experience, and API-driven integration for tools to submit, and receive submissions, through the US Freedom of Information Act.

## Setup

This is a Django app that uses [Postgres](http://www.postgresql.org/), and depends on [Python 3](https://docs.python.org/3/).

**Installing Python 3**:
There are multiple approaches to installing Python 3, depending on your personal setup and preferences.

One option is to [pyenv](https://github.com/yyuu/pyenv) to manage downloading Python 3 or you can install them directly.

For OS X, install Homebrew](http://brew.sh) (OS X), then run `brew install Python3`. For Ubuntu, install using `apt-get install Python3`.

**Installing Postgres**: You can `brew install postgres` (OS X) or `apt-get install postgresql` (Ubuntu).

The instructions below assume you use [pip](http://pip.readthedocs.org/en/latest/), [virtualenv](http://virtualenv.readthedocs.org/en/latest/), and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) to manage dependencies.

### Project setup

Create an environment to install Python dependencies, with virtualenvwrapper.

```bash
mkvirtualenv --python=/path/to/python3 foia-hub
```

Note: You don't need to explicitly specify the Python version, especially if you use pyenv + virtualenvwrapper. Running mkvirtualenv in that scenario will 'freeze' the currently active version of Python.


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
export PYTHONPATH=/path/to/hub:PYTHONPATH
```

* Create a `local_settings.py` file inside `foia-hub/settings`. Start by copying the example:

```bash
cp foia_hub/settings/local_settings.py.example foia_hub/settings/local_settings.py
```

* In development, you may not need to update anything. It assumes a local Postgres database named `foia` with a username of `foia` and a password of `foia`. Change this if need be.

### Database setup

Create a `foia` database in Postgres:

```bash
createdb foia
```

Note, that the database encoding needs to be UTF8. If your default is set to something else, you can use:

```SQL
create database foia with encoding 'UTF8' LC_COLLATE='en_US.UTF8' LC_CTYPE='en_US.UTF8' TEMPLATE=template0;
```

If you you get a `could not connect to server` error, you could be experiencing a number of issues. Check the following:
* PGHOST is set to localhost. If not `export PGHOST=localhost` to your bash profile.
* Postgres has been started.

Next, create user `foia` with password <<PASSWORD>>:

```bash
psql -d foia -c "CREATE USER foia WITH PASSWORD '<<PASSWORD>>';"
```

where <<PASSWORD>> is a password of your choosing.

Initialize your database schema:

```bash
django-admin.py syncdb
```

Finally, launch the server locally:

```
django-admin.py runserver
```

The site should be running at [`http://localhost:8000`](http://localhost:8000).

### Loading Data

Agency contact data is stored in another repository as YAML files.

Clone the repository:

```bash
git clone git@github.com:18F/foia.git
```

Then run the data loading script:

```bash
cd foia_hub
python manage.py load_agency_contacts <<path to foia repository>>/foia/contacts/data/
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

