# Papillon

**WIP**

Basic image pasting Django-powered website, with encrypted on-disk images.

## Install

To install Papillon, first clone this repository wherever you want, then,

* install a virtual environment:

    ```bash
    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

* copy the default local settings file:

    ```bash
    cp papillon/settings_local{.default,}.py
    ```

* edit this file to match what you actually want. Don't forget to edit the
  `SECRET_KEY`! You can generate one with, eg., `pwgen 60 1`

* initialize the database:

    ```bash
    ./manage.py migrate
    ```

* serve the application through your favorite WSGI server and web server, eg.
  `gunicorn` and `nginx`, and keep the wsgi server running using eg. a
  `systemd` service.
