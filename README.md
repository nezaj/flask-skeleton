## [Flask Skeleton][flask-skeleton]
Flask Skeleton provides a base structure for a medium-sized Flask app. This is my default setup for whenever I create a new Flask project. This was built and tested with Python 2.

* [Overview](#overview)
* [Installing](#installing)
* [Running](#running)
* [Tests](#tests)
* [Configuration](#configuration)

### Overview
Here's the stuff you get right off the bat:
* Asset concatenation and minification via [Flask-Assets][flask-assets]
* [Blueprints][blueprints] and [app factory][app-factory] for creating configured apps and registering routes
* Makefile with targets for virtualenv creation, cleanup, and running testing
* [Manage][flask-script] script for running the app, managing the database, and loading an interactive shell
* [pylint][pylint] and [pep8][pep8] configuration for static analysis
* [pytest][pytest] and [webtest][webtest] test examples
* Settings for managing multiple environments via [classes and inheritance][app-config]
* [SQLAlchemy][sqlalchemy] integration
* User authentication via [Flask-Login][flask-login] and [Bcrypt][flask-bcrypt]
* User email activation and password recovery

### Installing
You should build a [virtualenv][virtualenv] to contain this project's Python dependencies. The Makefile will create one for you and put it in `~/.virtualenvs/flask-skeleton`.
```
make virtualenv
```

Then activate it:
```
source ~/.virtualenvs/flask-skeleton/bin/activate
```

Instead of activating it manually like that, you might find it convenient to use [virtualenvwrapper][virtualenvwrapper] for working with virtualenvs:
```
sudo pip install virtualenvwrapper
source /usr/local/bin/virtualenvwrapper.sh
workon flask-skeleton
```

If you ever need to upgrade it or install packages which appeared since your last run, just run `make virtualenv` again.

### Running
To run the app you can simply use
```
./manage.py runserver
```

You may also specify the port and host like so:
```
./manage.py runserver --port=8080 --host=0.0.0.0  # listening on port 8080 to requests coming from any source
```

By default, the app runs using the `DevelopmentConfig` configuration defined in  the `settings` module. To point to a different configuration module, you can set the `APP_ENV` variable:
```
APP_ENV=test ./manage.py runserver
```

This will also run against the database specified in that configuration rather than the one you just set up above.

### Tests
The environment is preconfigured to contain [pep8][pep8] and [pylint][pylint], popular Python static analysis tools. [pytest][pytest] and [webtest][webtest] are also used for automated testing. You can run all the tests via `make check`

### Configuration
I need to be written!

[flask-skeleton]: http://flask-skeleton.herokuapp.com/
[flask-assets]: http://flask-assets.readthedocs.org/en/latest/
[blueprints]: http://flask.pocoo.org/docs/blueprints/
[app-factory]: http://flask.pocoo.org/docs/patterns/appfactories/
[flask-script]: http://flask-script.readthedocs.org/en/latest/
[pep8]: https://pypi.python.org/pypi/pep8
[pylint]: https://pypi.python.org/pypi/pylint
[pytest]: http://pytest.org/latest/contents.html
[webtest]: http://webtest.readthedocs.org/en/latest/
[app-config]: http://flask.pocoo.org/docs/config/#config
[sqlalchemy]: http://www.sqlalchemy.org/
[flask-login]: https://flask-login.readthedocs.org/en/latest/
[flask-bcrypt]: https://pythonhosted.org/Flask-Bcrypt/
[virtualenv]: http://docs.python-guide.org/en/latest/dev/virtualenvs/
[virtualenvwrapper]: http://virtualenvwrapper.readthedocs.org/en/latest/
