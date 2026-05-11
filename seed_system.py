import pandas as pd

from app import app
from extensions import db

from models.user import User
from models.food import Food
from models.preference import UserPreference

from werkzeug.security import generate_password_hash


# =========================================
# LOAD DATASET
# =========================================

DATASET_PATH = 'dataset.xlsx'

df = pd.read_excel(DATASET_PATH)

print("=================================")
print("DATASET LOADED")
print("=================================")

print(df.shape)

print()


# =========================================
# FOOD COLUMNS
# =========================================

food_columns = []

for col in df.columns:

    if 'Seberapa Anda menyukai makanan berikut?' in col:

        food_columns.append(col)

print(f"Food Columns: {len(food_columns)}")


# =========================================
# FOOD NAMES
# =========================================

food_names = []

for col in food_columns:

    food_name = col.split('[')[1].replace(']', '')

    food_names.append(food_name)

print(f"Food Names Extracted: {len(food_names)}")

print()


# =========================================
# APP CONTEXT
# =========================================

with app.app_context():

    print("=================================")
    print("CLEARING OLD DATABASE")
    print("=================================")

    # =====================================
    # CLEAR OLD DATA
    # =====================================

    UserPreference.query.delete()

    Food.query.delete()

    User.query.delete()

    db.session.commit()

    print("Old database cleared")

    print()


    # =====================================
    # INSERT FOODS
    # =====================================

    print("=================================")
    print("INSERTING FOODS")
    print("=================================")

    food_objects = {}

    inserted_foods = 0

    for food_name in food_names:

        food_name = str(food_name).strip()

        # =================================
        # SKIP EMPTY
        # =================================

        if not food_name:

            continue

        # =================================
        # SKIP DUPLICATE
        # =================================

        existing_food = Food.query.filter_by(

            food_name=food_name

        ).first()

        if existing_food:

            continue

        # =================================
        # AUTO FLAGS
        # =================================

        high_protein = False
        low_sugar = False

        # =================================
        # CREATE FOOD
        # =================================

        food = Food(

            food_name=food_name,

            image='',

            category='Athlete Nutrition',

            description=f'{food_name} nutrition food',

            calories=0,

            sugar=0,

            protein=0,

            carbohydrates=0,

            fat=0,

            fiber=0,

            sodium=0,

            cocok_normal=True,

            cocok_cutting=True,

            cocok_bulking=True,

            low_sugar=low_sugar,

            high_protein=high_protein

        )

        db.session.add(food)

        db.session.flush()

        food_objects[food_name] = food

        inserted_foods += 1

    db.session.commit()

    print(f"{inserted_foods} foods inserted")

    print()


    # =====================================
    # INSERT USERS
    # =====================================

    print("=================================")
    print("INSERTING USERS")
    print("=================================")

    inserted_users = 0

    inserted_preferences = 0

    for _, row in df.iterrows():

        # =================================
        # BASIC INFO
        # =================================

        full_name = str(

            row.get(
                'Nama Lengkap Atlet',
                ''
            )

        ).strip()

        email = str(

            row.get(
                'Email',
                ''
            )

        ).strip().lower()

        # =================================
        # SKIP INVALID USER
        # =================================

        if not full_name:

            continue

        if not email:

            continue

        # =================================
        # CLEAN WEIGHT
        # =================================

        weight_raw = str(

            row.get(
                'Berat Badan (kg)',
                '0'
            )

        ).lower()

        weight_raw = weight_raw.replace(
            'kg',
            ''
        ).strip()

        try:

            weight = float(weight_raw)

        except:

            weight = 0

        # =================================
        # SPORT INFO
        # =================================

        sport_type = str(

            row.get(
                'Jenis Latihan',
                'General Training'
            )

        ).strip()

        training_phase = str(

            row.get(
                'Fase Latihan',
                'Normal Training'
            )

        ).strip()

        # =================================
        # CALCULATE NUTRITION
        # =================================

        daily_calories = weight * 35

        sugar_limit = daily_calories * 0.025

        protein_target = weight * 2

        carbs_target = weight * 4

        fat_target = weight * 1

        # =================================
        # CHECK EXISTING USER
        # =================================

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            continue

        # =================================
        # CREATE USER
        # =================================

        user = User(

            full_name=full_name,

            username=full_name,

            email=email,

            password=generate_password_hash(
                '123456'
            ),

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

            profile_completed=True,

            recommendation_model='Collaborative Filtering'

        )

        db.session.add(user)

        db.session.flush()

        inserted_users += 1

        # =================================
        # INSERT PREFERENCES
        # =================================

        for food_col in food_columns:

            food_name = food_col.split('[')[1].replace(']', '')

            rating = row[food_col]

            # =============================
            # SKIP EMPTY
            # =============================

            if pd.isna(rating):

                continue

            # =============================
            # CLEAN RATING
            # =============================

            rating_raw = str(
                rating
            ).strip()

            # =============================
            # EXTRACT NUMBER
            # =============================

            try:

                rating = int(

                    rating_raw.split()[0]

                )

            except:

                continue

            # =============================
            # VALIDATE
            # =============================

            if rating < 1 or rating > 5:

                continue

            # =============================
            # GET FOOD
            # =============================

            food = food_objects.get(
                food_name
            )

            if not food:

                continue

            # =============================
            # CREATE PREFERENCE
            # =============================

            preference = UserPreference(

                user_id=user.id,

                food_id=food.id,

                rating=rating

            )

            db.session.add(preference)

            inserted_preferences += 1

    db.session.commit()

    print(f"{inserted_users} users inserted")

    print(f"{inserted_preferences} preferences inserted")

    print()


    # =====================================
    # FINAL RESULT
    # =====================================

    print("=================================")
    print("FINAL DATABASE GENERATED")
    print("=================================")

    print(f"Users        : {User.query.count()}")

    print(f"Foods        : {Food.query.count()}")

    print(f"Preferences  : {UserPreference.query.count()}")

    print()

    print("=================================")
    print("COLLABORATIVE FILTERING READY")
    print("=================================")