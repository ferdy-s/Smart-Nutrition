# routes/profile.py

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_required
from flask_login import current_user

from extensions import db

import hashlib


profile_bp = Blueprint(
    'profile',
    __name__
)


# =========================================
# PROFILE PAGE
# =========================================

@profile_bp.route(
    '/profile',
    methods=['GET', 'POST']
)
@login_required
def profile():

    # =====================================
    # UPDATE PROFILE
    # =====================================

    if request.method == 'POST':

        # =================================
        # FULL NAME
        # =================================

        full_name = request.form.get(
            'full_name',
            ''
        ).strip()

        if full_name:

            current_user.full_name = full_name

            # OPTIONAL
            if hasattr(current_user, 'username'):

                current_user.username = full_name

        # =================================
        # WEIGHT
        # =================================

        weight_raw = request.form.get(
            'weight',
            '0'
        )

        try:

            weight = float(weight_raw)

        except:

            weight = 0

        current_user.weight = weight

        # =================================
        # SPORT TYPE
        # =================================

        sport_type = request.form.get(
            'sport_type'
        )

        if sport_type:

            current_user.sport_type = sport_type

        # =================================
        # TRAINING PHASE
        # =================================

        training_phase = request.form.get(
            'training_phase'
        )

        if training_phase:

            current_user.training_phase = training_phase

        # =================================
        # AUTO CALCULATE NUTRITION
        # =================================

        current_user.daily_calories = (
            weight * 35
        )

        current_user.sugar_limit = (
            current_user.daily_calories * 0.025
        )

        # =================================
        # OPTIONAL TARGETS
        # =================================

        if hasattr(current_user, 'protein_target'):

            current_user.protein_target = (
                weight * 2
            )

        if hasattr(current_user, 'carbs_target'):

            current_user.carbs_target = (
                weight * 4
            )

        if hasattr(current_user, 'fat_target'):

            current_user.fat_target = (
                weight * 1
            )

        # =================================
        # PROFILE STATUS
        # =================================

        if hasattr(current_user, 'profile_completed'):

            current_user.profile_completed = True

        if hasattr(current_user, 'onboarding_completed'):

            current_user.onboarding_completed = True

        # =================================
        # SAVE DATABASE
        # =================================

        db.session.commit()

        # =================================
        # SUCCESS POPUP
        # =================================

        flash(

            'Profile updated successfully',

            'success'

        )

        return redirect(

            url_for(
                'profile.profile'
            )

        )

    # =====================================
    # SAFE DATA
    # =====================================

    daily_calories = 0

    sugar_limit = 0

    try:

        if current_user.daily_calories:

            daily_calories = float(
                current_user.daily_calories
            )

        if current_user.sugar_limit:

            sugar_limit = float(
                current_user.sugar_limit
            )

    except:

        daily_calories = 0

        sugar_limit = 0

    # =====================================
    # GRAVATAR
    # =====================================

    email = str(
        current_user.email
    ).lower().strip()

    email_hash = hashlib.md5(

        email.encode()

    ).hexdigest()

    gravatar_url = (

        f'https://www.gravatar.com/avatar/'
        f'{email_hash}?d=identicon&s=200'

    )

    # =====================================
    # RENDER TEMPLATE
    # =====================================

    return render_template(

        'profile.html',

        user=current_user,

        gravatar_url=gravatar_url,

        daily_calories=daily_calories,

        sugar_limit=sugar_limit

    )