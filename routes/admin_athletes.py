from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_required

from extensions import db

from middlewares.admin_required import admin_required

from models.user import User


admin_athletes_bp = Blueprint(
    'admin_athletes',
    __name__
)


# =========================================
# ATHLETES PAGE
# =========================================

@admin_athletes_bp.route('/athletes')
@login_required
@admin_required
def athletes():

    search = request.args.get(
        'search',
        ''
    )

    if search:

        users = User.query.filter(

            User.full_name.ilike(
                f'%{search}%'
            )

        ).all()

    else:

        users = User.query.order_by(
            User.full_name.asc()
        ).all()

    return render_template(

        'admin_athletes.html',

        users=users,

        search=search

    )


# =========================================
# EDIT ATHLETE
# =========================================

@admin_athletes_bp.route(
    '/athletes/edit/<int:id>',
    methods=['POST']
)
@login_required
@admin_required
def edit_athlete(id):

    user = User.query.get_or_404(id)

    user.full_name = request.form.get(
        'full_name'
    )

    user.weight = float(

        request.form.get(
            'weight',
            0
        )

    )

    user.sport_type = request.form.get(
        'sport_type'
    )

    user.training_phase = request.form.get(
        'training_phase'
    )

    user.daily_calories = (
        user.weight * 35
    )

    db.session.commit()

    flash(
        'Athlete updated successfully',
        'success'
    )

    return redirect(
        url_for(
            'admin_athletes.athletes'
        )
    )


# =========================================
# DELETE ATHLETE
# =========================================

@admin_athletes_bp.route(
    '/athletes/delete/<int:id>'
)
@login_required
@admin_required
def delete_athlete(id):

    user = User.query.get_or_404(id)

    db.session.delete(user)

    db.session.commit()

    flash(
        'Athlete deleted successfully',
        'success'
    )

    return redirect(
        url_for(
            'admin_athletes.athletes'
        )
    )