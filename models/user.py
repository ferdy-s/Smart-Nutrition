from extensions import db

from flask_login import UserMixin


class User(
    UserMixin,
    db.Model
):

    __tablename__ = 'users_atlet'

    # =========================================
    # PRIMARY KEY
    # =========================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # =========================================
    # BASIC INFORMATION
    # =========================================

    full_name = db.Column(
        db.String(255),
        nullable=True
    )

    username = db.Column(
        db.String(150),
        nullable=True
    )

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=True
    )

    google_id = db.Column(
        db.String(255),
        unique=True,
        nullable=True
    )

    profile_picture = db.Column(
        db.Text,
        nullable=True
    )

    # =========================================
    # ROLE MANAGEMENT
    # =========================================

    role = db.Column(
        db.String(50),
        default='user'
    )

    # =========================================
    # PROFILE STATUS
    # =========================================

    profile_completed = db.Column(
        db.Boolean,
        default=False
    )

    is_active_user = db.Column(
        db.Boolean,
        default=True
    )

    # =========================================
    # ATHLETE PROFILE
    # =========================================

    weight = db.Column(
        db.Float,
        default=0
    )

    height = db.Column(
        db.Float,
        default=0
    )

    age = db.Column(
        db.Integer,
        default=0
    )

    gender = db.Column(
        db.String(20),
        default=''
    )

    sport_type = db.Column(
        db.String(100),
        default=''
    )

    training_phase = db.Column(
        db.String(100),
        default='Normal Training'
    )

    activity_level = db.Column(
        db.String(100),
        default='Moderate'
    )

    # =========================================
    # NUTRITION PROFILE
    # =========================================

    daily_calories = db.Column(
        db.Float,
        default=0
    )

    protein_target = db.Column(
        db.Float,
        default=0
    )

    carbs_target = db.Column(
        db.Float,
        default=0
    )

    fat_target = db.Column(
        db.Float,
        default=0
    )

    sugar_limit = db.Column(
        db.Float,
        default=0
    )

    water_target = db.Column(
        db.Float,
        default=0
    )

    # =========================================
    # AI RECOMMENDATION SYSTEM
    # =========================================

    recommendation_model = db.Column(
        db.String(100),
        default='Collaborative Filtering'
    )

    onboarding_completed = db.Column(
        db.Boolean,
        default=False
    )

    recommendation_score = db.Column(
        db.Float,
        default=0
    )

    # =========================================
    # ACCOUNT METADATA
    # =========================================

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    last_login = db.Column(
        db.DateTime,
        nullable=True
    )

    # =========================================
    # RELATIONSHIP
    # =========================================

    preferences = db.relationship(

        'UserPreference',

        backref='user',

        lazy=True,

        cascade='all, delete-orphan'

    )

    # =========================================
    # HELPER METHODS
    # =========================================

    @property
    def display_name(self):

        if self.full_name:

            return self.full_name

        if self.username:

            return self.username

        return self.email.split('@')[0]

    @property
    def avatar(self):

        if self.profile_picture:

            return self.profile_picture

        return '/static/images/default-avatar.png'

    # =========================================
    # STRING REPRESENTATION
    # =========================================

    def __repr__(self):

        return f'<User {self.email}>'