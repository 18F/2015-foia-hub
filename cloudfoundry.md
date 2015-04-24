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
````

Better instructions TBD!

## Cloud Foundry time

* Change `Procfile` to use `$VCAP_APP_PORT` instead of `$PORT`.

* Set the necessary environment variables:

```bash
cf set-env foia DATABASE_URL [value]
cf set-env foia FOIA_ANALYTICS_ID [value]
cf set-env foia FOIA_SECRET_SESSION_KEY [value]
cf set-env foia DJANGO_SETTINGS_MODULE foia_hub.settings.dev
cf set-env foia NEW_RELIC_LICENSE_KEY=[value]
cf set-env foia NEW_RELIC_APP_NAME=[value]
```

* Moved the runtime down from `3.4.2` to `3.4.0`, as that's what 18F's CF currently supports.

* Renamed app from `foia-testing` to `foia`.

* Ignored the `staticfiles/` directory.

* Re-synced the `.cfignore` and `.gitignore`.

## Custom domain

* Map a route from our app to a custom domain.

```bash
cf map-route foia open.foia.gov
```

* Setting the host value in `/etc/hosts` locally for `open.foia.gov` to the IP address used by `cf.18f.us` should then cause `http://open.foia.gov` to show the deployed app in your browser.

## Deploying

To deploy the app while also running migrations and loading in the latest data:

```bash
cf push foia -c "bash cf.sh"
```

# Staging

To deploy a staging version of the application, deploy using the staging-manifest.yml (as follows):

```bash
cf push -f ./staging-manifest.yml -c "bash cf.sh"
```

Using the staging-manifest.yml ensures that the  application name is set
correctly (and as expected).

There's also a staging.py settings file that sets up a production environment
(Debug=False in Django) but does not include any of the HTTPS related
configuration.


At 18F:

* In Cloud Foundry at 18F, the staging server is in a separate space called
'staging' than the production instance.

* There's a separate S3 bucket for staging files.

* There's a separate RDS instance.

* There is no ELB instance used by the staging instance, since we don't
* configure that with HTTPS.



