# routes/favorites.py

from flask import Blueprint
from flask import render_template

from flask_login import login_required
from flask_login import current_user

from models.food import Food
from models.preference import UserPreference


favorites_bp = Blueprint(
    'favorites',
    __name__
)


# =========================================
# FAVORITES PAGE
# =========================================

@favorites_bp.route('/favorites')
@login_required
def favorites():

    # =====================================
    # GET FAVORITED FOODS
    # =====================================

    favorite_preferences = UserPreference.query.filter(

        UserPreference.user_id == current_user.id,
        UserPreference.rating >= 4

    ).all()

    favorite_food_ids = [

        pref.food_id

        for pref in favorite_preferences

    ]

    # =====================================
    # GET FOODS
    # =====================================

    favorite_foods = Food.query.filter(

        Food.id.in_(favorite_food_ids)

    ).all()

    return render_template(

        'favorites.html',

        user=current_user,

        favorite_foods=favorite_foods

    )