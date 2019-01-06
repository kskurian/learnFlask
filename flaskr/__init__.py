import os

from . import db
from . import auth
from . import blog
from .resources import restBlog

from flask import Flask
from flask_restful import Resource, Api


# create and configure the app
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    api = Api(restBlog.api_bp)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE = os.path.join(app.instance_path,'flask.sqlite')
    )

    if test_config is None :
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_pyfile(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello,World!'
    api.add_resource(restBlog.simpleBlog, '/rest/blog/<int:blog_id>')

    # from our own package the db is imported and the function is called to setup
    db.init_app(app)
    # The app is registered with a blue print
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(restBlog.api_bp)

    app.add_url_rule('/', endpoint='index')

    return app
#set FLASK_APP=flaskr
#set FLASK_ENV=development
#flask run
#http://127.0.0.1:5000/hello