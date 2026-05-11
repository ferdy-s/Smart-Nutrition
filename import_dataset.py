import pandas as pd

from app import app

from extensions import db

from models.user import User
from models.food import Food
from models.preference import UserPreference


# =========================================
# LOAD DATASET
# =========================================

file_path = 'dataset.xlsx'

df = pd.read_excel(file_path)


# =========================================
# FOOD COLUMNS
# =========================================

food_columns = [

    col for col in df.columns

    if 'Seberapa Anda menyukai makanan berikut?' in str(col)

]


with app.app_context():

    # =========================================
    # CREATE FOODS
    # =========================================

    food_map = {}

    for column in food_columns:

        # AMBIL NAMA MAKANAN DI DALAM []

        food_name = column.split('[')[-1].replace(']', '').strip()

        existing_food = Food.query.filter_by(
            food_name=food_name
        ).first()

        if not existing_food:

            food = Food(

                food_name=food_name,

                calories=0,

                sugar=0,

                protein=0,

                carbohydrates=0,

                fat=0,

                cocok_normal=True,

                cocok_cutting=True

            )

            db.session.add(food)

            db.session.commit()

            food_map[food_name] = food.id

        else:

            food_map[food_name] = existing_food.id


    # =========================================
    # CREATE USERS
    # =========================================

    for index, row in df.iterrows():

        full_name = str(
            row.get('Nama Lengkap Atlet', 'Unknown')
        )

        email = str(
            row.get('Email', f'user{index}@example.com')
        )

        # =========================================
        # CLEAN WEIGHT
        # =========================================

        weight_raw = str(
            row.get('Berat Badan (kg)', 70)
        )

        # CONVERT:
        # "59kg" -> 59
        # "70 kg" -> 70

        weight = float(

            weight_raw
            .lower()
            .replace('kg', '')
            .replace(' ', '')

        )

        sport_type = str(
            row.get('Jenis Latihan', 'Boxing')
        )

        training_phase = str(
            row.get('Fase Latihan', 'NORMAL')
        )

        # =========================================
        # NUTRITION CALCULATION
        # =========================================

        daily_calories = weight * 35

        sugar_limit = (0.1 * daily_calories) / 4


        existing_user = User.query.filter_by(
            email=email
        ).first()


        if not existing_user:

            user = User(

                full_name=full_name,

                email=email,

                password='imported-user',

                weight=weight,

                sport_type=sport_type,

                training_phase=training_phase,

                daily_calories=daily_calories,

                sugar_limit=sugar_limit

            )

            db.session.add(user)

            db.session.commit()

        else:

            user = existing_user


        # =========================================
        # INSERT RATINGS
        # =========================================

        for column in food_columns:

            food_name = column.split('[')[-1].replace(']', '').strip()

            rating = row[column]

            if pd.notna(rating):

                existing_pref = UserPreference.query.filter_by(

                    user_id=user.id,

                    food_id=food_map[food_name]

                ).first()

                if not existing_pref:

                    # CONVERT:
                    # "5 Sangat Suka" -> 5
                    # "3 Netral" -> 3

                    rating_value = int(
                        str(rating).split()[0]
                    )

                    pref = UserPreference(

                        user_id=user.id,

                        food_id=food_map[food_name],

                        rating=rating_value

                    )

                    db.session.add(pref)


    db.session.commit()


print('DATASET IMPORT SUCCESSFULLY')