from flask import Flask

def create_app(): #create flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sefjshsbfhjdfsjbjfb' #make s secret key

    from .views import views #import view for blueprint 

    #register blueprint
    app.register_blueprint(views, url_prefix='/') #register blueprint

    return app


