from app import app

from extensions import db

from models.user import User

from werkzeug.security import generate_password_hash


with app.app_context():

    # =====================================
    # CHECK EXISTING ADMIN
    # =====================================

    existing_admin = User.query.filter_by(

        email='admin_ferdy@smartnutrition.com'

    ).first()

    if existing_admin:

        print('Admin already exists')

    else:

        # =================================
        # CREATE ADMIN
        # =================================

        admin = User(

            full_name='Administrator',

            username='adminferdy',

            email='admin_ferdy@smartnutrition.com',

            password=generate_password_hash(
                'adminferdy123'
            ),

            role='admin',

            weight=70,

            sport_type='Admin',

            training_phase='Normal Training',

            daily_calories=2500,

            sugar_limit=50,

            protein_target=140,

            carbs_target=280,

            fat_target=70,

            onboarding_completed=True,

            profile_completed=True,

            recommendation_model='Admin System'

        )

        db.session.add(admin)

        db.session.commit()

        print('=================================')
        print('ADMIN CREATED SUCCESSFULLY')
        print('=================================')

        print('EMAIL : admin_ferdy@smartnutrition.com')

        print('PASSWORD : adminferdy123')