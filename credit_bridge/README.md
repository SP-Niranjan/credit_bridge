# 🚀 CreditBridge - Alternative Credit Risk Assessment System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![ML](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents
- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Machine Learning Model](#machine-learning-model)
- [Demo Accounts](#demo-accounts)
- [Screenshots](#screenshots)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

**CreditBridge** is a production-ready web application that uses Machine Learning to assess creditworthiness for credit-invisible populations in India. Unlike traditional credit scoring systems that rely on CIBIL scores and formal income records, our system analyzes **behavioral financial data** to determine credit risk.

**Tagline:** *Bridging Financial Gaps*

### Key Statistics
- 190+ million credit-invisible Indians
- Targets: Gig workers, daily wage earners, small business owners, students
- AI-powered assessment using 6 behavioral metrics
- Professional PDF reports with bank-grade formatting

## 🎯 Problem Statement

In India, millions of people who manage money responsibly cannot access loans because they lack:
- CIBIL scores
- Salary slips
- Formal income records
- Traditional banking history

This creates a financial inclusion gap where creditworthy individuals are denied opportunities.

## 💡 Solution

CreditBridge solves this by:
1. **Collecting behavioral financial data** (income, expenses, digital activity)
2. **Analyzing with Machine Learning** (6 key behavioral metrics)
3. **Generating credit scores** (300-900 range with risk categories)
4. **Providing professional reports** (PDF with recommendations)

## ✨ Features

### Core Features
- ✅ **AI-Powered Credit Scoring** - Logistic Regression model trained on 5000+ samples
- ✅ **Behavioral Metrics Analysis** - 6 key financial indicators
- ✅ **Professional PDF Reports** - Bank-grade formatting with ReportLab
- ✅ **Role-Based Access Control** - 4 user roles with different permissions
- ✅ **Interactive Dashboard** - Real-time analytics with Chart.js
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile
- ✅ **Secure Authentication** - Password hashing with Werkzeug

### User Roles & Permissions
1. **Branch Manager** (admin) - Full access, all permissions
2. **Credit Analyst** - View all, create, edit, analytics
3. **Loan Officer** - View own, create assessments
4. **Auditor** - View all, export reports

## 🛠️ Technology Stack

### Backend
- **Python 3.8+** - Programming language
- **Flask 3.0** - Web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Database (easily switchable to PostgreSQL/MySQL)

### Machine Learning
- **scikit-learn** - Logistic Regression model
- **pandas** - Data manipulation
- **numpy** - Numerical operations
- **joblib** - Model persistence

### Frontend
- **Jinja2** - Template engine
- **Bootstrap 5** - CSS framework
- **Chart.js** - Data visualizations
- **Vanilla JavaScript** - Client-side interactivity

### PDF Generation
- **ReportLab** - Professional PDF creation

### Data Generation
- **Faker** - Synthetic training data

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/creditbridge.git
cd creditbridge
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Application
```bash
python app.py
```

The application will:
1. Create database and tables
2. Seed 4 demo employee accounts
3. Train the ML model (if not already trained)
4. Start server on `http://localhost:5000`

## 🚀 Usage

### First Time Setup
1. Start the application: `python app.py`
2. Open browser: `http://localhost:5000`
3. Login with any demo account (see below)
4. Explore the dashboard

### Creating an Assessment
1. Login with an account that has 'create' permission
2. Click "New Assessment" from home or navigation
3. Fill in the assessment form:
   - Personal information (name, phone, email, PAN)
   - Financial behavior data (income, expenses, savings)
   - Digital activity (UPI transactions, payment streak)
   - Business data (if self-employed)
4. Submit form
5. View AI-generated results with charts
6. Download professional PDF report

### Viewing Analytics
1. Login with 'analytics' permission
2. Navigate to "Analytics Dashboard"
3. View:
   - Total assessments
   - Average credit score
   - Risk distribution
   - Recent applications

## 🗄️ Database Schema

### Tables

#### 1. employees
```sql
id              INTEGER PRIMARY KEY
username        VARCHAR(50) UNIQUE NOT NULL
password_hash   VARCHAR(256) NOT NULL
name            VARCHAR(100) NOT NULL
role            VARCHAR(50) NOT NULL
permissions     TEXT NOT NULL (JSON format)
created_at      DATETIME
```

#### 2. users (Applicants)
```sql
id          INTEGER PRIMARY KEY
name        VARCHAR(100) NOT NULL
phone       VARCHAR(20) NOT NULL
email       VARCHAR(100)
pan_card    VARCHAR(10)
created_at  DATETIME
```

#### 3. financial_profiles
```sql
id                      INTEGER PRIMARY KEY
user_id                 INTEGER FOREIGN KEY
monthly_income          FLOAT NOT NULL
monthly_expenses        FLOAT NOT NULL
income_std_dev          FLOAT
upi_transaction_count   INTEGER
bill_payment_streak     INTEGER
digital_activity_months INTEGER
savings_amount          FLOAT
business_revenue        FLOAT
business_expenses       FLOAT
created_at              DATETIME
```

#### 4. credit_assessments
```sql
id                      INTEGER PRIMARY KEY
user_id                 INTEGER FOREIGN KEY
profile_id              INTEGER FOREIGN KEY
credit_score            INTEGER NOT NULL
risk_category           VARCHAR(20) NOT NULL
repayment_probability   FLOAT NOT NULL
features_json           TEXT NOT NULL (JSON format)
processed_by            INTEGER FOREIGN KEY
status                  VARCHAR(20) DEFAULT 'Pending Review'
assessment_date         DATETIME
```

## 🌐 API Endpoints

### Authentication
- `GET /` - Redirect to login
- `GET /login` - Login page
- `POST /login` - Process login
- `GET /logout` - Logout

### Dashboard
- `GET /home` - Home dashboard (requires login)
- `GET /assessment/new` - New assessment form
- `POST /assessment/create` - Create assessment
- `GET /assessment/<id>` - View assessment result
- `GET /applications` - List all applications
- `GET /dashboard` - Analytics dashboard

### API Routes (JSON)
- `POST /api/login` - JSON login endpoint
- `GET /api/assessments` - Get all assessments
- `GET /api/analytics` - Get analytics data
- `DELETE /api/assessment/<id>` - Delete assessment

### PDF Generation
- `GET /report/pdf/<id>` - Generate and download PDF

## 🤖 Machine Learning Model

### Model Type
**Logistic Regression** (scikit-learn)

### Features (6 Behavioral Metrics)

1. **Income Stability Index (ISI)** - Weight: 25%
   - Formula: `1 - (income_std_dev / monthly_income)`
   - Measures income consistency

2. **Expense Control Ratio (ECR)** - Weight: 20%
   - Formula: `(monthly_income - monthly_expenses) / monthly_income`
   - Measures savings capacity

3. **Payment Consistency Score (PCS)** - Weight: 20%
   - Formula: `bill_payment_streak / 12`
   - Measures payment reliability

4. **Digital Activity Score (DAS)** - Weight: 15%
   - Formula: `min(upi_transactions/30, 1) × min(digital_months/6, 1)`
   - Measures digital engagement

5. **Savings Discipline Ratio (SDR)** - Weight: 15%
   - Formula: `savings_amount / (monthly_income × 3)`
   - Measures savings habit

6. **Cashflow Health Score (CHS)** - Weight: 5%
   - Formula: `(business_revenue - business_expenses) / business_revenue`
   - Measures business profitability

### Credit Score Calculation
```python
weighted_score = (ISI × 0.25 + ECR × 0.20 + PCS × 0.20 + 
                  DAS × 0.15 + SDR × 0.15 + CHS × 0.05)
credit_score = 300 + (weighted_score × 600)  # Range: 300-900
```

### Risk Categories
- **Low Risk:** Score ≥ 750 (Green)
- **Medium Risk:** Score 600-749 (Orange)
- **High Risk:** Score < 600 (Red)

### Model Performance
- Training samples: 5000
- Accuracy: > 80%
- Synthetic data generated using Faker and NumPy

## 🔑 Demo Accounts

| Username | Password | Role | Permissions |
|----------|----------|------|-------------|
| admin | admin123 | Branch Manager | ALL |
| analyst | analyst123 | Credit Analyst | view_all, create, edit, analytics |
| officer | officer123 | Loan Officer | view_own, create |
| viewer | viewer123 | Auditor | view_all, export |

## 📸 Screenshots

### Login Page
Modern glassmorphism design with demo account credentials

### Home Dashboard
Welcome banner, statistics cards, quick actions, and feature highlights

### Assessment Form
Multi-section form with personal info, financial data, and digital activity

### Results Page
Credit score display, behavioral metrics charts, financial profile, and recommendations

### Applications List
Professional table with all assessments, color-coded risk badges

### Analytics Dashboard
Comprehensive stats, pie chart, line chart, and recent applications

## 🧪 Testing

### Automated Testing
Run the test script:
```bash
python test_system.py
```

Tests include:
- Database creation
- Model training
- Employee account seeding
- Assessment creation
- PDF generation

### Manual Testing Checklist
- [ ] Login with all 4 demo accounts
- [ ] Create new assessment
- [ ] View assessment results
- [ ] Download PDF report
- [ ] View applications list
- [ ] Check analytics dashboard
- [ ] Verify role permissions
- [ ] Test logout functionality

## 📁 Project Structure

```
creditbridge/
├── app.py                      # Main Flask application
├── ml_model.py                 # ML model class
├── pdf_generator.py            # PDF report generator
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
├── test_system.py              # Testing script
├── templates/                  # Jinja2 templates
│   ├── base.html
│   ├── login.html
│   ├── home.html
│   ├── assessment_form.html
│   ├── result.html
│   ├── applications.html
│   └── dashboard.html
├── static/                     # Static assets
│   ├── css/
│   └── js/
├── reports/                    # Generated PDFs
├── uploads/                    # Uploaded documents
├── creditbridge.db             # SQLite database
├── ml_model.pkl               # Trained model
└── scaler.pkl                 # Feature scaler
```

## 🎓 Academic Use

This project is designed for:
- Final year BTech/MTech projects
- Machine Learning demonstrations
- Web development portfolios
- Fintech product presentations

## ⚠️ Disclaimers

1. **Research Prototype:** This is an educational/research system
2. **Not CIBIL Replacement:** Supplements, not replaces traditional scoring
3. **Regulatory Compliance:** Real deployment requires RBI compliance
4. **Human Review Required:** Final decisions need human oversight
5. **Data Privacy:** Follows data protection best practices

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Anthropic AI for development tools
- Bootstrap team for UI framework
- Chart.js for visualizations
- ReportLab for PDF generation
- scikit-learn for ML capabilities

## 📞 Support

For questions or issues:
- Email: support@creditbridge.in
- GitHub Issues: [Create an issue](https://github.com/yourusername/creditbridge/issues)

## 🚀 Future Enhancements

- [ ] Integration with real banking APIs
- [ ] Mobile app (React Native)
- [ ] Advanced ML models (Random Forest, XGBoost)
- [ ] Real-time credit monitoring
- [ ] Blockchain for data integrity
- [ ] Multi-language support
- [ ] SMS/Email notifications
- [ ] Document OCR for automatic data extraction

---

**Built with ❤️ for Financial Inclusion in India**