# services/recommendation.py

import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

from models.preference import UserPreference
from models.food import Food


# =========================================
# BUILD USER ITEM MATRIX
# =========================================

def build_matrix():

    preferences = UserPreference.query.all()

    data = []

    for pref in preferences:

        data.append({

            'user_id': pref.user_id,
            'food_id': pref.food_id,
            'rating': pref.rating

        })

    # =====================================
    # EMPTY DATA
    # =====================================

    if len(data) == 0:

        return None

    # =====================================
    # DATAFRAME
    # =====================================

    df = pd.DataFrame(data)

    matrix = df.pivot_table(

        index='user_id',

        columns='food_id',

        values='rating'

    ).fillna(0)

    return matrix


# =========================================
# GET SIMILARITY MATRIX
# =========================================

def build_similarity_matrix(matrix):

    similarity = cosine_similarity(matrix)

    similarity_df = pd.DataFrame(

        similarity,

        index=matrix.index,

        columns=matrix.index

    )

    return similarity_df


# =========================================
# GET TOP RECOMMENDATIONS
# =========================================

def get_top_recommendations(user_id, top_n=10):

    matrix = build_matrix()

    # =====================================
    # EMPTY MATRIX
    # =====================================

    if matrix is None:

        return []

    # =====================================
    # USER NOT FOUND
    # =====================================

    if user_id not in matrix.index:

        return []

    # =====================================
    # BUILD SIMILARITY
    # =====================================

    similarity_df = build_similarity_matrix(
        matrix
    )

    # =====================================
    # TARGET USER SIMILARITY
    # =====================================

    user_similarity = similarity_df[user_id]

    similar_users = user_similarity.sort_values(

        ascending=False

    )

    # =====================================
    # REMOVE SELF
    # =====================================

    similar_users = similar_users.drop(
        user_id
    )

    # =====================================
    # USER RATINGS
    # =====================================

    user_ratings = matrix.loc[user_id]

    unrated_foods = user_ratings[
        user_ratings == 0
    ].index

    recommendations = []

    # =====================================
    # PREDICT UNSEEN FOODS
    # =====================================

    for food_id in unrated_foods:

        weighted_sum = 0

        similarity_sum = 0

        # =================================
        # ITERATE SIMILAR USERS
        # =================================

        for similar_user_id, sim_score in similar_users.items():

            # skip similarity <= 0

            if sim_score <= 0:

                continue

            rating = matrix.loc[
                similar_user_id,
                food_id
            ]

            if rating > 0:

                weighted_sum += (
                    rating * sim_score
                )

                similarity_sum += sim_score

        # =================================
        # PREDICT SCORE
        # =================================

        if similarity_sum > 0:

            predicted_score = (

                weighted_sum
                /
                similarity_sum

            )

            food = Food.query.get(food_id)

            if food:

                # dynamic attribute

                food.predicted_score = round(

                    predicted_score,
                    2

                )

                recommendations.append(food)

    # =====================================
    # SORT BY AI SCORE
    # =====================================

    recommendations = sorted(

        recommendations,

        key=lambda x: x.predicted_score,

        reverse=True

    )

    return recommendations[:top_n]


# =========================================
# ALIAS FOR NUTRITION PLAN
# =========================================

def get_recommendations(user_id, top_n=12):

    return get_top_recommendations(
        user_id,
        top_n
    )