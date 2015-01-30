
from fabric.api import run, env

"""
Manage auto-deploy webhooks remotely.

Staging hook:

  forever start -l $HOME/hub/shared/log/hookshot.log -a $HOME/hub/current/deploy/hookshot.js -p 3000 -b master -c "bash $HOME/hub/current/deploy/bin/deploy-site.sh >> $HOME/hub/shared/log/hookshot.log"
  forever restart $HOME/hub/current/deploy/hookshot.js -p 3000 -b master -c "bash $HOME/hub/current/deploy/bin/deploy-site.sh >> $HOME/hub/shared/log/hookshot.log"
  forever stop $HOME/hub/current/deploy/hookshot.js -p 3000 -b master -c "bash $HOME/hub/current/deploy/bin/deploy-site.sh >> $HOME/hub/shared/log/hookshot.log"
"""

environment = env.get('env', 'staging')

port = {
    "staging": 3000
}[environment]

env.use_ssh_config = True

home = "/home/foia"
shared = "%s/hub/shared" % home
current = "%s/hub/current" % home
log = "%s/log/hookshot.log" % shared

# principal command to run when the main branch is updated
branch = "master"
command = "bash %s/deploy/bin/deploy-site.sh >> %s" % (current, log)


# needs to be run out of $HOME, because this will run as a daemon across deploys
def start():
    run(
        "cd %s && forever start -l %s -a %s/deploy/hookshot.js -p %i -b %s -c \"%s\""
        % (home, log, current, port, branch, command)
    )

def stop():
    run(
        "cd %s && forever stop %s/deploy/hookshot.js -p %i -b %s -c \"%s\""
        % (home, current, port, branch, command)
    )

def restart():
    run(
        "cd %s && forever restart %s/deploy/hookshot.js -p %i -b %s -c \"%s\""
        % (home, current, port, branch, command)
    )
