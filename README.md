## [Flask Skeleton][flask-skeleton]
Flask Skeleton provides a base structure for a medium-sized Flask app. This incorporates several Flask best practices and is my default setup for whenever I create a new Flask project. This was built and tested with Python 2.

Here's the stuff you get right off the bat when using Flask-Skeleton:
* Asset concatenation and minification ([Alembic][alembic] and [Flask-Assets][flask-assets])
* Database migrations support ([Flask-Migrate][flask-Migrate])
* Functional and unit testing boilerplate with examples ([pytest][pytest] and [webtest][webtest])
* Modular Flask application architecture using [Application Factories][app-factory] and [Blueprints][blueprints]
* ORM integration ([SQLAlchemy][sqlalchemy])
* Python static analysis tools ([pylint][pylint] and [pep8][pep8])
* Secure user authentication with password hashing ([Flask-Login][flask-login] and [Flask-Bcrypt][flask-bcrypt])
* User email activation and password recovery

## Table of contents
* [Quickstart](#quickstart)
* [Installing](#installing)
* [Preparing a database](#preparing-a-database)
* [Environment variables](#environment-variables)
* [Running](#running)
* [Tests](#tests)
* [Migrations](#migrations)
* [Additional configuration](#additional-configuration)

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
You need to pick a database to run the app against. By default, the development configuration points to a local SQLlite database `dev.db` located at the top level directory. Run the following to create the database
```
./manage.py db upgrade
```

### Environment variables
Most of the app configuration is defined in the `settings` module. However, some necessary but sensitive configuration settings like secret keys, emails, and production database URIs are not (and should not) be part of source control. Instead, we import these settings from another file and create environment variables at runtime. Flask Skeleton will look for key-value pairs (in the form of `KEY=VALUE`) defined in the `.env` file at the top level directory. The `.env` file should not be part of source control and included in our `.gitignore`.

At a minimum, we must define an `APP_KEY` variable which will be used as the [secret key][secret-key] for signing cookies in our application. We can create the `.env` file and a random value for `APP_KEY` in one go
```
python -c 'import os; print "APP_KEY={}".format(os.urandom(24))' > .env
```

To specify additional key-value pairs, add them on separate lines in your newly generated `.env` file. These will be imported whenever you run a `./manage` command.

### Running
Once you've installed all the dependencies, prepared a database, and configured your environment variables you're ready to run the app.
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

### Migrations
We use [alembic][alembic] and [flask-migrate][flask-migrate] for keeping a revision history of database schemas. You can see the history at any time:
```
./manage.py db history
```

Common operations available are:
```
# ensures that the current database is up-to-date
./manage.py db upgrade

# rolls back the database to the previous revision
./manage.py db downgrade
```

These are thin wrappers around the underlying `alembic` commands. For a full list of commands
```
./manage.py db --help
```

If you make changes to the schema, you'll want to generate a new Alembic revision.
```
./manage.py db migrate -m "Short description of your change"
```

This will create a new revision file in the migrations directory with upgrade and downgrade scripts. You should inspect it for accuracy. Type `./manage.py db upgrade` to test it out. If all seems good, then commit the alembic revision to git with your schema changes. To run the upgrade on your production database
```
APP_ENV=prod ./manage.py db upgrade`
```

### Additional configuration
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
[secret-key]: http://flask.pocoo.org/docs/quickstart/#sessions
[sqlalchemy]: http://www.sqlalchemy.org/
[virtualenv]: http://docs.python-guide.org/en/latest/dev/virtualenvs/
[virtualenvwrapper]: http://virtualenvwrapper.readthedocs.org/en/latest/
[webtest]: http://webtest.readthedocs.org/en/latest/
