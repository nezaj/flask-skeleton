from flask_assets import Environment, Bundle

CSS_ASSETS = [
    'css/vendor/bootstrap.css',
    Bundle('css/application.scss', filters='pyscss', output='css/compiled-scss.css')
]

def register_assets(app):
    assets = Environment(app)
    assets.debug = app.debug
    assets.auto_build = True
    assets.url = app.static_url_path

    css = Bundle(*CSS_ASSETS, filters='cssmin', output='css/bundle.min.css')

    assets.register('css_all', css)
    app.logger.info("Registered assets...")
    return assets
