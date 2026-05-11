from extensions import db


class Food(db.Model):

    __tablename__ = 'foods_database'

    # =========================================
    # PRIMARY KEY
    # =========================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # =========================================
    # BASIC FOOD INFORMATION
    # =========================================

    food_name = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    image = db.Column(
        db.Text,
        nullable=True
    )

    category = db.Column(
        db.String(100),
        nullable=True
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    # =========================================
    # NUTRITION INFORMATION
    # =========================================

    calories = db.Column(
        db.Float,
        default=0
    )

    sugar = db.Column(
        db.Float,
        default=0
    )

    protein = db.Column(
        db.Float,
        default=0
    )

    carbohydrates = db.Column(
        db.Float,
        default=0
    )

    fat = db.Column(
        db.Float,
        default=0
    )

    fiber = db.Column(
        db.Float,
        default=0
    )

    sodium = db.Column(
        db.Float,
        default=0
    )

    # =========================================
    # ATHLETE FILTERING
    # =========================================

    cocok_normal = db.Column(
        db.Boolean,
        default=True
    )

    cocok_cutting = db.Column(
        db.Boolean,
        default=False
    )

    cocok_bulking = db.Column(
        db.Boolean,
        default=False
    )

    low_sugar = db.Column(
        db.Boolean,
        default=False
    )

    high_protein = db.Column(
        db.Boolean,
        default=False
    )

    # =========================================
    # AI / RECOMMENDATION METADATA
    # =========================================

    ai_score = db.Column(
        db.Float,
        default=0
    )

    total_ratings = db.Column(
        db.Integer,
        default=0
    )

    average_rating = db.Column(
        db.Float,
        default=0
    )

    # =========================================
    # RELATIONSHIP
    # =========================================

    preferences = db.relationship(

        'UserPreference',

        backref='food',

        lazy=True,

        cascade='all, delete'

    )

    # =========================================
    # SERIALIZE
    # =========================================

    def to_dict(self):

        return {

            'id': self.id,
            'food_name': self.food_name,
            'image': self.image,
            'category': self.category,
            'description': self.description,

            'calories': self.calories,
            'protein': self.protein,
            'carbohydrates': self.carbohydrates,
            'fat': self.fat,
            'fiber': self.fiber,
            'sugar': self.sugar,
            'sodium': self.sodium,

            'cocok_normal': self.cocok_normal,
            'cocok_cutting': self.cocok_cutting,
            'cocok_bulking': self.cocok_bulking,

            'low_sugar': self.low_sugar,
            'high_protein': self.high_protein,

            'ai_score': self.ai_score,
            'total_ratings': self.total_ratings,
            'average_rating': self.average_rating

        }

    # =========================================
    # STRING REPRESENTATION
    # =========================================

    def __repr__(self):

        return f'<Food {self.food_name}>'