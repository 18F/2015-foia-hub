# Deploying to Cloud Foundry

This covers Cloud Foundry specific instructions, and TODOs.

- [X] moving config to environment variables
- [ ] running via foreman
- [ ] Deployed to Heroku
- [ ] Deployed to Cloudfront


## waitress

* `waitress` added to `requirements.txt`.

```bash
pip install -r requirements.txt
```

* Run with waitress directly:

```bash
waitress-serve --port=8000 foia_hub.wsgi:application
```

* Make a `Procfile` that will work with CloudFoundry's port:

```bash
web: waitress-serve --port=$VCAP_APP_PORT foia_hub.wsgi:application
```

* Add `VCAP_APP_PORT` to `.env` and `env.example`.

* Run with foreman:

```bash
foreman start
```

## dj-database-url

* Install `dj-database-url`.
* Rework `local_settings.py` to use a database string instead of a whole dict.

## Specify runtime

* Add a `runtime.txt` with `python-3.4.2`.


## On heroku

* Create a Heroku app.

```bash
heroku apps:create foia-testing-18f
```

* Install the Postgres addon.

```bash
heroku addons:add heroku-postgresql:hobby-dev
```

* Grab the Postgres connection string from the Heroku config.

```bash
heroku config
```

* Add the Postgres connection string to `.env`.

* Send environment variables to the app, overwriting any that are there.

```bash
heroku config:push -o
```

* Deploy the app.

```bash
git push heroku master
```

If using a non-`master` branch, like `cloudfoundry`:

```bash
git push heroku cloudfoundry:master
```

* Migrate the database.

```bash
heroku run python manage.py migrate
```

## Moving AWS to use Heroku-style deployment

* Moved some old settings file into `shared/old`.
* Made a new `shared/log` dir and restarted nginx to kick off nginx log files again.
* Updated fabfile with a first pass at new approach.
* Renamed `env` to `foia-env`, since `env` is a system command.
* Removed `links` method in `fabfile.py`, since we don't need unversioned files anymore.
* **Important**: the `$PYTHONPATH` variable should _not_ be set. If it is set, it interferes in non-obvious ways to make the server not see env variables and not start.
* Sourced environment variables for the `migrate` step in the fabfile.
* Temporarily add `$PORT` to the env file as well, since the `Procfile` uses `$PORT`.
* Change the `start` command to use `nohup foreman start &`.
* Change the `stop` command to just `killall waitress-server`

Status:

* `fab deploy` will stay hanging, but successfully daemonize the app.
* The webhook is down.

## Load the data

Right now, load it *locally* from your laptop, with a connection string pointed at the production DB:

```bash
./manage.py load_agency_contacts /path/to/foia/contacts/data

Better instructions TBD!

## Cloud Foundry time

* Change `Procfile` to use `$VCAP_APP_PORT` instead of `$PORT`.
* Create the Postgresql service:

```bash
cf create-service postgresql default foia-db
```

* Bind the postgresql service to the app:

```
cf bind-service foia-testing foia-db
```

* Grab the database URL from the env. It's in `VCAP_SERVICES.postgresql-9.3.credentials.uri`.

```
cf env foia-testing
```

* Set the `DATABASE_URL` to that URL.

```
cf set-env foia-testing [url]
```

* Set the remaining environment variables, one by one.

```
cf set-env foia-testing FOIA_ANALYTICS_ID [value]
cf set-env foia-testing FOIA_SECRET_SESSION_KEY [value]
cf set-env foia-testing DJANGO_SETTINGS_MODULE foia_hub.settings.dev
```
