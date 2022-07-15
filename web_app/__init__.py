import os

from flask import Flask, render_template, request, redirect, url_for

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.config.from_pyfile('config.py', silent=True)

    from . import views
    app.register_blueprint(views.bp)
    app.add_url_rule('/', endpoint='home')

    return app