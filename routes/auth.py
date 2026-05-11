from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user

from flask_dance.contrib.google import google

from extensions import db

from models.user import User


auth_bp = Blueprint(
    'auth',
    __name__
)


# =========================================
# REGISTER
# =========================================

@auth_bp.route(
    '/register',
    methods=['GET', 'POST']
)
def register():

    # =====================================
    # ALREADY LOGIN
    # =====================================

    if current_user.is_authenticated:

        if current_user.role == 'admin':

            return redirect(
                url_for(
                    'foods.admin_dashboard'
                )
            )

        return redirect(
            url_for(
                'foods.user_dashboard'
            )
        )

    # =====================================
    # REGISTER PROCESS
    # =====================================

    if request.method == 'POST':

        full_name = request.form.get(
            'full_name'
        )

        username = request.form.get(
            'username'
        )

        email = request.form.get(
            'email'
        )

        password = request.form.get(
            'password'
        )

        weight = float(

            request.form.get(
                'weight'
            )

        )

        sport_type = request.form.get(
            'sport_type'
        )

        training_phase = request.form.get(
            'training_phase'
        )

        # =====================================
        # CHECK EXISTING EMAIL
        # =====================================

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                'Email sudah digunakan',
                'danger'
            )

            return redirect(
                url_for(
                    'auth.register'
                )
            )

        # =====================================
        # AUTO CALCULATE
        # =====================================

        daily_calories = weight * 35

        sugar_limit = (
            0.1 * daily_calories
        ) / 4

        protein_target = weight * 2.0

        carbs_target = weight * 4.0

        fat_target = weight * 1.0

        # =====================================
        # HASH PASSWORD
        # =====================================

        hashed_password = (
            generate_password_hash(
                password
            )
        )

        # =====================================
        # CREATE USER
        # =====================================

        user = User(

            full_name=full_name,

            username=username,

            email=email,

            password=hashed_password,

            role='user',

            weight=weight,

            sport_type=sport_type,

            training_phase=training_phase,

            daily_calories=daily_calories,

            sugar_limit=sugar_limit,

            protein_target=protein_target,

            carbs_target=carbs_target,

            fat_target=fat_target,

            onboarding_completed=True,

            profile_completed=True

        )

        db.session.add(user)

        db.session.commit()

        flash(
            'Register berhasil',
            'success'
        )

        return redirect(
            url_for(
                'auth.login'
            )
        )

    return render_template(
        'register.html'
    )


# =========================================
# LOGIN
# =========================================

@auth_bp.route(
    '/login',
    methods=['GET', 'POST']
)
def login():

    # =====================================
    # ALREADY LOGIN
    # =====================================

    if current_user.is_authenticated:

        if current_user.role == 'admin':

            return redirect(
                url_for(
                    'foods.admin_dashboard'
                )
            )

        # =====================================
        # PROFILE CHECK
        # =====================================

        if not current_user.profile_completed:

            return redirect(
                url_for(
                    'profile.profile'
                )
            )

        return redirect(
            url_for(
                'foods.user_dashboard'
            )
        )

    # =====================================
    # LOGIN PROCESS
    # =====================================

    if request.method == 'POST':

        email = request.form.get(
            'email'
        )

        password = request.form.get(
            'password'
        )

        user = User.query.filter_by(
            email=email
        ).first()

        # =====================================
        # VALIDATE PASSWORD
        # =====================================

        if user and check_password_hash(

            user.password,
            password

        ):

            login_user(

                user,

                remember=True

            )

            # =====================================
            # ADMIN REDIRECT
            # =====================================

            if user.role == 'admin':

                return redirect(
                    url_for(
                        'foods.admin_dashboard'
                    )
                )

            # =====================================
            # PROFILE CHECK
            # =====================================

            if not user.profile_completed:

                return redirect(
                    url_for(
                        'profile.profile'
                    )
                )

            return redirect(
                url_for(
                    'foods.user_dashboard'
                )
            )

        flash(
            'Email atau password salah',
            'danger'
        )

    return render_template(
        'login.html'
    )


# =========================================
# GOOGLE LOGIN
# =========================================

@auth_bp.route('/google-login')
def google_login():

    # =====================================
    # REDIRECT TO GOOGLE
    # =====================================

    if not google.authorized:

        return redirect(
            url_for(
                'google.login'
            )
        )

    # =====================================
    # GET USER INFO
    # =====================================

    response = google.get(
        '/oauth2/v2/userinfo'
    )

    if not response.ok:

        flash(
            'Google login gagal',
            'danger'
        )

        return redirect(
            url_for(
                'auth.login'
            )
        )

    info = response.json()

    email = info.get('email')

    name = info.get(
        'name',
        'Google User'
    )

    google_id = info.get('id')

    picture = info.get('picture')

    # =====================================
    # CHECK USER
    # =====================================

    user = User.query.filter_by(
        email=email
    ).first()

    # =====================================
    # AUTO CREATE USER
    # =====================================

    if not user:

        user = User(

            full_name=name,

            username=name,

            email=email,

            password=generate_password_hash(
                'google-oauth-user'
            ),

            google_id=google_id,

            profile_picture=picture,

            role='user',

            # =====================================
            # EMPTY PROFILE
            # =====================================

            weight=0,

            sport_type='',

            training_phase='Normal Training',

            daily_calories=0,

            sugar_limit=0,

            protein_target=0,

            carbs_target=0,

            fat_target=0,

            onboarding_completed=False,

            profile_completed=False

        )

        db.session.add(user)

        db.session.commit()

    # =====================================
    # UPDATE GOOGLE DATA
    # =====================================

    else:

        user.google_id = google_id

        user.profile_picture = picture

        db.session.commit()

    # =====================================
    # LOGIN SESSION
    # =====================================

    login_user(

        user,

        remember=True,

        force=True

    )

    # =====================================
    # ADMIN REDIRECT
    # =====================================

    if user.role == 'admin':

        return redirect(
            url_for(
                'foods.admin_dashboard'
            )
        )

    # =====================================
    # PROFILE ONBOARDING
    # =====================================

    if not user.profile_completed:

        return redirect(
            url_for(
                'profile.profile'
            )
        )

    # =====================================
    # USER DASHBOARD
    # =====================================

    return redirect(
        url_for(
            'foods.user_dashboard'
        )
    )


# =========================================
# LOGOUT
# =========================================

@auth_bp.route('/logout')
@login_required
def logout():

    logout_user()

    flash(
        'Logout berhasil',
        'success'
    )

    return redirect(
        url_for(
            'auth.login'
        )
    )