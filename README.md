## openFOIA

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

* **If using Ubuntu**, you may need to install the following:

```bash
sudo apt-get install libpq-dev python3-dev
```

* Install project requirements. It's recommended you use a virtualenv.

```bash
pip install -r requirements.txt
```

* Install [`autoenv`](https://github.com/kennethreitz/autoenv) to automatically load the contents of `.env` as environment variables. Do not use the `brew` version of `autoenv`.

* Copy `env.example` to `.env` to get your settings started.

```bash
cp env.example .env
```

### Using SQLite

If you're using SQLite, you're already done! Jump to [loading data](#loading-data).

### Using Postgres

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

* Initialize your database schema:

```bash
python manage.py syncdb
```

* Update the `DATABASE_URL` in `.env` with your Postgres connection string.

### Elasticsearch setup

* Start the Elasticsearch server
```bash
elasticsearch
```

### Running the tests

```
python manage.py test --settings=foia_hub.settings.test
```

### Loading Contacts Data

First, migrate the database:

```bash
python manage.py migrate
```

Agency contact data is stored in another repository as YAML files.

Clone the repository:

```bash
git clone git@github.com:18F/foia.git
```

Then run the data loading script, providing the path to `contacts/data/` inside the `foia` repo you checked out above:

```bash
python manage.py load_agency_contacts /path/to/foia/contacts/data/
```

There's a small bash script which will check for changes to the repository,
and if found, import the new data. This can be useful if combined with a cron
script to run on a routine basis. The script expects to be ran from the
foia-hub repository's root:

```bash
./check-new-data.sh <<path to foia repository>>
```

No repository parameter is needed if both the foia and foia-hub projects are
cloned into the same directory. You should be able to run the server now:

### Loading Responsive Documents

***Work in progress***

```bash
python manage.py import_documents
```

### Running the server

* Launch the server locally:

```
python manage.py runserver
```

* The site should be running at [`http://localhost:8000`](http://localhost:8000).



### Front-end Dev Environment

We use [Sass](http://sass-lang.com/), [Bourbon](http://bourbon.io/) and [Neat](http://neat.bourbon.io/) for our front-end stack.

You will need Ruby, and the following gems:

```bash
gem install sass bourbon neat
```

You will then need to pull down further Bourbon and Neat dependencies:

```bash
cd foia_hub/static/sass
bourbon install
neat install
```

While developing you can trigger a recompile or run a "watch" script, which will recompile as you make Sass changes:

```bash
python manage.py scss   # one-off

python manage.py scss watch   # will run continuously
```

During development, you will likely run both `scss watch` and `runserver`.

## Deploying to Cloud Foundry

18F deploys this app to a self-hosted instance of Cloud Foundry.

You'll need to configure an app named `foia` in the space or org that makes sense for you. We already have a [`manifest.yml`](manifest.yml) that assumes the app is named `foia`, and sets a memory size of 1GB.

#### 18F setup

Point `cf` at 18F's API. You may need to use `--skip-ssl`

```bash
cf api https://api.cf.18f.us
```

If the `cf api` command below fails, add `--skip-ssl-validation` (this is temporary).

Work with the right "org" and "space":

```bash
cf target -o foia -s hub
```

#### Two production environments

To ensure zero downtime deploys, 18F uses two production environments, `foia-a` and `foia-b`.

A new deploy pushes code to the production environment not in use, and when the deploy has been concluded, URL routes are remapped to instantly switch from one app to another.

For each environment, set the app's environment variables.

* `DATABASE_URL`: connection string to Postgres.
* `FOIA_ANALYTICS_ID`: A Google Analytics profile ID.
* `FOIA_SECRET_SESSION_KEY`: A random high-entropy string. Should be strong and unique for production.
* `DJANGO_SETTINGS_MODULE`: Set to `foia_hub.settings.dev` in development, and to `foia_hub.settings.production` in production.

```
cf set-env foia-a DATABASE_URL [value]
cf set-env foia-a FOIA_ANALYTICS_ID [value]
cf set-env foia-a FOIA_SECRET_SESSION_KEY [value]
cf set-env foia-a DJANGO_SETTINGS_MODULE foia_hub.settings.dev

cf set-env foia-b DATABASE_URL [value]
cf set-env foia-b FOIA_ANALYTICS_ID [value]
cf set-env foia-b FOIA_SECRET_SESSION_KEY [value]
cf set-env foia-b DJANGO_SETTINGS_MODULE foia_hub.settings.dev
```

Deploy the app with:

```bash
./deploy.sh
```

This will:

* Decide whether to deploy to `foia-a` or `foia-b`, based on whether `foia-a` is currently `started`.
* Deploy the app **from the directory you run the command** (the server does not check out the app from source control).
* Migrate the database.
* Check out the latest data from [`18f/foia`](https://github.com/18f/foia) and load the data into the database.
* Start the app.
* If the app successfully starts, the route will be mapped to the new environment, and the previous production environment will have its route unmapped, and then be stopped.

#### Watching the logs

You can tail the logs for a given production environment during the process with:

```bash
cf logs foia-a
```

Tailing the logs doesn't show past logs. To view recent logs (without tailing), run:

```bash
cf logs foia-a --recent
```

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
