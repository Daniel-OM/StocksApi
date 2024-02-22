
import os

from flask import Flask

from .views import views

basedir = os.path.abspath(os.path.dirname(__file__))

# Create App
app: Flask = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'dev-stocks'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True
app.register_blueprint(views, url_prefix='/')

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', debug=True)


    '''
    To create the database you must open the flask shell in the terminal:
    >> flask shell

    And execute the initialization
    >> from app import db, Role, Station, User, Vehicle, Tank
    >> db.create_all()

    The db.create_all() function does not recreate or update a table if it 
    already exists. For example, if you modify your model by adding a new column, 
    and run the db.create_all() function, the change you make to the model will 
    not be applied to the table if the table already exists in the database. The 
    solution is to delete all existing database tables with the db.drop_all() 
    function and then recreate them with the db.create_all() function like so:
    >> db.drop_all()
    >> db.create_all()

    To create migration file:
    >> flask db init

    To make a migration:
    >> flask db migrate -m "Initial migration."
    >> flask db upgrade 
    '''
