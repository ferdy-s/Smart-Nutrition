import os

# =========================================
# OAUTH LOCAL DEVELOPMENT
# =========================================

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask import Flask

from config import Config

from extensions import db
from extensions import login_manager
from extensions import socketio

from flask_dance.contrib.google import make_google_blueprint

from models.user import User
from models.food import Food
from models.preference import UserPreference
from models.recommendation_history import RecommendationHistory

from routes.auth import auth_bp
from routes.foods import foods_bp
from routes.nutrition import nutrition_bp
from routes.favorites import favorites_bp
from routes.profile import profile_bp
from routes.admin_foods import admin_foods_bp
from routes.admin_athletes import admin_athletes_bp
from routes.admin_recommendation import admin_recommendation_bp
from routes.dashboard import dashboard_bp
from routes.admin_analytics import admin_analytics_bp


# =========================================
# CREATE APP
# =========================================

app = Flask(__name__)

app.config.from_object(Config)


# =========================================
# INIT DATABASE
# =========================================

db.init_app(app)


# =========================================
# INIT LOGIN MANAGER
# =========================================

login_manager.init_app(app)

login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


# =========================================
# SOCKET.IO INIT
# =========================================

socketio.init_app(app)


# =========================================
# GOOGLE OAUTH
# =========================================

google_bp = make_google_blueprint(

    client_id=app.config[
        'GOOGLE_OAUTH_CLIENT_ID'
    ],

    client_secret=app.config[
        'GOOGLE_OAUTH_CLIENT_SECRET'
    ],

    reprompt_consent=True,

    scope=[

        "openid",

        "https://www.googleapis.com/auth/userinfo.email",

        "https://www.googleapis.com/auth/userinfo.profile"

    ]

)

app.register_blueprint(

    google_bp,

    url_prefix="/login"

)


# =========================================
# REGISTER BLUEPRINTS
# =========================================

app.register_blueprint(
    dashboard_bp
)

app.register_blueprint(
    admin_analytics_bp
)

app.register_blueprint(auth_bp)

app.register_blueprint(foods_bp)

app.register_blueprint(nutrition_bp)

app.register_blueprint(favorites_bp)

app.register_blueprint(profile_bp)

app.register_blueprint(admin_foods_bp)

app.register_blueprint(admin_athletes_bp)

app.register_blueprint(admin_recommendation_bp)






# =========================================
# CREATE TABLES
# =========================================

with app.app_context():

    db.create_all()


# =========================================
# RUN APP
# =========================================

if __name__ == '__main__':

    socketio.run(

        app,

        debug=True,

        allow_unsafe_werkzeug=True

    )