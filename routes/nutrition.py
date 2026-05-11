# routes/nutrition.py

from flask import Blueprint
from flask import render_template

from flask_login import login_required
from flask_login import current_user

from services.recommendation import get_recommendations

nutrition_bp = Blueprint(
    'nutrition',
    __name__
)


# =========================================
# GENERATE DYNAMIC NUTRITION PLAN
# =========================================

def generate_nutrition_plan(user):

    # =========================================
    # DAILY TARGET
    # =========================================

    daily_calories = int(
        user.daily_calories or 2500
    )

    breakfast_target = int(
        daily_calories * 0.25
    )

    lunch_target = int(
        daily_calories * 0.35
    )

    dinner_target = int(
        daily_calories * 0.25
    )

    snack_target = int(
        daily_calories * 0.15
    )

    # =========================================
    # GET AI RECOMMENDATIONS
    # =========================================

    recommended_foods = get_recommendations(
        user.id,
        top_n=12
    )

    # =========================================
    # FALLBACK
    # =========================================

    if len(recommended_foods) == 0:

        return {

            'daily_calories': daily_calories,

            'breakfast_target': breakfast_target,
            'lunch_target': lunch_target,
            'dinner_target': dinner_target,
            'snack_target': snack_target,

            'breakfast': [],
            'lunch': [],
            'dinner': [],
            'snack': [],

            'recommendation_based': False

        }

    # =========================================
    # SPLIT MEALS
    # =========================================

    breakfast = recommended_foods[:3]

    lunch = recommended_foods[3:6]

    dinner = recommended_foods[6:9]

    snack = recommended_foods[9:12]

    # =========================================
    # RETURN PLAN
    # =========================================

    return {

        'daily_calories': daily_calories,

        'breakfast_target': breakfast_target,
        'lunch_target': lunch_target,
        'dinner_target': dinner_target,
        'snack_target': snack_target,

        'breakfast': breakfast,
        'lunch': lunch,
        'dinner': dinner,
        'snack': snack,

        'recommendation_based': True

    }


# =========================================
# NUTRITION PLAN PAGE
# =========================================

@nutrition_bp.route('/nutrition-plan')
@login_required
def nutrition_plan():

    plan = generate_nutrition_plan(
        current_user
    )

    return render_template(

        'nutrition_plan.html',

        user=current_user,

        plan=plan

    )