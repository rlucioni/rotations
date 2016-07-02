# rotations

Django app for managing rotations.

## Getting Started

This app uses Docker and Heroku's [container tools plugin](https://github.com/heroku/heroku-container-tools) to facilitate local development and deployment to Heroku. Working, local installations of Docker and Docker Compose are required.

Set up Docker locally by installing the [Docker Toolbox](https://www.docker.com/products/docker-toolbox). Once installed and if you're running OS X locally, open a shell using the Docker Quickstart Terminal app. This will create a `default` [Docker Machine](https://docs.docker.com/machine/overview/) instance. Verify that you have a working Docker installation by running:

```
$ docker run hello-world
```

You should see output confirming a working installation. If you don't, refer to Docker's [Troubleshooting](https://docs.docker.com/v1.10/faqs/troubleshoot/) docs for help. If you're using Docker Machine, make a note of the active machine's IP address. You'll need it to access the app in a browser.

```
$ docker-machine ip
192.168.99.100
```

Install the [Heroku Toolbelt](https://toolbelt.heroku.com/) if you haven't already, then install the container tools plugin:

```
$ heroku plugins:install heroku-container-tools
```

Now you're ready to clone the code:

```
$ git clone git@github.com:rlucioni/rotations.git
$ cd rotations
```

Start the app as follows:

```
$ docker-compose up web
```

The app should now be running locally. Verify by visiting `http://192.168.99.100:8080/` in a browser. Django's `DEBUG` setting is disabled by default, so you should expect a 404.

Now run migrations, collect static files in `STATIC_ROOT`, and create a superuser:

```
$ docker-compose run shell
root@8ca7213f28c4:/app/user# python manage.py migrate
root@8ca7213f28c4:/app/user# python manage.py collectstatic
root@8ca7213f28c4:/app/user# python manage.py createsuperuser
```

Since you've just made changes to the app (collecting static files), rebuild your containers:

```
$ docker-compose build
```

You should now be able to access the Django admin by starting the app again and visiting `http://192.168.99.100:8080/admin`.

See Heroku's docs on [local development with Docker](https://devcenter.heroku.com/articles/local-development-with-docker) for more information.
