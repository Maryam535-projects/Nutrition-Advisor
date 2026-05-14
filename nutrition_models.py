import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import os

class NutritionAIModels:
    def __init__(self):
        self.scaler = StandardScaler()
        self.calorie_model = None
        self.disease_model = None
        self.profile_model = None
        self.initialize_models()
    
    def initialize_models(self):
        """Initialize or train AI models"""
        os.makedirs('models', exist_ok=True)
        
        if os.path.exists('models/calorie_model.pkl'):
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
        except:
            print("⚠️  Models not found, training new ones...")
            self.train_models()
    
    def train_models(self):
        """Train all AI models with simulated data"""
        print("🤖 Training AI Models...")
        
        # Generate simulated training data
        X_calorie, y_calorie = self.generate_calorie_data()
        X_disease, y_disease = self.generate_disease_data()
        X_profile, y_profile = self.generate_profile_data()
        
        # Train calorie prediction model
        self.calorie_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.calorie_model.fit(X_calorie, y_calorie)
        
        # Train disease risk model
        self.disease_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.disease_model.fit(X_disease, y_disease)
        
        # Train user profile model
        self.profile_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.profile_model.fit(X_profile, y_profile)
        
        # Save models
        joblib.dump(self.calorie_model, 'models/calorie_model.pkl')
        joblib.dump(self.disease_model, 'models/disease_model.pkl')
        joblib.dump(self.profile_model, 'models/user_profile_model.pkl')
        
        print("✅ AI Models trained and saved successfully!")
    
    def generate_calorie_data(self, n_samples=10000):
        """Generate simulated calorie data"""
        np.random.seed(42)
        
        # Features: age, weight, height, activity_level, bmi, gender, meal_frequency
        X = np.zeros((n_samples, 7))
        
        X[:, 0] = np.random.randint(18, 70, n_samples)  # age
        X[:, 1] = np.random.randint(45, 120, n_samples)  # weight (kg)
        X[:, 2] = np.random.randint(150, 200, n_samples)  # height (cm)
        X[:, 3] = np.random.choice([1.2, 1.375, 1.55, 1.725, 1.9], n_samples)  # activity
        X[:, 4] = X[:, 1] / ((X[:, 2]/100) ** 2)  # bmi
        X[:, 5] = np.random.randint(0, 2, n_samples)  # gender (0=male, 1=female)
        X[:, 6] = np.random.randint(3, 6, n_samples)  # meal frequency
        
        # Target: daily calorie needs using Mifflin-St Jeor Equation
        y = np.zeros(n_samples)
        for i in range(n_samples):
            if X[i, 5] == 0:  # male
                y[i] = 10*X[i, 1] + 6.25*X[i, 2] - 5*X[i, 0] + 5
            else:  # female
                y[i] = 10*X[i, 1] + 6.25*X[i, 2] - 5*X[i, 0] - 161
            
            y[i] *= X[i, 3]  # multiply by activity level
            y[i] += np.random.normal(0, 100)  # add noise
        
        return X, y
    
    def generate_disease_data(self, n_samples=10000):
        """Generate simulated disease risk data"""
        np.random.seed(42)
        
        # Features: age, bmi, cholesterol, blood_pressure, glucose, activity, smoking, family_history
        X = np.zeros((n_samples, 8))
        
        X[:, 0] = np.random.randint(20, 80, n_samples)  # age
        X[:, 1] = np.random.uniform(18, 40, n_samples)  # bmi
        X[:, 2] = np.random.uniform(150, 300, n_samples)  # cholesterol
        X[:, 3] = np.random.uniform(110, 180, n_samples)  # blood pressure
        X[:, 4] = np.random.uniform(70, 200, n_samples)  # glucose
        X[:, 5] = np.random.uniform(0, 1, n_samples)  # activity level (0-1)
        X[:, 6] = np.random.binomial(1, 0.2, n_samples)  # smoking (0/1)
        X[:, 7] = np.random.binomial(1, 0.3, n_samples)  # family history (0/1)
        
        # Calculate disease risk score
        risk_score = (
            0.1 * (X[:, 0] - 40) +  # age factor
            0.2 * (X[:, 1] - 25) +  # bmi factor
            0.15 * (X[:, 2] - 200) / 100 +  # cholesterol
            0.15 * (X[:, 3] - 120) / 60 +  # blood pressure
            0.2 * (X[:, 4] - 100) / 100 +  # glucose
            -0.1 * X[:, 5] +  # activity reduces risk
            0.3 * X[:, 6] +  # smoking increases risk
            0.2 * X[:, 7]    # family history
        )
        
        # Convert to classes: 0=low, 1=medium, 2=high
        y = np.zeros(n_samples, dtype=int)
        y[risk_score > 0.5] = 1
        y[risk_score > 1.5] = 2
        
        return X, y
    
    def generate_profile_data(self, n_samples=10000):
        """Generate user profile data"""
        np.random.seed(42)
        
        # Features: age, bmi, activity_level, goal_weight, current_calories, exercise_hours
        X = np.zeros((n_samples, 6))
        
        X[:, 0] = np.random.randint(18, 65, n_samples)  # age
        X[:, 1] = np.random.uniform(18, 35, n_samples)  # bmi
        X[:, 2] = np.random.uniform(1.2, 1.9, n_samples)  # activity level
        X[:, 3] = np.random.uniform(50, 100, n_samples)  # goal weight
        X[:, 4] = np.random.randint(1200, 3500, n_samples)  # current calories
        X[:, 5] = np.random.uniform(0, 10, n_samples)  # exercise hours
        
        # Determine profiles based on features
        y = np.zeros(n_samples, dtype=int)
        
        for i in range(n_samples):
            if X[i, 1] > 27 and X[i, 4] > 2500:  # high bmi, high calories
                y[i] = 0  # weight loss
            elif X[i, 1] < 22 and X[i, 5] > 5:  # low bmi, high exercise
                y[i] = 1  # muscle gain
            elif X[i, 2] > 1.7 and X[i, 5] > 7:  # high activity and exercise
                y[i] = 3  # athletic
            else:
                y[i] = 2  # maintenance
        
        return X, y
    
    def predict_calorie_needs(self, user_data):
        """Predict daily calorie needs"""
        features = np.array([[
            user_data['age'],
            user_data['weight'],
            user_data['height'],
            user_data['activity_level'],
            user_data['bmi'],
            user_data['gender_numeric'],
            user_data.get('meal_frequency', 4)
        ]])
        
        return self.calorie_model.predict(features)[0]
    
    def predict_disease_risk(self, user_data):
        """Predict disease risk level"""
        features = np.array([[
            user_data['age'],
            user_data['bmi'],
            user_data.get('cholesterol', 200),
            user_data.get('blood_pressure', 120),
            user_data.get('glucose', 90),
            user_data.get('activity_score', 0.5),
            user_data.get('smoking', 0),
            user_data.get('family_history', 0)
        ]])
        
        risk_level = self.disease_model.predict(features)[0]
        return {
            'level': risk_level,
            'label': ['Low', 'Medium', 'High'][risk_level]
        }
    
    def predict_user_profile(self, user_data):
        """Predict user diet profile"""
        features = np.array([[
            user_data['age'],
            user_data['bmi'],
            user_data['activity_level'],
            user_data.get('goal_weight', user_data['weight']),
            user_data.get('current_calories', 2000),
            user_data.get('exercise_hours', 5)
        ]])
        
        profile_id = self.profile_model.predict(features)[0]
        profiles = {
            0: {'name': 'Weight Loss', 'icon': '⚖️', 'focus': 'Calorie deficit'},
            1: {'name': 'Muscle Gain', 'icon': '💪', 'focus': 'Protein surplus'},
            2: {'name': 'Maintenance', 'icon': '🔄', 'focus': 'Balance'},
            3: {'name': 'Athletic', 'icon': '🏃', 'focus': 'Performance'}
        }
        
        return profiles.get(profile_id, profiles[2])
    
    def get_recommendations(self, profile, risk_level):
        """Get personalized recommendations"""
        recommendations = {
            'diet': [],
            'exercise': [],
            'supplements': [],
            'monitoring': []
        }
        
        if profile['name'] == 'Weight Loss':
            recommendations['diet'] = [
                "Calorie deficit of 300-500 calories daily",
                "High protein intake (1.6-2.2g per kg body weight)",
                "Increase fiber intake to 25-30g daily",
                "Limit processed foods and added sugars"
            ]
            recommendations['exercise'] = [
                "150 minutes moderate cardio weekly",
                "Strength training 2-3 times weekly",
                "Incorporate HIIT workouts"
            ]
        
        elif profile['name'] == 'Muscle Gain':
            recommendations['diet'] = [
                "Calorie surplus of 300-500 calories daily",
                "Protein intake: 1.8-2.2g per kg body weight",
                "Carbohydrate timing around workouts",
                "Adequate healthy fats (0.8-1g per kg)"
            ]
            recommendations['exercise'] = [
                "Progressive overload strength training",
                "Focus on compound movements",
                "Adequate recovery between sessions"
            ]
        
        # Add risk-based recommendations
        if risk_level['level'] == 2:  # High risk
            recommendations['monitoring'].extend([
                "Regular blood tests every 3-6 months",
                "Blood pressure monitoring weekly",
                "Consult with healthcare professional"
            ])
        
        return recommendations

# Test the models
if __name__ == '__main__':
    models = NutritionAIModels()
    
    # Test prediction
    test_user = {
        'age': 30,
        'weight': 70,
        'height': 175,
        'activity_level': 1.55,
        'bmi': 22.9,
        'gender_numeric': 0,
        'goal_weight': 68,
        'current_calories': 2200,
        'exercise_hours': 6
    }
    
    calories = models.predict_calorie_needs(test_user)
    risk = models.predict_disease_risk(test_user)
    profile = models.predict_user_profile(test_user)
    
    print(f"Calorie Needs: {calories:.0f}")
    print(f"Risk Level: {risk['label']}")
    print(f"Profile: {profile['name']}")