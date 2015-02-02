## foia.18f.us deployment details

Quick file overview:

* [`hub.conf`](hub.conf) - Our nginx config for the staging site. Not synced to version control automatically, but we'll try to keep them in sync.
* [`fabfile.py`](fabfile.py) - Fabric deployment script to start/stop/restart our webhook processes.
* [`hookshot.js`](hookshot.js) - Tiny webhook app, runs a command when a branch is updated. Uses [`hookshot`](https://github.com/coreh/hookshot) to do the heavy lifting. Daemonized on our server using [`forever`](https://github.com/nodejitsu/forever).
* [`bin/deploy-site.sh`](bin/deploy-site.sh) - The script run by the webhook every time a commit is pushed to `master`.

### Automatic deployment

On the staging server, this project uses [Node](http://nodejs.org) and [`hookshot`](https://github.com/coreh/hookshot) to receive GitHub post-receive webhooks and update the project.

Ideally, these webhooks just run forever and never need to be maintained!

But just in case, this project includes [fabric tasks](http://www.fabfile.org/) for easy remote stop/start/restart of the hook processes on the FOIA web server.

The fabric tasks can start, stop, and restart the staging hook like so:

```
fab stop
fab start
fab restart
```

They expect a hostname called `foia` in your `$HOME/.ssh/config`.

#### Setting it up yourself

These instructions can be applied locally (for development) or on the server (for deployment).

Install the Node dependencies with:

```bash
npm install
npm install -g forever
```

The FOIA staging server uses the `hookshot` command to listen for hooks.

From `/deploy`, run the hook with the appropriate port and command. It can be helpful to have `forever` and your command both log to the same file.

In development, you might use:

```bash
forever start -l $HOME/hookshot.log -a deploy/hookshot.js -p 3000 -b your-branch -c "cd $HOME/foia/hub && git pull && jekyll build >> $HOME/hookshot.log"
```

You can stop and restart your hooks by supplying the same arguments you gave.

You may wish to use [ngrok](https://ngrok.com/) or [localtunnel](https://localtunnel.me/) in development to test out the webhook.

### Staging server

On the staging server, this hookshot daemon is run:

```
forever start -l $HOME/hub/shared/log/hookshot.log -a deploy/hookshot.js -p 3000 -b master -c "bash $HOME/hub/current/deploy/bin/deploy-site.sh >> $HOME/hub/shared/log/hookshot.log"
```

It should be run from the project root (the `current` dir/symlink). Both the hook and the output log to the same file, and when it's hit it will execute a small bash script:

```bash
#!/bin/bash

source /home/foia/.bashrc
cd /home/foia/hub/current
workon fab
fab -H localhost deploy
```

This loads in the `foia` user's environment, navigates to the project root, activates the Fabric (Python 2.x) virtualenv, `fab`, and then runs the deploy script against itself.

Fabric is able to deploy to itself because the `foia` user's public key is also on the `foia` user's `.ssh/authorized_keys` list. It has been previously authorized as a known host and should run without warnings.

