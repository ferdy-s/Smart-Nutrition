<div align="center">

# AI Collaborative Filtering Nutrition Recommendation System

Sistem rekomendasi nutrisi atlet berbasis Artificial Intelligence menggunakan metode Collaborative Filtering.

</div>

<img width="1918" height="922" alt="image" src="https://github.com/user-attachments/assets/f7b13f16-c101-4ec1-a317-2cfbfb3fd685" />

# Deskripsi Project

Smart Nutrition adalah platform rekomendasi makanan dan nutrisi atlet berbasis web yang dibangun menggunakan Flask dan Collaborative Filtering Recommendation System.

Project ini dirancang untuk membantu atlet mendapatkan rekomendasi makanan berdasarkan:

* preferensi makanan
* pola rating pengguna lain
* fase latihan
* jenis olahraga
* kebutuhan nutrisi harian

Sistem menggunakan pendekatan Collaborative Filtering untuk menghasilkan rekomendasi makanan yang lebih personal dan adaptif.

# Fitur Utama


## Authentication System

* Login
* Register
* Logout
* Session Authentication
* Role Management
* Admin Middleware

## User Dashboard

* Personalized Dashboard
* Nutrition Analytics
* Daily Calories
* Sugar Limit
* Recommendation Summary
* Favorites Foods
* Live Recommendation Activity

## Recommendation Engine

* Collaborative Filtering Recommendation
* User Preference Matching
* Rating Based Recommendation
* Similar User Analysis
* Dynamic Recommendation Score
* Real-time Recommendation Monitoring

## Nutrition Management

* Foods Database
* Nutrition Information
* Calories Tracking
* Sugar Tracking
* Protein Tracking
* Carbohydrates Tracking
* Fat Tracking

## Athlete Management

* Athlete Database
* Sport Type
* Training Phase
* Weight Management
* Nutrition Requirement
* User Activity

## Analytics Dashboard

* Recommendation Acceptance Rate
* Active Athletes
* Average Predicted Score
* Onboarding Completion
* Recommendation Trends
* Live Activity Monitoring
* Realtime Analytics


# Teknologi Yang Digunakan

| Technology       | Description             |
| ---------------- | ----------------------- |
| Python           | Backend Language        |
| Flask            | Web Framework           |
| Flask Login      | Authentication          |
| Flask SQLAlchemy | ORM Database            |
| SQLite           | Database                |
| Pandas           | Dataset Processing      |
| Chart.js         | Analytics Visualization |
| Socket.IO        | Realtime Activity       |
| HTML5            | Frontend Structure      |
| CSS3             | Frontend Styling        |
| JavaScript       | Frontend Interaction    |


# Struktur Project

```bash
smart-nutrition/
│
├── app.py
├── config.py
├── extensions.py
├── requirements.txt
├── dataset.xlsx
├── seed_system.py
│
├── database/
│   └── database.db
│
├── middlewares/
│   └── admin_required.py
│
├── models/
│   ├── user.py
│   ├── food.py
│   └── preference.py
│
├── routes/
│   ├── auth.py
│   ├── dashboard.py
│   ├── profile.py
│   ├── foods.py
│   ├── recommendations.py
│   ├── admin_dashboard.py
│   ├── admin_foods.py
│   ├── admin_athletes.py
│   └── admin_analytics.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/
│
└── templates/
    ├── login.html
    ├── register.html
    ├── user_dashboard.html
    ├── profile.html
    ├── recommendations.html
    ├── admin_dashboard.html
    ├── admin_foods.html
    ├── admin_athletes.html
    └── admin_analytics.html
```


# Cara Menjalankan Project

## 1. Clone Repository

```bash
git clone https://github.com/USERNAME/smart-nutrition.git
```


## 2. Masuk Ke Folder Project

```bash
cd smart-nutrition
```


## 3. Buat Virtual Environment

```bash
python -m venv venv
```


## 4. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / MacOS

```bash
source venv/bin/activate
```


## 5. Install Dependencies

```bash
pip install -r requirements.txt
```


## 6. Generate Database

```bash
python
```

```python
from app import app
from extensions import db

with app.app_context():
    db.create_all()
```


## 7. Import Dataset

```bash
python seed_system.py
```


## 8. Jalankan Project

```bash
python app.py
```


# Default Admin Account

| Email                                                                   | Password      |
| ----------------------------------------------------------------------- | ------------- |
| [admin_ferdy@smartnutrition.com](mailto:admin_ferdy@smartnutrition.com) | adminferdy123 |


# Collaborative Filtering Flow

```text
User Memberikan Rating
        ↓
Preference Disimpan Ke Database
        ↓
Collaborative Filtering Engine
        ↓
Mencari User Similarity
        ↓
Menghitung Recommendation Score
        ↓
Generate Personalized Recommendation
        ↓
Ditampilkan Ke Dashboard
```

# Sistem Recommendation

Sistem menggunakan pendekatan:

## User-Based Collaborative Filtering

Proses recommendation:

1. User memberikan rating makanan
2. Sistem mencari user dengan preferensi serupa
3. Sistem menghitung similarity score
4. Sistem menghasilkan rekomendasi makanan
5. Recommendation ditampilkan secara personalized


# Analytics System

Analytics Dashboard menampilkan:

* Recommendation Accuracy
* Recommendation Acceptance
* User Interaction
* Food Popularity
* Athlete Activity
* Realtime Recommendation Activity
* Recommendation Trend


# Security Features

* Password Hashing
* Authentication Middleware
* Session Management
* Admin Access Control
* Login Protection
* Route Protection


# Realtime Features

Menggunakan Socket.IO untuk:

* Live Recommendation Activity
* Realtime Analytics
* Dynamic Dashboard Updates


# Dataset Information

Dataset digunakan untuk:

* Athlete Information
* Food Preferences
* Nutrition Data
* Collaborative Filtering Training Data

Format dataset:

```text
dataset.xlsx
```


# Preview Dokumentasi

## Login Page

<img width="1918" height="922" alt="image" src="https://github.com/user-attachments/assets/f7b13f16-c101-4ec1-a317-2cfbfb3fd685" />

## User Dashboard

<img width="1900" height="1078" alt="image" src="https://github.com/user-attachments/assets/2567e1d9-8e9f-4251-b43a-f14ca085fc3c" />

## Recommendation Engine

<img width="1901" height="922" alt="image" src="https://github.com/user-attachments/assets/ed8854fd-c063-4245-bd6e-d430c35ba2b1" />

## Foods Database

<img width="1901" height="922" alt="image" src="https://github.com/user-attachments/assets/7bb2d64a-6a40-4e40-8388-8fa12e02f3c0" />

## Athlete Management

<img width="1901" height="922" alt="image" src="https://github.com/user-attachments/assets/6248e190-1ab4-4785-aaca-965791c6fb05" />

## Analytics Dashboard

<img width="1901" height="927" alt="image" src="https://github.com/user-attachments/assets/f23b73f9-58e3-4ce7-b6b8-0905becd5725" />


# Future Improvement

* JWT Authentication
* REST API
* Mobile Application
* Docker Deployment
* PostgreSQL Migration
* Kubernetes Deployment
* Recommendation Explainability
* Machine Learning Pipeline
* AI Nutrition Assistant


# Author

## Ferdy Salsabilla
AI Collaborative Filtering Nutrition Recommendation System Developer
