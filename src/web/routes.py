"""
Registers all routes served by the web app.
"""

def register_endpoints(app):
    "Configures the given app to serve all of our web app endpoints."
    # it's long on purpose, so set pylint not to complain
    # pylint:disable=R0915

    def route(url, view_func, **kwargs):
        """
        Defines a route to the given URL. Like add_url_rule, but sets the
        Flask endpoint name to the scoped identifier of the view_func
        in its module, e.g. "auth.login."
        """
        module = view_func.__module__.split('.')[-1]
        endpoint = "{}.{}".format(module, view_func.__name__)
        return app.add_url_rule(url, endpoint, view_func, **kwargs)

    from web.views import services
    route('/health', services.health, methods=['GET'])

    from web.views import dashboard
    route('/', dashboard.hello, methods=['GET'])
