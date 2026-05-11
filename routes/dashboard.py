from flask import Blueprint
from flask import render_template
from flask import redirect

from flask_login import login_required
from flask_login import current_user

from models.food import Food
from models.preference import UserPreference


# =========================================
# BLUEPRINT
# =========================================

dashboard_bp = Blueprint(
    'dashboard',
    __name__
)


# =========================================
# USER DASHBOARD
# =========================================

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():

    # =====================================
    # FORCE PROFILE
    # =====================================

    if not current_user.profile_completed:

        return redirect('/profile')

    # =====================================
    # USER RATINGS
    # =====================================

    preferences = UserPreference.query.filter_by(
        user_id=current_user.id
    ).all()

    ratings = {}

    rated_food_ids = []

    for pref in preferences:

        ratings[pref.food_id] = pref.rating

        rated_food_ids.append(
            pref.food_id
        )

    total_ratings = len(
        rated_food_ids
    )

    # =====================================
    # AI STATUS
    # =====================================

    ai_ready = total_ratings >= 10

    # =====================================
    # FOODS
    # =====================================

    if ai_ready:

        foods = Food.query.limit(12).all()

    else:

        foods = Food.query.filter(

            ~Food.id.in_(rated_food_ids)

        ).limit(10).all()

    # =====================================
    # PROGRESS BAR
    # =====================================

    progress_width = min(

        (total_ratings / 10) * 100,

        100

    )

    # =====================================
    # RENDER
    # =====================================

    return render_template(

        'user_dashboard.html',

        foods=foods,

        ratings=ratings,

        total_ratings=total_ratings,

        ai_ready=ai_ready,

        progress_width=progress_width

    )