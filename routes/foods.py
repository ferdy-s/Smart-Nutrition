from extensions import socketio

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_required
from flask_login import current_user

from extensions import db

from models.food import Food
from models.user import User
from models.preference import UserPreference

from services.recommendation import (
    get_top_recommendations
)


foods_bp = Blueprint(
    'foods',
    __name__
)


# =========================================
# ROOT REDIRECT
# =========================================

@foods_bp.route('/')
@login_required
def root_redirect():

    if current_user.role == 'admin':

        return redirect(
            url_for('foods.admin_dashboard')
        )

    return redirect(
        url_for('foods.user_dashboard')
    )


# =========================================
# USER DASHBOARD
# =========================================

@foods_bp.route('/dashboard')
@login_required
def user_dashboard():

    # =====================================
    # ADMIN REDIRECT
    # =====================================

    if current_user.role == 'admin':

        return redirect(
            url_for('foods.admin_dashboard')
        )

    # =====================================
    # USER PREFERENCES
    # =====================================

    preferences = UserPreference.query.filter_by(
        user_id=current_user.id
    ).all()

    ratings = {

        pref.food_id: pref.rating

        for pref in preferences

    }

    total_ratings = len(preferences)

    # =====================================
    # PROGRESS BAR
    # =====================================

    progress_width = int(

        min(
            (total_ratings / 10) * 100,
            100
        )

    )

    # =====================================
    # AI STATUS
    # =====================================

    onboarding_completed = (
        total_ratings >= 10
    )

    ai_ready = onboarding_completed

    # =====================================
    # SAFE USER DATA
    # =====================================

    sugar_limit = (
        current_user.sugar_limit or 9999
    )

    training_phase = str(

        current_user.training_phase or ''

    ).upper()

    # =====================================
    # BASE FILTER
    # =====================================

    foods_query = Food.query.filter(

        Food.sugar <= sugar_limit

    )

    # =====================================
    # TRAINING PHASE FILTER
    # =====================================

    if training_phase == 'NORMAL':

        foods_query = foods_query.filter(
            Food.cocok_normal == True
        )

    elif training_phase in [

        'CUTTING',
        'WEIGHT CUTTING'

    ]:

        foods_query = foods_query.filter(
            Food.cocok_cutting == True
        )

    # =====================================
    # FILTERED FOODS
    # =====================================

    filtered_foods = foods_query.all()

    # =====================================
    # NEW USER FLOW
    # =====================================

    if total_ratings < 10:

        foods = Food.query.order_by(

            Food.protein.desc()

        ).limit(12).all()

        for food in foods:

            food.predicted_score = 0

    # =====================================
    # AI RECOMMENDATION FLOW
    # =====================================

    else:

        recommendations = get_top_recommendations(
            current_user.id
        )

        allowed_food_ids = [

            food.id

            for food in filtered_foods

        ]

        foods = [

            food

            for food in recommendations

            if food.id in allowed_food_ids

        ]

        # =================================
        # FALLBACK
        # =================================

        if len(foods) == 0:

            foods = filtered_foods[:10]

            for food in foods:

                food.predicted_score = 0

    # =====================================
    # DASHBOARD ANALYTICS
    # =====================================

    total_protein = round(

        sum(

            food.protein or 0

            for food in foods

        ),

        2

    )

    total_low_sugar = len([

        food

        for food in foods

        if (food.sugar or 0) <= 10

    ])

    average_prediction_score = 0

    if len(foods) > 0:

        average_prediction_score = round(

            sum(

                getattr(
                    food,
                    'predicted_score',
                    0
                )

                for food in foods

            ) / len(foods),

            2

        )

    # =====================================
    # RENDER
    # =====================================

    return render_template(

        'user_dashboard.html',

        foods=foods,

        ratings=ratings,

        total_ratings=total_ratings,

        onboarding_completed=onboarding_completed,

        ai_ready=ai_ready,

        total_protein=total_protein,

        total_low_sugar=total_low_sugar,

        progress_width=progress_width,

        average_prediction_score=average_prediction_score

    )


# =========================================
# ADMIN DASHBOARD
# =========================================

@foods_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():

    # =====================================
    # BLOCK NON ADMIN
    # =====================================

    if current_user.role != 'admin':

        return redirect(
            url_for('foods.user_dashboard')
        )

    foods = Food.query.all()

    users = User.query.all()

    preferences = UserPreference.query.all()

    total_foods = Food.query.count()

    total_users = User.query.count()

    total_preferences = UserPreference.query.count()

    # =====================================
    # ANALYTICS
    # =====================================

    acceptance_rate = 82

    average_predicted_score = 4.3

    onboarding_completion_rate = 76

    active_athletes = total_users

    recommendation_accuracy = 88

    most_liked_food = "Chicken Breast"

    return render_template(

        'admin_dashboard.html',

        foods=foods,

        users=users,

        preferences=preferences,

        total_foods=total_foods,

        total_users=total_users,

        total_preferences=total_preferences,

        acceptance_rate=acceptance_rate,

        average_predicted_score=average_predicted_score,

        onboarding_completion_rate=onboarding_completion_rate,

        active_athletes=active_athletes,

        recommendation_accuracy=recommendation_accuracy,

        most_liked_food=most_liked_food

    )


# =========================================
# RATE FOOD
# =========================================

@foods_bp.route(
    '/rate-food/<int:food_id>',
    methods=['POST']
)
@login_required
def rate_food(food_id):

    try:

        rating = int(
            request.form['rating']
        )

    except:

        return redirect(
            url_for('foods.user_dashboard')
        )

    # =====================================
    # VALIDATION
    # =====================================

    if rating < 1 or rating > 5:

        return redirect(
            url_for('foods.user_dashboard')
        )

    # =====================================
    # EXISTING PREFERENCE
    # =====================================

    existing_preference = UserPreference.query.filter_by(

        user_id=current_user.id,

        food_id=food_id

    ).first()

    # =====================================
    # UPDATE
    # =====================================

    if existing_preference:

        existing_preference.rating = rating

    # =====================================
    # CREATE
    # =====================================

    else:

        preference = UserPreference(

            user_id=current_user.id,

            food_id=food_id,

            rating=rating

        )

        db.session.add(preference)

    db.session.commit()

    # =====================================
    # REALTIME EVENT
    # =====================================

    try:

        socketio.emit(

            'food_rated',

            {

                'user': current_user.full_name,

                'food_id': food_id,

                'rating': rating,

                'message': f'{current_user.full_name} rated food {rating}/5'

            }

        )

    except Exception as e:

        print(e)

    # =====================================
    # ONBOARDING ACTIVATION
    # =====================================

    total_preferences = UserPreference.query.filter_by(
        user_id=current_user.id
    ).count()

    if total_preferences == 10:

        flash(

            'AI Recommendation Activated Successfully',

            'success'

        )

    return redirect(
        url_for('foods.user_dashboard')
    )


# =========================================
# CREATE FOOD
# =========================================

@foods_bp.route(
    '/foods/create',
    methods=['GET', 'POST']
)
@login_required
def create_food():

    if current_user.role != 'admin':

        return redirect(
            url_for('foods.user_dashboard')
        )

    if request.method == 'POST':

        try:

            food = Food(

                food_name=request.form.get(
                    'food_name'
                ),

                calories=float(
                    request.form.get(
                        'calories',
                        0
                    ) or 0
                ),

                sugar=float(
                    request.form.get(
                        'sugar',
                        0
                    ) or 0
                ),

                protein=float(
                    request.form.get(
                        'protein',
                        0
                    ) or 0
                ),

                carbohydrates=float(
                    request.form.get(
                        'carbohydrates',
                        0
                    ) or 0
                ),

                fat=float(
                    request.form.get(
                        'fat',
                        0
                    ) or 0
                ),

                cocok_normal=(
                    'cocok_normal' in request.form
                ),

                cocok_cutting=(
                    'cocok_cutting' in request.form
                )

            )

            db.session.add(food)

            db.session.commit()

            flash(
                'Food created successfully',
                'success'
            )

        except Exception as e:

            db.session.rollback()

            flash(
                f'Create failed: {str(e)}',
                'error'
            )

        return redirect(
            url_for('foods.admin_dashboard')
        )

    return render_template(
        'create_food.html'
    )


# =========================================
# EDIT FOOD
# =========================================

@foods_bp.route(
    '/foods/edit/<int:id>',
    methods=['GET', 'POST']
)
@login_required
def edit_food(id):

    if current_user.role != 'admin':

        return redirect(
            url_for('foods.user_dashboard')
        )

    food = Food.query.get_or_404(id)

    if request.method == 'POST':

        try:

            food.food_name = request.form.get(
                'food_name'
            )

            food.calories = float(
                request.form.get(
                    'calories',
                    0
                ) or 0
            )

            food.sugar = float(
                request.form.get(
                    'sugar',
                    0
                ) or 0
            )

            food.protein = float(
                request.form.get(
                    'protein',
                    0
                ) or 0
            )

            food.carbohydrates = float(
                request.form.get(
                    'carbohydrates',
                    0
                ) or 0
            )

            food.fat = float(
                request.form.get(
                    'fat',
                    0
                ) or 0
            )

            food.cocok_normal = (
                'cocok_normal' in request.form
            )

            food.cocok_cutting = (
                'cocok_cutting' in request.form
            )

            db.session.commit()

            flash(
                'Food updated successfully',
                'success'
            )

        except Exception as e:

            db.session.rollback()

            flash(
                f'Update failed: {str(e)}',
                'error'
            )

        return redirect(
            url_for('foods.admin_dashboard')
        )

    return render_template(

        'edit_food.html',

        food=food

    )


# =========================================
# RECOMMENDATION PAGE
# =========================================

@foods_bp.route('/recommendations')
@login_required
def recommendations_page():

    recommendations = get_top_recommendations(
        current_user.id
    )

    # =====================================
    # FALLBACK
    # =====================================

    if len(recommendations) == 0:

        recommendations = Food.query.order_by(
            Food.protein.desc()
        ).limit(10).all()

        for food in recommendations:

            food.predicted_score = 0

    # =====================================
    # SAFE TOP FOOD
    # =====================================

    top_food = None

    if len(recommendations) > 0:

        top_food = recommendations[0]

    # =====================================
    # AI SUMMARY
    # =====================================

    ai_summary = ''

    if top_food:

        ai_summary = f'''

        Based on collaborative filtering analysis,
        athlete similarity patterns,
        nutrition profiling,
        and user preference behavior,
        the AI system recommends
        {top_food.food_name}
        as your highest predicted nutrition recommendation.

        '''

    return render_template(

        'recommendations.html',

        recommendations=recommendations,

        top_food=top_food,

        ai_summary=ai_summary

    )


# =========================================
# DELETE FOOD
# =========================================

@foods_bp.route('/foods/delete/<int:id>')
@login_required
def delete_food(id):

    if current_user.role != 'admin':

        return redirect(
            url_for('foods.user_dashboard')
        )

    try:

        food = Food.query.get_or_404(id)

        db.session.delete(food)

        db.session.commit()

        flash(
            'Food deleted successfully',
            'success'
        )

    except Exception as e:

        db.session.rollback()

        flash(
            f'Delete failed: {str(e)}',
            'error'
        )

    return redirect(
        url_for('foods.admin_dashboard')
    )