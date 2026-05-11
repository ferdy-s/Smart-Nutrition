# routes/admin_foods.py

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_required

from extensions import db

from middlewares.admin_required import admin_required

from models.food import Food


admin_foods_bp = Blueprint(
    'admin_foods',
    __name__
)


# =========================================
# FOOD DATABASE PAGE
# =========================================

@admin_foods_bp.route('/admin-food')
@login_required
@admin_required
def admin_foods():

    search = request.args.get(
        'search',
        ''
    )

    # =====================================
    # SEARCH FOODS
    # =====================================

    if search:

        foods = Food.query.filter(

            Food.food_name.ilike(
                f'%{search}%'
            )

        ).order_by(

            Food.food_name.asc()

        ).all()

    else:

        foods = Food.query.order_by(

            Food.food_name.asc()

        ).all()

    # =====================================
    # TOTAL DATA
    # =====================================

    total_foods = Food.query.count()

    total_normal = Food.query.filter_by(
        cocok_normal=True
    ).count()

    total_cutting = Food.query.filter_by(
        cocok_cutting=True
    ).count()

    return render_template(

        'admin_foods.html',

        foods=foods,

        total_foods=total_foods,

        total_normal=total_normal,

        total_cutting=total_cutting,

        search=search

    )


# =========================================
# CREATE FOOD
# =========================================

@admin_foods_bp.route(
    '/admin-food/create',
    methods=['POST']
)
@login_required
@admin_required
def create_food():

    try:

        food = Food(

            food_name=request.form.get(
                'food_name'
            ),

            image=request.form.get(
                'image'
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

            cocok_normal=bool(
                request.form.get(
                    'cocok_normal'
                )
            ),

            cocok_cutting=bool(
                request.form.get(
                    'cocok_cutting'
                )
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
        url_for(
            'admin_foods.admin_foods'
        )
    )


# =========================================
# UPDATE FOOD
# =========================================

@admin_foods_bp.route(
    '/admin-food/update/<int:id>',
    methods=['POST']
)
@login_required
@admin_required
def update_food(id):

    food = Food.query.get_or_404(id)

    try:

        food.food_name = request.form.get(
            'food_name'
        )

        food.image = request.form.get(
            'image'
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

        food.cocok_normal = bool(
            request.form.get(
                'cocok_normal'
            )
        )

        food.cocok_cutting = bool(
            request.form.get(
                'cocok_cutting'
            )
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
        url_for(
            'admin_foods.admin_foods'
        )
    )


# =========================================
# DELETE FOOD
# =========================================

@admin_foods_bp.route(
    '/admin-food/delete/<int:id>'
)
@login_required
@admin_required
def delete_food(id):

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
        url_for(
            'admin_foods.admin_foods'
        )
    )