import pandas as pd

from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix

from models.recommendation_history import RecommendationHistory

from models.user import User
from models.food import Food
from models.preference import UserPreference


# =========================================
# BUILD EVALUATION DATA
# =========================================

def build_evaluation_data():

    histories = RecommendationHistory.query.all()

    y_true = []

    y_pred = []

    for history in histories:

        # =========================================
        # ACTUAL USER ACTION
        # =========================================

        actual = 1 if history.selected else 0

        # =========================================
        # AI PREDICTION THRESHOLD
        # =========================================

        predicted = 1 if (
            history.predicted_score >= 3.5
        ) else 0

        y_true.append(actual)

        y_pred.append(predicted)

    return y_true, y_pred


# =========================================
# CALCULATE METRICS
# =========================================

def calculate_metrics():

    y_true, y_pred = build_evaluation_data()

    # =========================================
    # EMPTY DATA PROTECTION
    # =========================================

    if len(y_true) == 0:

        return {

            'precision': 0,

            'recall': 0,

            'f1_score': 0,

            'confusion_matrix': [

                [0, 0],

                [0, 0]

            ]

        }

    # =========================================
    # METRICS
    # =========================================

    precision = precision_score(

        y_true,
        y_pred,

        zero_division=0

    )

    recall = recall_score(

        y_true,
        y_pred,

        zero_division=0

    )

    f1 = f1_score(

        y_true,
        y_pred,

        zero_division=0

    )

    cm = confusion_matrix(
        y_true,
        y_pred
    ).tolist()

    return {

        'precision': round(
            precision,
            4
        ),

        'recall': round(
            recall,
            4
        ),

        'f1_score': round(
            f1,
            4
        ),

        'confusion_matrix': cm

    }


# =========================================
# EXPORT ALL DATA
# =========================================

def build_export_data():

    # =========================================
    # USERS
    # =========================================

    users = User.query.all()

    users_data = []

    for user in users:

        users_data.append({

            'id': user.id,

            'full_name': user.full_name,

            'email': user.email,

            'role': user.role,

            'weight': user.weight,

            'sport_type': user.sport_type,

            'training_phase': user.training_phase,

            'daily_calories': user.daily_calories,

            'sugar_limit': user.sugar_limit

        })

    # =========================================
    # FOODS
    # =========================================

    foods = Food.query.all()

    foods_data = []

    for food in foods:

        foods_data.append({

            'id': food.id,

            'food_name': food.food_name,

            'calories': food.calories,

            'sugar': food.sugar,

            'protein': food.protein,

            'carbohydrates': food.carbohydrates,

            'fat': food.fat,

            'cocok_normal': food.cocok_normal,

            'cocok_cutting': food.cocok_cutting

        })

    # =========================================
    # PREFERENCES
    # =========================================

    preferences = UserPreference.query.all()

    preferences_data = []

    for pref in preferences:

        preferences_data.append({

            'id': pref.id,

            'user_id': pref.user_id,

            'food_id': pref.food_id,

            'rating': pref.rating

        })

    # =========================================
    # RECOMMENDATION HISTORY
    # =========================================

    histories = RecommendationHistory.query.all()

    histories_data = []

    for history in histories:

        histories_data.append({

            'id': history.id,

            'user_id': history.user_id,

            'food_id': history.food_id,

            'predicted_score': history.predicted_score,

            'selected': history.selected,

            'liked': history.liked,

            'created_at': history.created_at

        })

    return {

        'users': pd.DataFrame(users_data),

        'foods': pd.DataFrame(foods_data),

        'preferences': pd.DataFrame(preferences_data),

        'histories': pd.DataFrame(histories_data)

    }


# =========================================
# EXPORT CSV
# =========================================

def export_csv():

    data = build_export_data()

    data['users'].to_csv(
        'exports/users.csv',
        index=False
    )

    data['foods'].to_csv(
        'exports/foods.csv',
        index=False
    )

    data['preferences'].to_csv(
        'exports/preferences.csv',
        index=False
    )

    data['histories'].to_csv(
        'exports/histories.csv',
        index=False
    )

    return True


# =========================================
# EXPORT EXCEL
# =========================================

def export_excel():

    data = build_export_data()

    with pd.ExcelWriter(

        'exports/smart_nutrition_report.xlsx',

        engine='openpyxl'

    ) as writer:

        data['users'].to_excel(

            writer,

            sheet_name='users',

            index=False

        )

        data['foods'].to_excel(

            writer,

            sheet_name='foods',

            index=False

        )

        data['preferences'].to_excel(

            writer,

            sheet_name='preferences',

            index=False

        )

        data['histories'].to_excel(

            writer,

            sheet_name='recommendation_history',

            index=False

        )

    return True