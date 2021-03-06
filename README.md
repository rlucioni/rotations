# rotations [![Build Status](https://img.shields.io/travis/rlucioni/rotations.svg?style=flat-square&maxAge=60)](https://travis-ci.org/rlucioni/rotations)

Django app for managing rotations.

## Overview

This app uses Docker and Heroku's [container tools plugin](https://github.com/heroku/heroku-container-tools) to facilitate local development and deployment to Heroku. Working, local installations of Docker and Docker Compose are required.

Complete instructions for development and deployment are below, adapted from Heroku's docs on [local development with Docker](https://devcenter.heroku.com/articles/local-development-with-docker).

## Getting Started

### Docker

Set up Docker locally by installing the [Docker Toolbox](https://www.docker.com/products/docker-toolbox). If you require a Docker Machine VM (e.g., you're on OS X), start and connect your shell to the VM using:

```
$ make connect
```

This will create a `default` [Docker Machine](https://docs.docker.com/machine/overview/) instance. Make a note of the active machine's IP address. You'll need it to access the app in a browser.

Verify that you have a working Docker installation by running:

```
$ docker run hello-world
```

You should see output confirming a working installation. If you don't, refer to Docker's [Troubleshooting](https://docs.docker.com/v1.10/faqs/troubleshoot/) docs for help.

### Heroku Toolbelt

Install the [Heroku Toolbelt](https://toolbelt.heroku.com/) if you haven't already, then install the container tools plugin:

```
$ heroku plugins:install heroku-container-tools
```

### Development

Now you're ready to clone the code:

```
$ git clone git@github.com:rlucioni/rotations.git
$ cd rotations
```

Start the app as follows:

```
$ make up
```

The app should now be running locally. Verify by visiting `http://<Docker Machine IP>:8080/` in a browser. Django's `DEBUG` setting is disabled by default, so you should expect a 404.

Now run migrations, create a superuser, and collect static files in `STATIC_ROOT`.

```
$ make shell
root@8ca7213f28c4:/app/user# python manage.py migrate
root@8ca7213f28c4:/app/user# python manage.py createsuperuser
root@8ca7213f28c4:/app/user# python manage.py collectstatic
root@8ca7213f28c4:/app/user# exit
```

You should now be able to access the Django admin by starting the app again and visiting `http://<Docker Machine IP>:8080/admin`.

Run the tests with:

```
$ make test
```

Run code style checks with:

```
$ make quality
```

If you introduce new dependencies (i.e., by adding to `requirements.py`), install them by rebuilding the service:

```
$ make build
```

As you work, you'll leave a trail of exited containers and dangling images behind you. To clean these up, run:

```
$ make clean
```

## Deployment

### Initial Deployment

Deploy the app using the Heroku Toolbelt. Create a new Heroku app:

```
$ heroku create
```

Then deploy a Heroku-compatible slug:

```
$ make deploy
```

Run migrations using a one-off dyno. You'll also want to create a superuser.

```
$ heroku run bash
~ $ cd user/
~/user $ python manage.py migrate
~/user $ python manage.py createsuperuser
~/user $ exit
```

Export environment variables:

```
$ heroku config:set ROTATIONS_SECRET_KEY=<secret>
$ heroku config:set WEB_CONCURRENCY=2
```

Ensure that at least one instance of the app is running:

```
$ heroku ps:scale web=1
```

Verify deployment by visiting the admin:

```
$ heroku open /admin
```

#### Heroku Add-ons

To allow the app to send email, provision Heroku's [SendGrid add-on](https://devcenter.heroku.com/articles/sendgrid>). This will export the `SENDGRID_USERNAME` and `SENDGRID_PASSWORD` environment variables expected by the app.

```
$ heroku addons:create sendgrid:starter
```

Use the Heroku [Scheduler add-on](https://devcenter.heroku.com/articles/scheduler) to schedule reminder emails:

```
$ heroku addons:create scheduler:standard
$ heroku addons:open scheduler
```

### Subsequent Deployments

Subsequent deployments are simple. Just rebuild your containers and deploy a Heroku-compatible slug:

```
$ make deploy
```

Run migrations if necessary:

```
$ heroku run bash
~ $ cd user/
~/user $ python manage.py migrate
~/user $ exit
```

Heroku's traditional Git-based deployment (e.g., to deploy when a commit is merged to master on GitHub) is also supported. Note that when the app is deployed this way, source code will be mounted under `/app` instead of under `/app/user`.
