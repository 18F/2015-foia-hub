import time
from fabric.api import run, execute, env

# which settings file to use in production
environment = "production"

# depends on virtualenvwrapper with a named virtualenv to `workon`
virtualenv = "foia"

# name of WSGI wrapper for gunicorn to work with
wsgi = "foia_hub.wsgi:application"

# use `-H foia` or something to control where fabric runs
env.use_ssh_config = True

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

# always UTC datestamp, so it doesn't matter what computer does the deploy
datestamp = time.strftime("%Y%m%d%H%M%S", time.gmtime(time.mktime(time.localtime())))

home = "/home/foia/hub"
shared_path = "%s/shared" % home
versions_path = "%s/versions" % home
version_path = "%s/%s" % (versions_path, datestamp)
current_path = "%s/current" % home
logs = "%s/log" % shared_path
env = "%s/foia-env" % shared_path

# keep the last 5 deployed versions on disk
keep = 5


def checkout():
    run('git clone -q -b %s %s %s' % (branch, repo, version_path))

def dependencies():
    run('workon %s && cd %s && pip install -r requirements.txt' % (virtualenv, version_path))
    run('cd %s/deploy && npm install' % version_path)

def migrate():
    run('workon %s && source %s && cd %s && python manage.py migrate' % (virtualenv, env, version_path))

def make_current():
    run('rm -f %s && ln -s %s %s' % (current_path, version_path, current_path))

def cleanup():
    versions = run("ls -x %s" % versions_path).split()
    destroy = versions[:-keep]

    for version in destroy:
        command = "rm -rf %s/%s" % (versions_path, version)
        run(command)


# can be run on their own

def start():
    """
    Gunicorn start.
    """

    run(
        (
            "workon %s && source %s && " +
            "cd %s && " +
            "gunicorn -c %s/config.py %s"
        ) % (virtualenv, env, current_path, shared_path, wsgi), pty=False
    )

# config.py is expected to point the .pid to the shared/ dir
def stop():
    run("kill `cat %s/gunicorn.pid`" % shared_path)

def restart():
    run("kill -HUP `cat %s/gunicorn.pid`" % shared_path)

def deploy():
    """
    Usual deploy script. Expects app to be running.
    Checks out code, makes symlinks, installs dependencies,
    restarts app, cleans up old deploys.
    """
    execute(checkout)
    execute(dependencies)
    execute(migrate)
    execute(make_current)
    execute(restart)
    execute(cleanup)

def deploy_cold():
    """
    Similar to normal deploy, but expects the app to be stopped.
    Doesn't bother doing cleanup.
    """
    execute(checkout)
    execute(dependencies)
    execute(migrate)
    execute(make_current)
    execute(start)

def test():
    run("uname -a")
