from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import joblib
import os
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'ai_nutrition_secret_2024'

# ===============================
# AI Prediction Models
# ===============================
class NutritionPredictor:
    def __init__(self):
        self.calorie_model = None
        self.disease_model = None
        self.profile_model = None
        self.nutrition_db = self.load_nutrition_database()
        self.initialize_models()
    
    def load_nutrition_database(self):
        """Load food nutrition database"""
        return {
            'apple': {'calories': 52, 'carbs': 14, 'protein': 0.3, 'fat': 0.2, 'category': 'fruit'},
            'banana': {'calories': 89, 'carbs': 23, 'protein': 1.1, 'fat': 0.3, 'category': 'fruit'},
            'orange': {'calories': 47, 'carbs': 12, 'protein': 0.9, 'fat': 0.1, 'category': 'fruit'},
            'chicken breast': {'calories': 165, 'carbs': 0, 'protein': 31, 'fat': 3.6, 'category': 'protein'},
            'chicken': {'calories': 165, 'carbs': 0, 'protein': 31, 'fat': 3.6, 'category': 'protein'},
            'beef': {'calories': 250, 'carbs': 0, 'protein': 26, 'fat': 17, 'category': 'protein'},
            'fish': {'calories': 206, 'carbs': 0, 'protein': 22, 'fat': 13, 'category': 'protein'},
            'salmon': {'calories': 208, 'carbs': 0, 'protein': 20, 'fat': 13, 'category': 'protein'},
            'rice': {'calories': 130, 'carbs': 28, 'protein': 2.7, 'fat': 0.3, 'category': 'grain'},
            'brown rice': {'calories': 111, 'carbs': 23, 'protein': 2.6, 'fat': 0.9, 'category': 'grain'},
            'bread': {'calories': 265, 'carbs': 49, 'protein': 9, 'fat': 3.2, 'category': 'grain'},
            'pasta': {'calories': 131, 'carbs': 25, 'protein': 5, 'fat': 1.1, 'category': 'grain'},
            'potato': {'calories': 77, 'carbs': 17, 'protein': 2, 'fat': 0.1, 'category': 'vegetable'},
            'broccoli': {'calories': 34, 'carbs': 7, 'protein': 2.8, 'fat': 0.4, 'category': 'vegetable'},
            'carrot': {'calories': 41, 'carbs': 10, 'protein': 0.9, 'fat': 0.2, 'category': 'vegetable'},
            'spinach': {'calories': 23, 'carbs': 4, 'protein': 2.9, 'fat': 0.4, 'category': 'vegetable'},
            'egg': {'calories': 155, 'carbs': 1.1, 'protein': 13, 'fat': 11, 'category': 'protein'},
            'eggs': {'calories': 155, 'carbs': 1.1, 'protein': 13, 'fat': 11, 'category': 'protein'},
            'milk': {'calories': 42, 'carbs': 5, 'protein': 3.4, 'fat': 1, 'category': 'dairy'},
            'cheese': {'calories': 402, 'carbs': 1.3, 'protein': 25, 'fat': 33, 'category': 'dairy'},
            'yogurt': {'calories': 59, 'carbs': 4, 'protein': 10, 'fat': 0.4, 'category': 'dairy'},
            'butter': {'calories': 717, 'carbs': 0.1, 'protein': 0.9, 'fat': 81, 'category': 'dairy'},
            'olive oil': {'calories': 884, 'carbs': 0, 'protein': 0, 'fat': 100, 'category': 'fat'},
            'avocado': {'calories': 160, 'carbs': 9, 'protein': 2, 'fat': 15, 'category': 'fruit'},
            'nuts': {'calories': 607, 'carbs': 21, 'protein': 20, 'fat': 54, 'category': 'protein'},
            'chocolate': {'calories': 546, 'carbs': 61, 'protein': 4.9, 'fat': 31, 'category': 'snack'},
            'pizza': {'calories': 266, 'carbs': 33, 'protein': 11, 'fat': 10, 'category': 'grain'},
            'burger': {'calories': 295, 'carbs': 30, 'protein': 17, 'fat': 12, 'category': 'protein'},
            'fries': {'calories': 312, 'carbs': 41, 'protein': 3.4, 'fat': 15, 'category': 'vegetable'},
            'soda': {'calories': 41, 'carbs': 11, 'protein': 0, 'fat': 0, 'category': 'beverage'},
            'coffee': {'calories': 2, 'carbs': 0, 'protein': 0.3, 'fat': 0, 'category': 'beverage'},
            'tea': {'calories': 1, 'carbs': 0, 'protein': 0, 'fat': 0, 'category': 'beverage'},
            'water': {'calories': 0, 'carbs': 0, 'protein': 0, 'fat': 0, 'category': 'beverage'}
        }
    
    def initialize_models(self):
        """Initialize or train AI models"""
        os.makedirs('models', exist_ok=True)
        
        if os.path.exists('models/calorie_model.pkl') and \
           os.path.exists('models/disease_model.pkl') and \
           os.path.exists('models/profile_model.pkl'):
            self.load_models()
        else:
            self.train_models()
    
    def load_models(self):
        """Load trained models"""
        try:
            self.calorie_model = joblib.load('models/calorie_model.pkl')
            self.disease_model = joblib.load('models/disease_model.pkl')
            self.profile_model = joblib.load('models/user_profile_model.pkl')
            print("✅ AI Models loaded successfully")
        except Exception as e:
            print(f"⚠️ Error loading models: {e}")
            self.train_models()
    
    def train_models(self):
        """Train AI models with comprehensive data"""
        print("🤖 Training AI Models...")
        
        # Generate comprehensive training data
        np.random.seed(42)
        n_samples = 5000
        
        # ===== Calorie Model Training =====
        X_calorie = np.zeros((n_samples, 8))
        y_calorie = np.zeros(n_samples)
        
        for i in range(n_samples):
            age = np.random.randint(18, 70)
            weight = np.random.randint(45, 120)
            height = np.random.randint(150, 200)
            gender = np.random.randint(0, 2)  # 0=male, 1=female
            activity = np.random.choice([1.2, 1.375, 1.55, 1.725, 1.9])
            bmi = weight / ((height/100) ** 2)
            meal_freq = np.random.randint(3, 6)
            exercise_hours = np.random.uniform(0, 10)
            
            X_calorie[i] = [age, weight, height, gender, activity, bmi, meal_freq, exercise_hours]
            
            # Calculate BMR (Mifflin-St Jeor Equation)
            if gender == 0:  # male
                bmr = 10*weight + 6.25*height - 5*age + 5
            else:  # female
                bmr = 10*weight + 6.25*height - 5*age - 161
            
            y_calorie[i] = bmr * activity + np.random.normal(0, 100)
        
        self.calorie_model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
        self.calorie_model.fit(X_calorie, y_calorie)
        
        # ===== Disease Risk Model Training =====
        X_disease = np.zeros((n_samples, 10))
        y_disease = np.zeros(n_samples, dtype=int)
        
        for i in range(n_samples):
            age = np.random.randint(20, 80)
            bmi = np.random.uniform(18, 40)
            cholesterol = np.random.uniform(150, 300)
            bp = np.random.uniform(110, 180)
            glucose = np.random.uniform(70, 200)
            activity_score = np.random.uniform(0, 1)
            smoking = np.random.binomial(1, 0.2)
            family_history = np.random.binomial(1, 0.3)
            stress_level = np.random.uniform(0, 1)
            sleep_hours = np.random.uniform(4, 10)
            
            X_disease[i] = [age, bmi, cholesterol, bp, glucose, activity_score, 
                           smoking, family_history, stress_level, sleep_hours]
            
            # Calculate risk score
            risk_score = (
                0.08 * (age - 40) +
                0.15 * (bmi - 25) +
                0.12 * (cholesterol - 200)/100 +
                0.12 * (bp - 120)/60 +
                0.15 * (glucose - 100)/100 +
                -0.1 * activity_score +
                0.25 * smoking +
                0.18 * family_history +
                0.1 * stress_level +
                -0.08 * (sleep_hours - 7)
            )
            
            # Convert to classes
            if risk_score < 0.3:
                y_disease[i] = 0  # Low
            elif risk_score < 1.0:
                y_disease[i] = 1  # Medium
            else:
                y_disease[i] = 2  # High
        
        self.disease_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.disease_model.fit(X_disease, y_disease)
        
        # ===== User Profile Model Training =====
        X_profile = np.zeros((n_samples, 7))
        y_profile = np.zeros(n_samples, dtype=int)
        
        for i in range(n_samples):
            age = np.random.randint(18, 65)
            bmi = np.random.uniform(18, 35)
            activity = np.random.uniform(1.2, 1.9)
            goal_weight = np.random.uniform(50, 100)
            current_calories = np.random.randint(1200, 3500)
            exercise_hours = np.random.uniform(0, 10)
            body_fat = np.random.uniform(10, 40)
            
            X_profile[i] = [age, bmi, activity, goal_weight, current_calories, exercise_hours, body_fat]
            
            # Determine profile
            if bmi > 27 and current_calories > 2500:
                y_profile[i] = 0  # Weight Loss
            elif bmi < 22 and exercise_hours > 5:
                y_profile[i] = 1  # Muscle Gain
            elif activity > 1.7 and exercise_hours > 7:
                y_profile[i] = 3  # Athletic
            else:
                y_profile[i] = 2  # Maintenance
        
        self.profile_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.profile_model.fit(X_profile, y_profile)
        
        # Save models
        joblib.dump(self.calorie_model, 'models/calorie_model.pkl')
        joblib.dump(self.disease_model, 'models/disease_model.pkl')
        joblib.dump(self.profile_model, 'models/user_profile_model.pkl')
        
        print("✅ AI Models trained and saved successfully!")
    
    def predict_calorie_needs(self, user_data):
        """Predict daily calorie needs using AI"""
        gender_numeric = 0 if user_data['gender'] == 'male' else 1
        
        features = np.array([[
            user_data['age'],
            user_data['weight'],
            user_data['height'],
            gender_numeric,  # gender encoding
            user_data['activity_level'],
            user_data['bmi'],
            4,  # meal frequency (default)
            5   # exercise hours (default)
        ]])
        
        return int(self.calorie_model.predict(features)[0])
    
    def predict_disease_risk(self, user_data, nutrition_data):
        """Predict disease risk using AI"""
        features = np.array([[
            user_data['age'],
            user_data['bmi'],
            200,  # cholesterol (default)
            120,  # blood pressure (default)
            90,   # glucose (default)
            user_data['activity_level'] / 2,  # activity score
            0,    # smoking (default: no)
            0,    # family history (default: no)
            0.5,  # stress level (default: medium)
            7     # sleep hours (default)
        ]])
        
        risk_level = self.disease_model.predict(features)[0]
        risk_labels = ['Low Risk', 'Medium Risk', 'High Risk']
        
        # Get disease predictions based on risk
        diseases = {
            0: ['Good health maintenance needed'],
            1: ['Potential for Type 2 Diabetes', 'Cardiovascular issues', 'Hypertension risk'],
            2: ['High risk of Diabetes', 'Heart Disease', 'Hypertension', 'Obesity-related issues', 'Metabolic syndrome']
        }
        
        # Get recommendations
        recommendations = {
            'diet': self.get_diet_recommendations(risk_level, nutrition_data),
            'exercise': self.get_exercise_recommendations(risk_level, user_data),
            'lifestyle': self.get_lifestyle_recommendations(risk_level)
        }
        
        return {
            'risk_level': risk_labels[risk_level],
            'risk_score': int(risk_level),
            'potential_diseases': diseases[risk_level],
            'recommendations': recommendations
        }
    
    def predict_user_profile(self, user_data, nutrition_data):
        """Predict user diet profile using AI"""
        features = np.array([[
            user_data['age'],
            user_data['bmi'],
            user_data['activity_level'],
            user_data['weight'],  # goal weight = current weight for prediction
            nutrition_data['calories'],
            5,  # exercise hours (default)
            25  # body fat % (default)
        ]])
        
        profile_id = self.profile_model.predict(features)[0]
        
        profiles = {
            0: {'name': 'Weight Loss', 'color': 'primary', 'icon': '⚖️', 'focus': 'Calorie deficit'},
            1: {'name': 'Muscle Gain', 'color': 'success', 'icon': '💪', 'focus': 'Protein surplus'},
            2: {'name': 'Maintenance', 'color': 'info', 'icon': '🔄', 'focus': 'Balance'},
            3: {'name': 'Athletic', 'color': 'warning', 'icon': '🏃', 'focus': 'Performance'}
        }
        
        return profiles.get(profile_id, profiles[2])
    
    def analyze_food_intake(self, food_input):
        """Analyze food intake and calculate nutrition"""
        food_items = [f.strip().lower() for f in food_input.split(',') if f.strip()]
        
        total_calories = 0
        total_carbs = 0
        total_protein = 0
        total_fat = 0
        food_details = []
        
        for food in food_items:
            # Try to find exact match or partial match
            found = False
            for db_food, data in self.nutrition_db.items():
                if db_food in food or food in db_food:
                    total_calories += data['calories']
                    total_carbs += data['carbs']
                    total_protein += data['protein']
                    total_fat += data['fat']
                    food_details.append({
                        'name': db_food.title(),
                        'calories': data['calories'],
                        'category': data['category']
                    })
                    found = True
                    break
            
            # If not found, estimate
            if not found:
                estimated = self.estimate_food_nutrition(food)
                total_calories += estimated['calories']
                total_carbs += estimated['carbs']
                total_protein += estimated['protein']
                total_fat += estimated['fat']
                food_details.append({
                    'name': food.title(),
                    'calories': estimated['calories'],
                    'category': estimated['category']
                })
        
        # Ensure minimum values for realistic analysis
        if total_calories < 500:
            total_calories = 1800  # Default minimum
            total_carbs = 200
            total_protein = 70
            total_fat = 60
        
        return {
            'calories': int(total_calories),
            'carbs': int(total_carbs),
            'protein': int(total_protein),
            'fat': int(total_fat),
            'food_items': food_details
        }
    
    def estimate_food_nutrition(self, food_item):
        """Estimate nutrition for unknown foods"""
        food_lower = food_item.lower()
        
        # Categorize and estimate
        if any(word in food_lower for word in ['fruit', 'apple', 'banana', 'berry', 'orange']):
            category = 'fruit'
            calories = 50
            carbs = 12
            protein = 0.5
            fat = 0.2
        elif any(word in food_lower for word in ['vegetable', 'broccoli', 'carrot', 'spinach', 'salad']):
            category = 'vegetable'
            calories = 25
            carbs = 5
            protein = 2
            fat = 0.3
        elif any(word in food_lower for word in ['meat', 'chicken', 'beef', 'fish', 'pork', 'protein']):
            category = 'protein'
            calories = 150
            carbs = 0
            protein = 25
            fat = 5
        elif any(word in food_lower for word in ['grain', 'rice', 'bread', 'pasta', 'cereal']):
            category = 'grain'
            calories = 100
            carbs = 20
            protein = 3
            fat = 1
        elif any(word in food_lower for word in ['dairy', 'milk', 'cheese', 'yogurt']):
            category = 'dairy'
            calories = 80
            carbs = 5
            protein = 4
            fat = 5
        elif any(word in food_lower for word in ['snack', 'chips', 'chocolate', 'cookie', 'cake']):
            category = 'snack'
            calories = 200
            carbs = 25
            protein = 2
            fat = 10
        else:
            category = 'other'
            calories = 100
            carbs = 15
            protein = 5
            fat = 3
        
        return {
            'calories': calories,
            'carbs': carbs,
            'protein': protein,
            'fat': fat,
            'category': category
        }
    
    def get_diet_recommendations(self, risk_level, nutrition_data):
        """Get personalized diet recommendations"""
        if risk_level == 2:  # High risk
            return [
                "Reduce sugar and processed food intake by 50%",
                "Increase vegetable consumption to 5+ servings/day",
                "Limit red meat to once per week",
                "Choose whole grains over refined grains",
                "Reduce sodium intake to <1500mg daily"
            ]
        elif risk_level == 1:  # Medium risk
            return [
                "Balance macronutrients (40% carbs, 30% protein, 30% fat)",
                "Include 3-4 servings of vegetables daily",
                "Stay hydrated (2-3 liters of water daily)",
                "Include healthy fats (avocado, nuts, olive oil)"
            ]
        else:  # Low risk
            return [
                "Maintain current balanced diet",
                "Continue variety in food choices",
                "Monitor portion sizes",
                "Include probiotic-rich foods"
            ]
    
    def get_exercise_recommendations(self, risk_level, user_data):
        """Get personalized exercise recommendations"""
        if risk_level == 2:  # High risk
            return [
                "Start with 30 minutes of moderate exercise daily",
                "Include strength training 2-3 times per week",
                "Consider low-impact exercises (swimming, cycling)",
                "Consult with fitness trainer for personalized plan"
            ]
        elif risk_level == 1:  # Medium risk
            return [
                "150 minutes of moderate exercise per week",
                "Include walking 10,000 steps daily",
                "Add flexibility training (yoga, stretching)",
                "Gradually increase intensity"
            ]
        else:  # Low risk
            return [
                "Maintain regular exercise routine",
                "Try new physical activities for variety",
                "Include high-intensity interval training (HIIT)",
                "Focus on consistency over intensity"
            ]
    
    def get_lifestyle_recommendations(self, risk_level):
        """Get lifestyle recommendations"""
        if risk_level == 2:  # High risk
            return [
                "Regular health checkups every 3-6 months",
                "Monitor blood pressure weekly",
                "Reduce stress through meditation/yoga",
                "Aim for 7-8 hours of quality sleep",
                "Limit alcohol consumption"
            ]
        elif risk_level == 1:  # Medium risk
            return [
                "Annual comprehensive health checkup",
                "Maintain consistent sleep schedule (7-8 hours)",
                "Practice stress management techniques",
                "Stay socially active"
            ]
        else:  # Low risk
            return [
                "Continue healthy lifestyle habits",
                "Regular health monitoring",
                "Maintain work-life balance",
                "Stay updated with preventive healthcare"
            ]
    
    def generate_diet_plan(self, profile_name, calorie_needs, user_data):
        """Generate personalized diet plan"""
        plans = {
            'Weight Loss': {
                'breakfast': "Oatmeal with berries and nuts (300 cal)",
                'lunch': "Grilled chicken salad with avocado (400 cal)",
                'dinner': "Baked salmon with roasted vegetables (450 cal)",
                'snacks': ["Greek yogurt (150 cal)", "Apple with almond butter (200 cal)"],
                'hydration': "2-3 liters of water daily",
                'total_calories': 1500
            },
            'Muscle Gain': {
                'breakfast': "Protein shake with banana and oats (500 cal)",
                'lunch': "Chicken rice bowl with vegetables (600 cal)",
                'dinner': "Lean steak with sweet potato and greens (700 cal)",
                'snacks': ["Protein bar (250 cal)", "Cottage cheese with fruits (300 cal)"],
                'hydration': "3+ liters of water daily",
                'total_calories': 2350
            },
            'Maintenance': {
                'breakfast': "Eggs with whole wheat toast and avocado (400 cal)",
                'lunch': "Quinoa salad with chickpeas and vegetables (450 cal)",
                'dinner': "Grilled fish with brown rice and asparagus (500 cal)",
                'snacks': ["Mixed nuts (200 cal)", "Fruit smoothie (250 cal)"],
                'hydration': "2 liters of water daily",
                'total_calories': 1800
            },
            'Athletic': {
                'breakfast': "Smoothie bowl with protein powder and fruits (550 cal)",
                'lunch': "Turkey wrap with whole grain and vegetables (600 cal)",
                'dinner': "Lean meat with complex carbs and greens (650 cal)",
                'snacks': ["Energy balls (300 cal)", "Protein shake (250 cal)"],
                'hydration': "3-4 liters of water daily",
                'total_calories': 2350
            }
        }
        
        base_plan = plans.get(profile_name, plans['Maintenance'])
        
        # Adjust portions based on calorie needs
        calorie_ratio = calorie_needs / base_plan['total_calories']
        
        return {
            'profile': profile_name,
            'meals': base_plan,
            'daily_calorie_target': int(calorie_needs),
            'weekly_plan': self.generate_weekly_plan(profile_name),
            'macronutrient_ratio': self.get_macronutrient_ratio(profile_name)
        }
    
    def generate_weekly_plan(self, profile_name):
        """Generate weekly workout plan"""
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        if profile_name == 'Weight Loss':
            workouts = ["Cardio (30 min)", "Strength Training", "HIIT", "Active Rest", "Cardio (45 min)", "Yoga", "Rest"]
        elif profile_name == 'Muscle Gain':
            workouts = ["Chest & Triceps", "Back & Biceps", "Legs", "Shoulders & Abs", "Full Body", "Active Recovery", "Rest"]
        elif profile_name == 'Athletic':
            workouts = ["Intense Training", "Skill Work", "Conditioning", "Recovery", "Peak Performance", "Active Rest", "Full Rest"]
        else:  # Maintenance
            workouts = ["Balance Workout", "Cardio", "Strength", "Flexibility", "Mixed", "Light Activity", "Rest"]
        
        weekly_plan = {}
        for i, day in enumerate(days):
            weekly_plan[day] = {
                'workout': workouts[i],
                'focus': 'Nutrition tracking' if i % 2 == 0 else 'Performance metrics',
                'duration': '45-60 minutes'
            }
        
        return weekly_plan
    
    def get_macronutrient_ratio(self, profile_name):
        """Get macronutrient ratio for profile"""
        ratios = {
            'Weight Loss': {'carbs': 40, 'protein': 35, 'fat': 25},
            'Muscle Gain': {'carbs': 45, 'protein': 30, 'fat': 25},
            'Maintenance': {'carbs': 50, 'protein': 25, 'fat': 25},
            'Athletic': {'carbs': 55, 'protein': 25, 'fat': 20}
        }
        return ratios.get(profile_name, ratios['Maintenance'])

# ===============================
# Initialize AI Predictor
# ===============================
predictor = NutritionPredictor()

# ===============================
# Helper Functions
# ===============================
def calculate_bmi(weight, height):
    """Calculate BMI"""
    height_m = height / 100
    return round(weight / (height_m ** 2), 1)

def get_bmi_category(bmi):
    """Get BMI category"""
    if bmi < 18.5:
        return {'category': 'Underweight', 'color': 'warning'}
    elif 18.5 <= bmi < 25:
        return {'category': 'Normal', 'color': 'success'}
    elif 25 <= bmi < 30:
        return {'category': 'Overweight', 'color': 'warning'}
    else:
        return {'category': 'Obese', 'color': 'danger'}

def generate_ai_insights(user_data, nutrition_data, disease_risk):
    """Generate AI insights and recommendations"""
    insights = []
    
    # Calorie insight
    if nutrition_data['calories'] < 1200:
        insights.append({
            'type': 'warning',
            'icon': '⚠️',
            'title': 'Low Calorie Intake',
            'message': 'Your calorie intake is very low. Consider increasing nutrient-dense foods.'
        })
    elif nutrition_data['calories'] > 3000:
        insights.append({
            'type': 'warning',
            'icon': '⚠️',
            'title': 'High Calorie Intake',
            'message': 'Consider balancing your calorie intake for better weight management.'
        })
    
    # Protein insight
    protein_per_kg = nutrition_data['protein'] / user_data['weight']
    if protein_per_kg < 0.8:
        insights.append({
            'type': 'info',
            'icon': '💪',
            'title': 'Increase Protein',
            'message': f'Current: {protein_per_kg:.1f}g/kg. Aim for 1.2-1.6g/kg for optimal health.'
        })
    
    # Risk-based insights
    if disease_risk['risk_score'] == 2:  # High risk
        insights.append({
            'type': 'danger',
            'icon': '❤️',
            'title': 'Health Priority',
            'message': 'Focus on preventive measures. Regular monitoring recommended.'
        })
    
    # BMI insight
    if user_data['bmi'] > 25:
        insights.append({
            'type': 'warning',
            'icon': '⚖️',
            'title': 'Weight Management',
            'message': 'Consider gradual weight loss through diet and exercise.'
        })
    
    return insights

# ===============================
# Flask Routes
# ===============================
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_nutrition():
    """Analyze user input using AI"""
    try:
        # Get user data
        user_data = {
            'age': int(request.form.get('age', 25)),
            'weight': float(request.form.get('weight', 70)),
            'height': float(request.form.get('height', 170)),
            'gender': request.form.get('gender', 'male'),
            'activity_level': float(request.form.get('activity_level', 1.55)),
        }
        
        # Calculate BMI
        user_data['bmi'] = calculate_bmi(user_data['weight'], user_data['height'])
        
        # Get food input
        food_input = request.form.get('food_items', '')
        
        # ===== AI PREDICTIONS =====
        
        # 1. Analyze food intake
        nutrition_data = predictor.analyze_food_intake(food_input)
        
        # 2. Predict calorie needs
        calorie_needs = predictor.predict_calorie_needs(user_data)
        
        # 3. Predict user profile
        user_profile = predictor.predict_user_profile(user_data, nutrition_data)
        
        # 4. Predict disease risk
        disease_risk = predictor.predict_disease_risk(user_data, nutrition_data)
        
        # 5. Generate diet plan
        diet_plan = predictor.generate_diet_plan(
            user_profile['name'], 
            calorie_needs, 
            user_data
        )
        
        # 6. Generate AI insights
        ai_insights = generate_ai_insights(user_data, nutrition_data, disease_risk)
        
        # ===== PREPARE RESULTS =====
        results = {
            'user_data': user_data,
            'calorie_analysis': {
                'consumed': nutrition_data['calories'],
                'required': calorie_needs,
                'difference': calorie_needs - nutrition_data['calories'],
                'nutrition_breakdown': {
                    'carbs': nutrition_data['carbs'],
                    'protein': nutrition_data['protein'],
                    'fat': nutrition_data['fat']
                },
                'food_items': nutrition_data['food_items']
            },
            'user_profile': user_profile,
            'disease_risk': disease_risk,
            'diet_plan': diet_plan,
            'bmi_category': get_bmi_category(user_data['bmi']),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ai_insights': ai_insights
        }
        
        # Store in session
        session['last_analysis'] = results
        
        return render_template('results.html', results=results)
    
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    if 'last_analysis' in session:
        return render_template('dashboard.html', analysis=session['last_analysis'])
    return redirect('/')

@app.route('/api/predict_calories', methods=['POST'])
def api_predict_calories():
    """API endpoint for calorie prediction"""
    data = request.json
    user_data = {
        'age': data.get('age', 25),
        'weight': data.get('weight', 70),
        'height': data.get('height', 170),
        'gender': data.get('gender', 'male'),
        'activity_level': data.get('activity_level', 1.55)
    }
    user_data['bmi'] = calculate_bmi(user_data['weight'], user_data['height'])
    
    calorie_needs = predictor.predict_calorie_needs(user_data)
    
    return jsonify({
        'calorie_needs': int(calorie_needs),
        'bmi': user_data['bmi'],
        'bmi_category': get_bmi_category(user_data['bmi'])['category']
    })

# ===============================
# Run Application
# ===============================
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🤖 AI NUTRITION PREDICTION SYSTEM")
    print("="*60)
    print("✅ AI Models: Ready")
    print("📊 Database: Loaded")
    print("🌐 Starting server: http://127.0.0.1:5000")
    print("="*60)
    
    app.run(debug=True, host='127.0.0.1', port=5000)