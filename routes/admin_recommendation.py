from flask import Blueprint
from flask import render_template
from flask import request
from flask import jsonify

from flask_login import login_required

from extensions import db

from middlewares.admin_required import admin_required

from models.user import User
from models.food import Food
from models.preference import UserPreference

from sqlalchemy import func


admin_recommendation_bp = Blueprint(
    'admin_recommendation',
    __name__
)


# =========================================
# RECOMMENDATION ENGINE PAGE
# =========================================

@admin_recommendation_bp.route(
    '/recommendation-engine'
)
@login_required
@admin_required
def recommendation_engine():

    users = User.query.filter(
        User.role != 'admin'
    ).all()

    foods = Food.query.all()

    preferences = UserPreference.query.all()

    total_users = len(users)

    total_foods = len(foods)

    total_preferences = len(preferences)

    avg_rating = db.session.query(

        func.avg(
            UserPreference.rating
        )

    ).scalar()

    if not avg_rating:
        avg_rating = 0

    # =====================================
    # TOP FOODS
    # =====================================

    top_foods = db.session.query(

        Food.food_name,
        func.avg(UserPreference.rating)

    ).join(

        UserPreference

    ).group_by(

        Food.id

    ).order_by(

        func.avg(
            UserPreference.rating
        ).desc()

    ).limit(10).all()

    return render_template(

        'admin_recommendation.html',

        users=users,

        foods=foods,

        preferences=preferences,

        total_users=total_users,

        total_foods=total_foods,

        total_preferences=total_preferences,

        avg_rating=round(avg_rating, 1),

        top_foods=top_foods

    )