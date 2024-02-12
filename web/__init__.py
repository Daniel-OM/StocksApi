
import os

from flask import Flask



def create_app():
    
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # )
    app.config['SECRET_KEY'] = 'dev-stocks'

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app