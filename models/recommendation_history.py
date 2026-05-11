from datetime import datetime

from extensions import db


class RecommendationHistory(db.Model):

    __tablename__ = 'recommendation_history'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # =========================================
    # RELATIONS
    # =========================================

    user_id = db.Column(

        db.Integer,

        db.ForeignKey('users_atlet.id'),

        nullable=False

    )

    food_id = db.Column(

        db.Integer,

        db.ForeignKey('foods_database.id'),

        nullable=False

    )

    # =========================================
    # AI PREDICTION
    # =========================================

    predicted_score = db.Column(
        db.Float,
        nullable=False
    )

    # =========================================
    # USER INTERACTION
    # =========================================

    selected = db.Column(
        db.Boolean,
        default=False
    )

    liked = db.Column(
        db.Boolean,
        default=False
    )

    # =========================================
    # TRACKING TIME
    # =========================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # =========================================
    # RELATIONSHIP
    # =========================================

    user = db.relationship(
        'User',
        backref='recommendation_histories'
    )

    food = db.relationship(
        'Food',
        backref='recommendation_histories'
    )