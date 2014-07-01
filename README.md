## [Flask Skeleton][flask-skeleton]
Flask Skeleton provides a base structure for a medium-sized Flask app. This is my default setup for whenever I create a new Flask project. This was built and tested with Python 2.

* [Overview](#overview)
* [Getting Started](#getting-started)
* [Configuration](#configuration)

### Overview
Here's a bunch of stuff you get right off the bat:
* A nifty directory structure
* Makefile for virtualenv creation, project cleanup, and testing
* [pylint][pylint-docs] and [pep8][pep8-docs] configuration
* App creation via [factory pattern][app-factory]
* App configuration via [classes and inheritance][app-config]
* Asset concatenation/minification via [Flask-Assets][flask-assets]
* [SQLAlchemy][sqlalchemy] setup and db connection
* Console utilities for database and project models (`sql.py` and `console.py`)

### Getting Started
Before trying to make a [virtualenv][venv-docs], you should make sure that Python 2.7 is your system's default Python, and that [pip][pip-docs] is a Python 2 version of pip. (If that's not the case, you should uninstall and reinstall pip -- see the install directions on its [website][pip-docs].)
```
$ python --version
Python 2.7.3
$ pip --version
pip 1.1 from ~/.virtualenvs/rads/lib/python2.7/site-packages/pip-1.1-py2.7.egg (python 2.7)
```
Next you should build a [virtualenv][venv-docs] to contain this project's Python dependencies. The Makefile will create one for you and put it in `~/.virtualenvs/flask-skeleton`. If you get strange errors during this step, check that you don't have Python 3 `python`, `pip`, or `virtualenv` in your `PATH`.
```
sudo pip install virtualenv
make virtualenv
```
Then activate it:
```
source ~/.virtualenvs/flask-skeleton/bin/activate
```
Instead of activating it manually like that, you might find it convenient to use [virtualenvwrapper][venv-wrapper-docs] for working with virtualenvs (recommended):
```
sudo pip install virtualenvwrapper
source /usr/local/bin/virtualenvwrapper.sh
workon flask-skeleton
```
If you ever need to upgrade it or install packages which appeared since your last run, just run `make virtualenv` again.

You should now be able to start up a Flask server using `run.py`. Flask will bind to a socket listening to localhost on port 5000. If you want to run on a different port or access the web server from another host, use the `--port` and `--host` configuration options.
```
./run.py --port=8080 --host=0.0.0.0  # listening on port 8080 to requests coming from any source
```

### Configuration
I need to be written!

[flask-skeleton]: http://flask-skeleton.herokuapp.com/
[pylint-docs]: http://docs.pylint.org/intro.html
[pep8-docs]: http://legacy.python.org/dev/peps/pep-0008/#introduction
[app-factory]: http://flask.pocoo.org/docs/patterns/appfactories/
[app-config]: http://flask.pocoo.org/docs/config/#config
[flask-assets]: http://flask-assets.readthedocs.org/en/latest/
[sqlalchemy]: http://www.sqlalchemy.org/

[venv-docs]: http://docs.python-guide.org/en/latest/dev/virtualenvs/
[pip-docs]: http://pip.readthedocs.org/
[venv-wrapper-docs]: http://virtualenvwrapper.readthedocs.org/en/latest/
