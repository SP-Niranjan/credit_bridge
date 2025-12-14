# 🚀 Quick Setup Guide - CreditBridge

## ⚡ Quick Start (5 Minutes)

### Step 1: Install Python
Make sure you have Python 3.8 or higher installed:
```bash
python --version
# or
python3 --version
```

### Step 2: Create Project Directory
```bash
mkdir creditbridge
cd creditbridge
```

### Step 3: Save All Files
Save all the provided files in the following structure:
```
creditbridge/
├── app.py
├── ml_model.py
├── pdf_generator.py
├── requirements.txt
├── README.md
├── test_system.py
└── templates/
    ├── base.html
    ├── login.html
    ├── home.html
    ├── assessment_form.html
    ├── result.html
    ├── applications.html
    └── dashboard.html
```

### Step 4: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 5: Install Dependencies
```bash
pip install -r requirements.txt
```

Wait for all packages to install (this may take 2-3 minutes).

### Step 6: Run the Application
```bash
python app.py
```

You should see:
```
🤖 Training ML model...
✅ Model trained with accuracy: 82.50%
✅ Seeded 4 employee accounts

============================================================
🚀 CreditBridge - Alternative Credit Risk Assessment
============================================================

📋 Demo Accounts:
  1. Username: admin     | Password: admin123
  2. Username: analyst   | Password: analyst123
  3. Username: officer   | Password: officer123
  4. Username: viewer    | Password: viewer123

🌐 Server running at: http://localhost:5000
============================================================
```

### Step 7: Open Browser
Navigate to: **http://localhost:5000**

### Step 8: Login
Use any demo account:
- **admin** / **admin123** (Full access)
- **analyst** / **analyst123** (Most features)
- **officer** / **officer123** (Create assessments)
- **viewer** / **viewer123** (View only)

## 🎯 First Assessment

1. Click "New Assessment" button
2. Fill in the form:
   - Name: "John Doe"
   - Phone: "+91 9876543210"
   - Monthly Income: 45000
   - Monthly Expenses: 30000
   - Income Variation: 5000
   - Total Savings: 100000
   - UPI Transactions: 25
   - Bill Payment Streak: 10
   - Digital Banking: 12 months
3. Submit the form
4. View the results with charts
5. Click "Download PDF Report"

## 📁 File Checklist

Make sure you have these files:

### Core Files
- [ ] `app.py` - Main Flask application
- [ ] `ml_model.py` - Machine learning model
- [ ] `pdf_generator.py` - PDF report generator
- [ ] `requirements.txt` - Dependencies
- [ ] `README.md` - Documentation
- [ ] `test_system.py` - Testing script

### Templates Folder
- [ ] `templates/base.html`
- [ ] `templates/login.html`
- [ ] `templates/home.html`
- [ ] `templates/assessment_form.html`
- [ ] `templates/result.html`
- [ ] `templates/applications.html`
- [ ] `templates/dashboard.html`

### Auto-Generated (After First Run)
- [ ] `creditbridge.db` - Database
- [ ] `ml_model.pkl` - Trained model
- [ ] `scaler.pkl` - Feature scaler
- [ ] `reports/` - PDF reports folder
- [ ] `uploads/` - Uploads folder

## 🧪 Testing

Run automated tests:
```bash
python test_system.py
```

Expected output:
```
✅ PASSED - Module Imports
✅ PASSED - Machine Learning Model
✅ PASSED - Database Operations
✅ PASSED - PDF Generation
✅ PASSED - Flask Routes
✅ PASSED - Permissions System

RESULTS: 6/6 tests passed (100.0%)
🎉 All tests passed! System is ready for use.
```

## ❓ Troubleshooting

### Issue: Module not found
**Solution:** Make sure virtual environment is activated and run:
```bash
pip install -r requirements.txt
```

### Issue: Port 5000 already in use
**Solution:** Change port in `app.py`:
```python
app.run(debug=True, port=5001)  # Use different port
```

### Issue: Database locked
**Solution:** Close any other instances and delete `credit_risk.db`:
```bash
rm credit_risk.db
python app.py
```

### Issue: PDF not downloading
**Solution:** Check `reports/` folder exists:
```bash
mkdir reports
```

### Issue: Charts not displaying
**Solution:** Check internet connection (Chart.js loads from CDN)

## 🔧 Configuration

### Change Secret Key
In `app.py`, line 11:
```python
app.config['SECRET_KEY'] = 'your-secret-key-here'
```

### Change Database
In `app.py`, line 12:
```python
# SQLite (default)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///credit_risk.db'

# PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/dbname'

# MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:pass@localhost/dbname'
```

### Adjust ML Model
In `ml_model.py`, change training samples:
```python
# Line 234
model.train_model(n_samples=5000)  # Increase for better accuracy
```

## 📊 Understanding the System

### Credit Score Range
- **300-599:** High Risk (Red) ❌
- **600-749:** Medium Risk (Orange) ⚠️
- **750-900:** Low Risk (Green) ✅

### Behavioral Metrics
1. **ISI** - Income Stability (25% weight)
2. **ECR** - Expense Control (20% weight)
3. **PCS** - Payment Consistency (20% weight)
4. **DAS** - Digital Activity (15% weight)
5. **SDR** - Savings Discipline (15% weight)
6. **CHS** - Cashflow Health (5% weight)

### User Permissions
- **ALL:** Full system access
- **view_all:** View all assessments
- **view_own:** View only own assessments
- **create:** Create new assessments
- **edit:** Modify assessments
- **analytics:** Access dashboard
- **export:** Export data/reports

## 🚀 Deployment (Production)

### Option 1: Heroku
```bash
# Install Heroku CLI
heroku create creditbridge
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

### Option 2: AWS EC2
```bash
# SSH into EC2 instance
sudo apt update
sudo apt install python3-pip
git clone your-repo
cd creditbridge
pip3 install -r requirements.txt
python3 app.py
```

### Option 3: Docker
Create `Dockerfile`:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Run:
```bash
docker build -t creditbridge .
docker run -p 5000:5000 creditbridge
```

## 📝 Next Steps

1. ✅ Complete setup and test
2. 📖 Read full README.md
3. 🧪 Run test_system.py
4. 🎨 Customize branding/colors
5. 🔐 Change secret keys
6. 🗃️ Switch to production database
7. 🚀 Deploy to server
8. 📊 Monitor and improve

## 💡 Tips

- Use **admin** account for exploring all features
- Try different financial profiles to see score variations
- Download PDFs to see professional formatting
- Check analytics dashboard after creating multiple assessments
- Test permission restrictions with different accounts

## 📞 Need Help?

- Check README.md for detailed documentation
- Run test_system.py to diagnose issues
- Review error messages in terminal
- Ensure all dependencies are installed
- Verify Python version (3.8+)

## 🎓 Learning Resources

- **Flask:** https://flask.palletsprojects.com/
- **SQLAlchemy:** https://www.sqlalchemy.org/
- **scikit-learn:** https://scikit-learn.org/
- **Bootstrap:** https://getbootstrap.com/
- **ReportLab:** https://www.reportlab.com/

---

**Happy Coding! 🚀**

*For detailed documentation, see README.md*