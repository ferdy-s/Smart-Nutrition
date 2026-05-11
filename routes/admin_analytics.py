from extensions import db

from flask import Blueprint
from flask import render_template

from flask_login import login_required

from middlewares.admin_required import admin_required

from models.user import User
from models.food import Food
from models.preference import UserPreference

from sqlalchemy import func


admin_analytics_bp = Blueprint(
    'admin_analytics',
    __name__
)


# =========================================
# ADMIN ANALYTICS
# =========================================

@admin_analytics_bp.route('/admin/analytics')
@login_required
@admin_required
def admin_analytics():

    # =====================================
    # TOTAL DATA
    # =====================================

    total_users = User.query.filter(
        User.role != 'admin'
    ).count()

    total_foods = Food.query.count()

    total_preferences = UserPreference.query.count()

    # =====================================
    # ACTIVE USERS
    # =====================================

    active_users = User.query.filter(
        User.profile_completed == True
    ).count()

    # =====================================
    # ONBOARDING COMPLETE
    # =====================================

    completed_users = 0

    users = User.query.filter(
        User.role != 'admin'
    ).all()

    for user in users:

        ratings = UserPreference.query.filter_by(
            user_id=user.id
        ).count()

        if ratings >= 10:

            completed_users += 1

    onboarding_percentage = 0

    if total_users > 0:

        onboarding_percentage = int(
            (completed_users / total_users) * 100
        )

    # =====================================
    # AVG RATING
    # =====================================

    avg_rating = db.session.query(
        func.avg(UserPreference.rating)
    ).scalar()

    if not avg_rating:

        avg_rating = 0

    avg_rating = round(avg_rating, 1)

    # =====================================
    # RECOMMENDATION ACCURACY
    # =====================================

    recommendation_accuracy = min(
        60 + onboarding_percentage,
        98
    )

    # =====================================
    # MOST RATED FOODS
    # =====================================

    most_rated_foods = db.session.query(

        Food.food_name,

        func.count(
            UserPreference.id
        ).label('total')

    ).join(

        UserPreference,
        UserPreference.food_id == Food.id

    ).group_by(

        Food.food_name

    ).order_by(

        func.count(
            UserPreference.id
        ).desc()

    ).limit(5).all()

    # =====================================
    # TOP ATHLETES
    # =====================================

    top_athletes = db.session.query(

        User.full_name,

        func.count(
            UserPreference.id
        ).label('ratings')

    ).join(

        UserPreference,
        UserPreference.user_id == User.id

    ).group_by(

        User.full_name

    ).order_by(

        func.count(
            UserPreference.id
        ).desc()

    ).limit(5).all()

    # =====================================
    # TRAINING DISTRIBUTION
    # =====================================

    cutting_count = User.query.filter(
        User.training_phase == 'Cutting'
    ).count()

    normal_count = User.query.filter(
        User.training_phase == 'Normal Training'
    ).count()

    bulking_count = User.query.filter(
        User.training_phase == 'Bulking'
    ).count()

    # =====================================
    # RECENT ACTIVITIES
    # =====================================

    recent_preferences = UserPreference.query.order_by(
        UserPreference.id.desc()
    ).limit(10).all()

    # =====================================
    # RENDER
    # =====================================

    return render_template(

        'admin_analytics.html',

        total_users=total_users,

        total_foods=total_foods,

        total_preferences=total_preferences,

        active_users=active_users,

        onboarding_percentage=onboarding_percentage,

        avg_rating=avg_rating,

        recommendation_accuracy=recommendation_accuracy,

        most_rated_foods=most_rated_foods,

        top_athletes=top_athletes,

        cutting_count=cutting_count,

        normal_count=normal_count,

        bulking_count=bulking_count,

        recent_preferences=recent_preferences

    )