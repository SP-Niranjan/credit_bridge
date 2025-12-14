import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
from faker import Faker
import warnings
warnings.filterwarnings('ignore')

class CreditRiskModel:
    def __init__(self):
        self.model = LogisticRegression(random_state=42, max_iter=1000)
        self.scaler = StandardScaler()
        self.feature_names = [
            'ISI', 'ECR', 'PCS', 'DAS', 'SDR', 'CHS'
        ]
        self.feature_weights = {
            'ISI': 0.25,
            'ECR': 0.20,
            'PCS': 0.20,
            'DAS': 0.15,
            'SDR': 0.15,
            'CHS': 0.05
        }
    
    def calculate_features(self, profile_data):
        """Calculate behavioral features from financial profile"""
        
        # Income Stability Index (ISI)
        if profile_data['monthly_income'] > 0:
            isi = max(0, 1 - (profile_data['income_std_dev'] / profile_data['monthly_income']))
        else:
            isi = 0
        
        # Expense Control Ratio (ECR)
        if profile_data['monthly_income'] > 0:
            ecr = max(0, (profile_data['monthly_income'] - profile_data['monthly_expenses']) / profile_data['monthly_income'])
        else:
            ecr = 0
        
        # Payment Consistency Score (PCS)
        pcs = min(1.0, profile_data['bill_payment_streak'] / 12)
        
        # Digital Activity Score (DAS)
        upi_component = min(1.0, profile_data['upi_transaction_count'] / 30)
        digital_component = min(1.0, profile_data['digital_activity_months'] / 6)
        das = upi_component * digital_component
        
        # Savings Discipline Ratio (SDR)
        if profile_data['monthly_income'] > 0:
            sdr = min(1.0, profile_data['savings_amount'] / (profile_data['monthly_income'] * 3))
        else:
            sdr = 0
        
        # Cashflow Health Score (CHS)
        if profile_data['business_revenue'] > 0:
            chs = (profile_data['business_revenue'] - profile_data['business_expenses']) / profile_data['business_revenue']
            chs = max(-1, min(1, chs))  # Clamp between -1 and 1
        else:
            chs = 0
        
        return {
            'ISI': round(isi, 4),
            'ECR': round(ecr, 4),
            'PCS': round(pcs, 4),
            'DAS': round(das, 4),
            'SDR': round(sdr, 4),
            'CHS': round(chs, 4)
        }
    
    def calculate_credit_score(self, features):
        """Calculate credit score from features using weighted formula"""
        weighted_score = (
            features['ISI'] * self.feature_weights['ISI'] +
            features['ECR'] * self.feature_weights['ECR'] +
            features['PCS'] * self.feature_weights['PCS'] +
            features['DAS'] * self.feature_weights['DAS'] +
            features['SDR'] * self.feature_weights['SDR'] +
            features['CHS'] * self.feature_weights['CHS']
        )
        
        # Scale to 300-900 range
        credit_score = 300 + (weighted_score * 600)
        return int(credit_score)
    
    def get_risk_category(self, credit_score):
        """Determine risk category based on credit score"""
        if credit_score >= 750:
            return 'Low Risk'
        elif credit_score >= 600:
            return 'Medium Risk'
        else:
            return 'High Risk'
    
    def generate_training_data(self, n_samples=5000):
        """Generate synthetic training data"""
        fake = Faker('en_IN')
        np.random.seed(42)
        
        data = []
        
        for _ in range(n_samples):
            # Generate realistic financial profiles with variations
            income = np.random.uniform(10000, 100000)
            
            # Income stability varies by income level
            if income < 30000:
                income_std = np.random.uniform(income * 0.15, income * 0.35)
            else:
                income_std = np.random.uniform(income * 0.05, income * 0.20)
            
            # Expenses typically 60-90% of income
            expenses = np.random.uniform(income * 0.50, income * 0.85)
            
            # UPI transactions higher for tech-savvy users
            upi_count = int(np.random.gamma(5, 3))  # Gamma distribution for realistic count
            
            # Bill payment streak (0-12 months)
            payment_streak = int(np.random.triangular(0, 8, 12))
            
            # Digital activity months (0-24)
            digital_months = int(np.random.triangular(0, 6, 24))
            
            # Savings (0 to 6 months of income)
            savings = np.random.uniform(0, income * 6) * (np.random.random() > 0.3)  # 70% have savings
            
            # Business revenue/expenses (for self-employed, ~30% of population)
            if np.random.random() > 0.7:
                business_rev = np.random.uniform(income * 0.5, income * 2)
                business_exp = np.random.uniform(business_rev * 0.5, business_rev * 0.9)
            else:
                business_rev = 0
                business_exp = 0
            
            profile = {
                'monthly_income': income,
                'monthly_expenses': expenses,
                'income_std_dev': income_std,
                'upi_transaction_count': upi_count,
                'bill_payment_streak': payment_streak,
                'digital_activity_months': digital_months,
                'savings_amount': savings,
                'business_revenue': business_rev,
                'business_expenses': business_exp
            }
            
            # Calculate features
            features = self.calculate_features(profile)
            
            # Calculate credit score
            credit_score = self.calculate_credit_score(features)
            
            # Determine risk category
            risk_category = self.get_risk_category(credit_score)
            
            # Create training sample
            sample = {
                **features,
                'credit_score': credit_score,
                'risk_category': risk_category,
                'risk_label': 0 if risk_category == 'Low Risk' else (1 if risk_category == 'Medium Risk' else 2)
            }
            
            data.append(sample)
        
        df = pd.DataFrame(data)
        return df
    
    def train_model(self, n_samples=5000):
        """Train the logistic regression model"""
        print(f"Generating {n_samples} training samples...")
        df = self.generate_training_data(n_samples)
        
        # Prepare features and labels
        X = df[self.feature_names].values
        y = df['risk_label'].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        print("Training Logistic Regression model...")
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n{'='*60}")
        print("MODEL TRAINING COMPLETE")
        print(f"{'='*60}")
        print(f"Training Samples: {len(X_train)}")
        print(f"Testing Samples: {len(X_test)}")
        print(f"Accuracy: {accuracy:.2%}")
        print(f"{'='*60}\n")
        
        # Print classification report
        print("Classification Report:")
        print(classification_report(y_test, y_pred, 
                                   target_names=['Low Risk', 'Medium Risk', 'High Risk']))
        
        # Save model and scaler
        joblib.dump(self.model, 'ml_model.pkl')
        joblib.dump(self.scaler, 'scaler.pkl')
        print("✅ Model and scaler saved successfully\n")
        
        return accuracy
    
    def load_model(self):
        """Load trained model and scaler"""
        try:
            self.model = joblib.load('ml_model.pkl')
            self.scaler = joblib.load('scaler.pkl')
            return True
        except:
            print("⚠️  Model files not found. Training new model...")
            self.train_model()
            return True
    
    def predict(self, profile_data):
        """Make prediction for a new applicant"""
        # Calculate features
        features = self.calculate_features(profile_data)
        
        # Calculate credit score using rule-based approach
        credit_score = self.calculate_credit_score(features)
        
        # Get risk category
        risk_category = self.get_risk_category(credit_score)
        
        # Prepare features for ML model
        X = np.array([[features[f] for f in self.feature_names]])
        X_scaled = self.scaler.transform(X)
        
        # Get probability prediction
        probabilities = self.model.predict_proba(X_scaled)[0]
        
        # Repayment probability (inverse of high risk probability)
        repayment_probability = 1 - probabilities[2]  # 1 - P(High Risk)
        
        # Convert features to percentage for display
        features_percentage = {k: round(v * 100, 1) for k, v in features.items()}
        
        return {
            'credit_score': credit_score,
            'risk_category': risk_category,
            'repayment_probability': round(repayment_probability, 4),
            'features': features,
            'features_percentage': features_percentage,
            'probabilities': {
                'low_risk': round(probabilities[0], 4),
                'medium_risk': round(probabilities[1], 4),
                'high_risk': round(probabilities[2], 4)
            }
        }
    
    def get_recommendations(self, features, credit_score):
        """Generate personalized recommendations"""
        positive = []
        improvements = []
        
        # Check each feature
        if features['ISI'] >= 0.7:
            positive.append("Excellent income stability")
        elif features['ISI'] < 0.5:
            improvements.append("Work on stabilizing income sources")
        
        if features['ECR'] >= 0.3:
            positive.append("Good expense management")
        elif features['ECR'] < 0.15:
            improvements.append("Reduce monthly expenses to improve savings")
        
        if features['PCS'] >= 0.7:
            positive.append("Consistent bill payment history")
        elif features['PCS'] < 0.5:
            improvements.append("Maintain regular bill payments for at least 6 months")
        
        if features['DAS'] >= 0.5:
            positive.append("Active digital banking user")
        elif features['DAS'] < 0.3:
            improvements.append("Increase digital transaction frequency")
        
        if features['SDR'] >= 0.5:
            positive.append("Strong savings discipline")
        elif features['SDR'] < 0.25:
            improvements.append("Build emergency savings fund (3-6 months expenses)")
        
        if features['CHS'] > 0.3:
            positive.append("Healthy business cashflow")
        elif features['CHS'] < 0:
            improvements.append("Improve business profitability")
        
        # Loan recommendations based on credit score
        if credit_score >= 750:
            loan_amount = "Up to ₹5,00,000"
            interest_rate = "10-12% per annum"
            tenure = "12-36 months"
        elif credit_score >= 600:
            loan_amount = "Up to ₹2,00,000"
            interest_rate = "14-16% per annum"
            tenure = "6-24 months"
        else:
            loan_amount = "Up to ₹50,000"
            interest_rate = "18-22% per annum"
            tenure = "6-12 months"
        
        return {
            'positive': positive if positive else ["Continue building your financial profile"],
            'improvements': improvements if improvements else ["Maintain current good practices"],
            'loan_amount': loan_amount,
            'interest_rate': interest_rate,
            'tenure': tenure
        }


# Test the model
if __name__ == '__main__':
    model = CreditRiskModel()
    
    # Train model
    accuracy = model.train_model(5000)
    
    # Test prediction
    test_profile = {
        'monthly_income': 45000,
        'monthly_expenses': 30000,
        'income_std_dev': 5000,
        'upi_transaction_count': 25,
        'bill_payment_streak': 10,
        'digital_activity_months': 12,
        'savings_amount': 100000,
        'business_revenue': 0,
        'business_expenses': 0
    }
    
    print("\n" + "="*60)
    print("TEST PREDICTION")
    print("="*60)
    result = model.predict(test_profile)
    print(f"Credit Score: {result['credit_score']}")
    print(f"Risk Category: {result['risk_category']}")
    print(f"Repayment Probability: {result['repayment_probability']:.2%}")
    print(f"\nFeatures:")
    for feature, value in result['features'].items():
        print(f"  {feature}: {value:.2%}")
    print("="*60)