## [Flask Skeleton][flask-skeleton]
Flask Skeleton provides a base structure for a medium-sized Flask app. This incorporates several Flask best practices and is my default setup for whenever I create a new Flask project. This was built and tested with Python 2.

* [Overview](#overview)
* [Quickstart](#quickstart)
* [Installing](#installing)
* [Preparing a database](#preparing-a-database)
* [Running](#running)
* [Tests](#tests)
* [Configuration](#configuration)

### Overview
Here's the stuff you get right off the bat when using Flask-Skeleton:
* Asset concatenation and minification ([Flask-Assets][flask-assets])
* Database migrations support ([Flask-migrate][flask-Migrate])
* Functional and unit testing boilerplate with examples([pytest][pytest] and [webtest][webtest])
* Modular Flask application architecture using [Application Factories][app-factory] and [Blueprints][blueprints]
* ORM integration ([SQLAlchemy][sqlalchemy])
* Python static analysis tools ([pylint][pylint] and [pep8][pep8])
* Secure user authentication with password hashing ([Flask-Login][flask-login] and [Flask-Bcrypt][flask-bcrypt])
* User email activation and password recovery

### Quickstart
Because sometimes you just want to see it work
```
git clone git@github.com:nezaj/flask-skeleton.git
cd flask-skeleton
sudo pip install virtualenv
make virtualenv
source ~/.virtualenvs/flask-skeleton/bin/activate
./manage.py db upgrade
python -c 'import os; print "APP_KEY={}".format(os.urandom(24))' > .env  #  Generates random secret key for the app
./manage.py runserver
```

Now go to [http://localhost:5000/][localhost] in your favorite browser. Huzzah!

### Installing
You should build a [virtualenv][virtualenv] to contain this project's Python dependencies. The Makefile will create one for you and put it in `~/.virtualenvs/flask-skeleton`.
```
sudo pip install virtualenv
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

### Preparing a database
You need to pick a database to run the app against. By default, the development configuration points to a local SQLlite database `dev.db` located at the project root. You can create this database via `./manage.py db upgrade`.

### Running
Once you've installed and prepared a database you can run the app from the project root via `./manage.py runserver`

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

[alembic]: http://alembic.readthedocs.org/en/latest/
[app-config]: http://flask.pocoo.org/docs/config/#config
[app-factory]: http://flask.pocoo.org/docs/patterns/appfactories/
[blueprints]: http://flask.pocoo.org/docs/blueprints/
[flask-assets]: http://flask-assets.readthedocs.org/en/latest/
[flask-bcrypt]: https://pythonhosted.org/Flask-Bcrypt/
[flask-login]: https://flask-login.readthedocs.org/en/latest/
[flask-migrate]: http://flask-migrate.readthedocs.org/en/latest/
[flask-skeleton]: http://flask-skeleton.herokuapp.com/
[flask-script]: http://flask-script.readthedocs.org/en/latest/
[localhost]: http://localhost:5000/
[pep8]: https://pypi.python.org/pypi/pep8
[pylint]: https://pypi.python.org/pypi/pylint
[pytest]: http://pytest.org/latest/contents.html
[sqlalchemy]: http://www.sqlalchemy.org/
[virtualenv]: http://docs.python-guide.org/en/latest/dev/virtualenvs/
[virtualenvwrapper]: http://virtualenvwrapper.readthedocs.org/en/latest/
[webtest]: http://webtest.readthedocs.org/en/latest/
