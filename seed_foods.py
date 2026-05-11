import pandas as pd

from app import app
from extensions import db

from models.food import Food


# =========================================
# LOAD DATASET
# =========================================

df = pd.read_excel("dataset.xlsx")

# =========================================
# CLEAN COLUMN
# =========================================

df.columns = df.columns.str.strip()

print(df.columns)

# =========================================
# IMPORT
# =========================================

with app.app_context():

    Food.query.delete()

    db.session.commit()

    imported = 0

    for _, row in df.iterrows():

        food_name = str(

            row.get("food_name", "")

        ).strip()

        # SKIP EMPTY ROW
        if not food_name:

            continue

        # SKIP DUPLICATE
        existing_food = Food.query.filter_by(
            food_name=food_name
        ).first()

        if existing_food:

            continue

        food = Food(

            food_name=food_name,

            image=str(
                row.get("image", "")
            ),

            category=str(
                row.get("category", "")
            ),

            calories=float(
                row.get("calories", 0)
            ),

            sugar=float(
                row.get("sugar", 0)
            ),

            protein=float(
                row.get("protein", 0)
            ),

            carbohydrates=float(
                row.get("carbohydrates", 0)
            ),

            fat=float(
                row.get("fat", 0)
            )

        )

        db.session.add(food)

        imported += 1

    db.session.commit()

    print(f"{imported} foods imported successfully")