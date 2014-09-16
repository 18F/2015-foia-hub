import time
from fabric.api import run, execute, env

# which settings file to use in production
environment = "production"

# depends on virtualenvwrapper with a named virtualenv to `workon`
virtualenv = "foia"

# name of WSGI wrapper for gunicorn to work with
wsgi = "foia_hub.wsgi:application"

# expects an SSH entry named 'foia-hub', rather than hardcoded server details
env.use_ssh_config = True
env.hosts = ["foia"]

# using master branch for now, we could change this
branch = "master"
repo = "git@github.com:18f/foia-hub.git"

# base directory structure -
#   current/
#   versions/
#      20140914123412/
#      ...
#   shared/
#      log/
#      settings.py
home = "/home/foia/hub"
shared_path = "%s/shared" % home
versions_path = "%s/versions" % home
version_path = "%s/%s" % (versions_path, time.strftime("%Y%m%d%H%M%S"))
current_path = "%s/current" % home
logs = "%s/log" % shared_path

# keep the last 5 deployed versions on disk
keep = 5


def checkout():
  run('git clone -q -b %s %s %s' % (branch, repo, version_path))

def dependencies():
  run('workon %s && cd %s && pip install -r requirements.txt' % (virtualenv, version_path))

def make_current():
  run('rm -f %s && ln -s %s %s' % (current_path, version_path, current_path))

def cleanup():
  versions = run("ls -x %s" % versions_path).split()
  destroy = versions[:-keep]

  for version in destroy:
    command = "rm -rf %s/%s" % (versions_path, version)
    run(command)

def links():
  run("ln -s %s/config.py %s/deploy/config.py" % (shared_path, version_path))
  run("ln -s %s/local_settings.py %s/foia_hub/settings/local_settings.py" % (shared_path, version_path))


## can be run on their own

def start():
  """
  Run gunicorn:
    * with production settings,
    * with project root in the PYTHONPATH,
    * expecting the gunicorn config in deploy/config.py,
    * with our wsgi application module.
  """

  run(("workon %s && DJANGO_SETTINGS_MODULE=foia_hub.settings.%s " +
    "PYTHONPATH=%s:$PYTHONPATH " +
    "gunicorn -c %s/deploy/config.py %s") %
    (virtualenv, environment, current_path, current_path, wsgi), pty=False
  )

# config.py is expected to point the .pid to the shared/ dir
def stop():
  run("kill `cat %s/gunicorn.pid`" % shared_path)

def restart():
  run("kill -HUP `cat %s/gunicorn.pid`" % shared_path)

def deploy():
  execute(checkout)
  execute(links)
  execute(dependencies)
  execute(make_current)
  execute(restart)
  execute(cleanup)

def deploy_cold():
  execute(checkout)
  execute(links)
  execute(dependencies)
  execute(make_current)
  execute(start)

def testing():
  run("workon foia && which gunicorn")
