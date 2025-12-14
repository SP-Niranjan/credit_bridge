from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import os
import json
from ml_model import CreditRiskModel
from pdf_generator import generate_credit_report

app = Flask(__name__)
app.config['SECRET_KEY'] = 'creditbridge-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///credit_risk.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['REPORTS_FOLDER'] = 'reports'

db = SQLAlchemy(app)

# ============= DATABASE MODELS =============

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    permissions = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    assessments = db.relationship('CreditAssessment', backref='processor', lazy=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    pan_card = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    profiles = db.relationship('FinancialProfile', backref='user', lazy=True)
    assessments = db.relationship('CreditAssessment', backref='applicant', lazy=True)

class FinancialProfile(db.Model):
    __tablename__ = 'financial_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    monthly_income = db.Column(db.Float, nullable=False)
    monthly_expenses = db.Column(db.Float, nullable=False)
    income_std_dev = db.Column(db.Float)
    upi_transaction_count = db.Column(db.Integer)
    bill_payment_streak = db.Column(db.Integer)
    digital_activity_months = db.Column(db.Integer)
    savings_amount = db.Column(db.Float)
    business_revenue = db.Column(db.Float)
    business_expenses = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    assessments = db.relationship('CreditAssessment', backref='profile', lazy=True)

class CreditAssessment(db.Model):
    __tablename__ = 'credit_assessments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('financial_profiles.id'), nullable=False)
    credit_score = db.Column(db.Integer, nullable=False)
    risk_category = db.Column(db.String(20), nullable=False)
    repayment_probability = db.Column(db.Float, nullable=False)
    features_json = db.Column(db.Text, nullable=False)
    processed_by = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    status = db.Column(db.String(20), default='Pending Review')
    assessment_date = db.Column(db.DateTime, default=datetime.utcnow)

# ============= AUTHENTICATION DECORATORS =============

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            
            employee = Employee.query.get(session['user_id'])
            if not employee:
                return redirect(url_for('login'))
            
            perms = json.loads(employee.permissions)
            if permission not in perms and 'ALL' not in perms:
                return "Access Denied - Insufficient Permissions", 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ============= ROUTES =============

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        employee = Employee.query.filter_by(username=username).first()
        
        if employee and check_password_hash(employee.password_hash, password):
            session['user_id'] = employee.id
            session['username'] = employee.username
            session['name'] = employee.name
            session['role'] = employee.role
            session['permissions'] = employee.permissions
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    total_assessments = CreditAssessment.query.count()
    avg_score = db.session.query(db.func.avg(CreditAssessment.credit_score)).scalar() or 0
    low_risk_count = CreditAssessment.query.filter(CreditAssessment.risk_category == 'Low Risk').count()
    low_risk_percent = (low_risk_count / total_assessments * 100) if total_assessments > 0 else 0
    
    stats = {
        'total': total_assessments,
        'avg_score': round(avg_score, 0),
        'low_risk_percent': round(low_risk_percent, 1)
    }
    
    return render_template('home.html', stats=stats)

@app.route('/assessment/new')
@login_required
@permission_required('create')
def new_assessment():
    return render_template('assessment_form.html')

@app.route('/assessment/create', methods=['POST'])
@login_required
@permission_required('create')
def create_assessment():
    try:
        # Create user
        user = User(
            name=request.form.get('name'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            pan_card=request.form.get('pan_card')
        )
        db.session.add(user)
        db.session.flush()
        
        # Create financial profile
        profile = FinancialProfile(
            user_id=user.id,
            monthly_income=float(request.form.get('monthly_income')),
            monthly_expenses=float(request.form.get('monthly_expenses')),
            income_std_dev=float(request.form.get('income_std_dev', 0)),
            upi_transaction_count=int(request.form.get('upi_transactions', 0)),
            bill_payment_streak=int(request.form.get('bill_payment_streak', 0)),
            digital_activity_months=int(request.form.get('digital_months', 0)),
            savings_amount=float(request.form.get('savings_amount', 0)),
            business_revenue=float(request.form.get('business_revenue', 0)),
            business_expenses=float(request.form.get('business_expenses', 0))
        )
        db.session.add(profile)
        db.session.flush()
        
        # ML Prediction
        model = CreditRiskModel()
        model.load_model()
        
        result = model.predict({
            'monthly_income': profile.monthly_income,
            'monthly_expenses': profile.monthly_expenses,
            'income_std_dev': profile.income_std_dev,
            'upi_transaction_count': profile.upi_transaction_count,
            'bill_payment_streak': profile.bill_payment_streak,
            'digital_activity_months': profile.digital_activity_months,
            'savings_amount': profile.savings_amount,
            'business_revenue': profile.business_revenue,
            'business_expenses': profile.business_expenses
        })
        
        # Create assessment
        assessment = CreditAssessment(
            user_id=user.id,
            profile_id=profile.id,
            credit_score=result['credit_score'],
            risk_category=result['risk_category'],
            repayment_probability=result['repayment_probability'],
            features_json=json.dumps(result['features']),
            processed_by=session['user_id']
        )
        db.session.add(assessment)
        db.session.commit()
        
        return redirect(url_for('view_assessment', assessment_id=assessment.id))
        
    except Exception as e:
        db.session.rollback()
        return f"Error creating assessment: {str(e)}", 500

@app.route('/assessment/<int:assessment_id>')
@login_required
def view_assessment(assessment_id):
    assessment = CreditAssessment.query.get_or_404(assessment_id)
    user = User.query.get(assessment.user_id)
    profile = FinancialProfile.query.get(assessment.profile_id)
    processor = Employee.query.get(assessment.processed_by)
    
    features = json.loads(assessment.features_json)
    
    return render_template('result.html', 
                         assessment=assessment, 
                         user=user, 
                         profile=profile,
                         processor=processor,
                         features=features)

@app.route('/applications')
@login_required
@permission_required('view_all')
def applications():
    assessments = CreditAssessment.query.order_by(CreditAssessment.assessment_date.desc()).all()
    
    applications_data = []
    for assessment in assessments:
        user = User.query.get(assessment.user_id)
        profile = FinancialProfile.query.get(assessment.profile_id)
        processor = Employee.query.get(assessment.processed_by)
        
        applications_data.append({
            'id': assessment.id,
            'name': user.name,
            'score': assessment.credit_score,
            'risk': assessment.risk_category,
            'income': profile.monthly_income,
            'processor': processor.name,
            'date': assessment.assessment_date
        })
    
    return render_template('applications.html', applications=applications_data)

@app.route('/dashboard')
@login_required
@permission_required('analytics')
def dashboard():
    total = CreditAssessment.query.count()
    avg_score = db.session.query(db.func.avg(CreditAssessment.credit_score)).scalar() or 0
    
    low_risk = CreditAssessment.query.filter_by(risk_category='Low Risk').count()
    medium_risk = CreditAssessment.query.filter_by(risk_category='Medium Risk').count()
    high_risk = CreditAssessment.query.filter_by(risk_category='High Risk').count()
    
    recent = CreditAssessment.query.order_by(CreditAssessment.assessment_date.desc()).limit(10).all()
    
    recent_data = []
    for assessment in recent:
        user = User.query.get(assessment.user_id)
        recent_data.append({
            'name': user.name,
            'score': assessment.credit_score,
            'risk': assessment.risk_category,
            'date': assessment.assessment_date.strftime('%Y-%m-%d')
        })
    
    stats = {
        'total': total,
        'avg_score': round(avg_score, 0),
        'low_risk': low_risk,
        'medium_risk': medium_risk,
        'high_risk': high_risk,
        'low_risk_percent': round((low_risk/total*100) if total > 0 else 0, 1),
        'approval_rate': round((low_risk/total*100) if total > 0 else 0, 1)
    }
    
    return render_template('dashboard.html', stats=stats, recent=recent_data)

@app.route('/report/pdf/<int:assessment_id>')
@login_required
def generate_pdf(assessment_id):
    assessment = CreditAssessment.query.get_or_404(assessment_id)
    user = User.query.get(assessment.user_id)
    profile = FinancialProfile.query.get(assessment.profile_id)
    processor = Employee.query.get(assessment.processed_by)
    
    features = json.loads(assessment.features_json)
    
    pdf_path = generate_credit_report(assessment, user, profile, processor, features)
    
    return send_file(pdf_path, as_attachment=True, download_name=f'credit_report_{assessment.id}.pdf')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    employee = Employee.query.filter_by(username=data.get('username')).first()
    
    if employee and check_password_hash(employee.password_hash, data.get('password')):
        return jsonify({'success': True, 'name': employee.name, 'role': employee.role})
    
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/api/assessments')
@login_required
def api_assessments():
    assessments = CreditAssessment.query.all()
    data = [{
        'id': a.id,
        'score': a.credit_score,
        'risk': a.risk_category,
        'date': a.assessment_date.isoformat()
    } for a in assessments]
    
    return jsonify(data)

@app.route('/api/analytics')
@login_required
@permission_required('analytics')
def api_analytics():
    total = CreditAssessment.query.count()
    avg_score = db.session.query(db.func.avg(CreditAssessment.credit_score)).scalar() or 0
    
    low_risk = CreditAssessment.query.filter_by(risk_category='Low Risk').count()
    medium_risk = CreditAssessment.query.filter_by(risk_category='Medium Risk').count()
    high_risk = CreditAssessment.query.filter_by(risk_category='High Risk').count()
    
    return jsonify({
        'total': total,
        'avg_score': round(avg_score, 2),
        'risk_distribution': {
            'low': low_risk,
            'medium': medium_risk,
            'high': high_risk
        }
    })

@app.route('/api/assessment/<int:assessment_id>', methods=['DELETE'])
@login_required
@permission_required('ALL')
def delete_assessment(assessment_id):
    assessment = CreditAssessment.query.get_or_404(assessment_id)
    db.session.delete(assessment)
    db.session.commit()
    
    return jsonify({'success': True})

# ============= INITIALIZATION =============

def init_app():
    # Create directories
    os.makedirs('reports', exist_ok=True)
    os.makedirs('uploads', exist_ok=True)
    
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Seed employee accounts if empty
        if Employee.query.count() == 0:
            employees = [
                {
                    'username': 'admin',
                    'password': 'admin123',
                    'name': 'Admin User',
                    'role': 'Branch Manager',
                    'permissions': json.dumps(['ALL'])
                },
                {
                    'username': 'analyst',
                    'password': 'analyst123',
                    'name': 'Credit Analyst',
                    'role': 'Credit Analyst',
                    'permissions': json.dumps(['view_all', 'create', 'edit', 'analytics'])
                },
                {
                    'username': 'officer',
                    'password': 'officer123',
                    'name': 'Loan Officer',
                    'role': 'Loan Officer',
                    'permissions': json.dumps(['view_own', 'create'])
                },
                {
                    'username': 'viewer',
                    'password': 'viewer123',
                    'name': 'Auditor',
                    'role': 'Auditor',
                    'permissions': json.dumps(['view_all', 'export'])
                }
            ]
            
            for emp_data in employees:
                emp = Employee(
                    username=emp_data['username'],
                    password_hash=generate_password_hash(emp_data['password']),
                    name=emp_data['name'],
                    role=emp_data['role'],
                    permissions=emp_data['permissions']
                )
                db.session.add(emp)
            
            db.session.commit()
            print("✅ Seeded 4 employee accounts")
        
        # Train ML model if not exists
        if not os.path.exists('ml_model.pkl'):
            print("🤖 Training ML model...")
            model = CreditRiskModel()
            accuracy = model.train_model()
            print(f"✅ Model trained with accuracy: {accuracy:.2%}")
        else:
            print("✅ ML model loaded")
        
        print("\n" + "="*60)
        print("🚀 CreditBridge - Credit Risk Assessment System")
        print("="*60)
        print("\n📋 Demo Accounts:")
        print("  1. Username: admin     | Password: admin123")
        print("  2. Username: analyst   | Password: analyst123")
        print("  3. Username: officer   | Password: officer123")
        print("  4. Username: viewer    | Password: viewer123")
        print("\n🌐 Server running at: http://localhost:5000")
        print("="*60 + "\n")

if __name__ == '__main__':
    init_app()
    app.run(debug=True, port=5000)