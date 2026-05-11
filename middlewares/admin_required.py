# middlewares/admin_required.py

from functools import wraps

from flask import redirect
from flask import url_for
from flask import flash

from flask_login import current_user


# =========================================
# ADMIN REQUIRED MIDDLEWARE
# =========================================

def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        # =====================================
        # CHECK LOGIN
        # =====================================

        if not current_user.is_authenticated:

            flash(
                'Please login first',
                'error'
            )

            return redirect(
                url_for('auth.login')
            )

        # =====================================
        # CHECK ROLE
        # =====================================

        if current_user.role != 'admin':

            flash(
                'Admin access only',
                'error'
            )

            return redirect('/dashboard')

        return f(*args, **kwargs)

    return decorated_function