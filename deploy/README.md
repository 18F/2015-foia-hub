## foia.18f.us deployment details

Quick file overview:

* [`hub.conf`](hub.conf) - Our nginx config for the staging site. Not synced to version control automatically, but we'll try to keep them in sync.
* [`fabfile.py`](fabfile.py) - Fabric deployment script to start/stop/restart our webhook processes.
* [`hookshot.js`](hookshot.js) - Tiny webhook app, runs a command when a branch is updated. Uses [`hookshot`](https://github.com/coreh/hookshot) to do the heavy lifting. Daemonized on our server using [`forever`](https://github.com/nodejitsu/forever).

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

#### Setting it up yourself

These instructions can be applied locally (for development) or on the server (for deployment).

Install the Node dependencies with:

```bash
npm install hookshot
npm install minimist
npm install -g forever
```

The FOIA staging server uses the `hookshot` command to listen for hooks.

From `/deploy`, run the hook with the appropriate port and command. It can be helpful to have `forever` and your command both log to the same file.

In development, you might use:

```bash
forever start -l $HOME/hookshot.log -a deploy/hookshot.js -p 3000 -b your-branch -c "cd $HOME/foia/hub && git pull && jekyll build >> $HOME/hookshot.log"
```

You can stop and restart your hooks by supplying the same arguments you gave.

```bash
forever stop deploy/hookshot.js -p 3000 -b your-branch -c "cd $HOME/18f/18f.gsa.gov && git pull && jekyll build >> $HOME/hookshot.log"
forever restart deploy/hookshot.js -p 3000 -b your-branch -c "cd $HOME/foia/hub && git pull && jekyll build >> $HOME/hookshot.log"
```

You may wish to use [ngrok](https://ngrok.com/) or [localtunnel](https://localtunnel.me/) in development to test out the webhook.

