from extensions import db


class UserPreference(db.Model):

    __tablename__ = 'user_preferences'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users_atlet.id')
    )

    food_id = db.Column(
        db.Integer,
        db.ForeignKey('foods_database.id')
    )

    rating = db.Column(db.Integer)