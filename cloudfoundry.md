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
