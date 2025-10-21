# Vietnamese User Data Generation Summary

## ✅ Data Generation Completed Successfully!

**Date Generated**: May 2025  
**Database**: MoneyFlow (moneyflow.db)  
**Date Range**: May 2024 - May 2025 (13 months)

---

## 📊 Dataset Statistics

### Users
- **Total Users**: 50
- **All users have realistic Vietnamese names, emails, and profiles**
- **Password for all users**: `password123`

### Transactions
- **Total Transactions**: 26,672
- **Average per User**: 533.4 transactions
- **Transaction Types**: Income and Expense
- **All descriptions in Vietnamese**

---

## 👥 User Demographics

### Income Class Distribution
| Income Class | Count | Percentage | Monthly Income Range (VND) |
|--------------|-------|------------|----------------------------|
| High         | 6     | 12.0%      | 40M - 80M                  |
| Upper-Mid    | 10    | 20.0%      | 25M - 40M                  |
| Middle       | 14    | 28.0%      | 15M - 25M                  |
| Lower-Mid    | 14    | 28.0%      | 10M - 15M                  |
| Low          | 6     | 12.0%      | 5M - 10M                   |

### City Distribution
| City              | Count | Percentage |
|-------------------|-------|------------|
| Ho Chi Minh City  | 20    | 40.0%      |
| Hanoi             | 13    | 26.0%      |
| Da Nang           | 8     | 16.0%      |
| Can Tho           | 5     | 10.0%      |
| Nha Trang         | 2     | 4.0%       |
| Bien Hoa          | 2     | 4.0%       |

### Age Distribution
- **Range**: 22-59 years
- **Young Professionals (22-28)**: ~25%
- **Established Professionals (28-35)**: ~35%
- **Senior Professionals (35-45)**: ~25%
- **Experienced Professionals (45-60)**: ~15%

---

## 💰 Financial Data Features

### Numeric Features

1. **monthly_income** (VND)
   - Range: 5,000,000 - 90,000,000 VND
   - Average: ~17,300,000 VND (based on Vietnam 2024 data)
   - Adjusted higher for HCMC and Hanoi residents

2. **transaction_amount** (VND)
   - Range: 10,000 - 90,000,000 VND
   - Rounded to nearest 1,000 VND
   - Realistic amounts based on category and income class

3. **age** (years)
   - Range: 22-60 years
   - Weighted distribution favoring 28-35 age group

### Non-Numeric Features

1. **full_name** (Vietnamese)
   - Format: [Surname] [Middle Name] [Given Name]
   - Examples: "Nguyễn Văn Minh", "Trần Thị Hương"
   - Proper Vietnamese Unicode characters

2. **email** (String)
   - Derived from name (romanized)
   - Domains: gmail.com, yahoo.com, outlook.com, moneyflow.vn

3. **gender** (Categorical)
   - Values: "Male", "Female"
   - ~50/50 distribution

4. **city** (Categorical)
   - 7 major Vietnamese cities
   - Weighted by population

5. **occupation** (Categorical)
   - 20 different professions
   - Includes: Software Engineer, Teacher, Doctor, Business Owner, etc.

6. **income_class** (Categorical)
   - Values: "low", "lower-mid", "middle", "upper-mid", "high"
   - Determines spending patterns

### Transaction Features

1. **type** (Categorical)
   - Values: "income", "expense"
   - Income: 1-3 per month
   - Expense: 10-30 per month

2. **category** (Vietnamese, Categorical)
   - **Expense Categories** (9):
     - Ăn uống (Food & Dining)
     - Di chuyển (Transportation)
     - Mua sắm (Shopping)
     - Hóa đơn (Bills & Utilities)
     - Giải trí (Entertainment)
     - Y tế (Healthcare)
     - Giáo dục (Education)
     - Nhà ở (Housing)
     - Khác (Other)
   
   - **Income Categories** (5):
     - Lương (Salary)
     - Thưởng (Bonus)
     - Đầu tư (Investment)
     - Quà tặng (Gifts)
     - Thu nhập khác (Other Income)

3. **description** (Vietnamese, Free Text)
   - 100+ unique Vietnamese descriptions
   - Examples:
     - "Ăn sáng phở" (Breakfast pho)
     - "Xăng xe máy" (Motorbike fuel)
     - "Cà phê Highlands" (Highlands coffee)
     - "Lương tháng" (Monthly salary)

4. **date** (Date)
   - Format: YYYY-MM-DD
   - Range: 2024-05-01 to 2025-05-31
   - Daily transactions with realistic frequency

---

## 📈 Spending Patterns by Income Class

### Low Income (5-10M VND/month)
- Food: 30-40% of income
- Housing: 25-35%
- Transportation: 10-15%
- Other categories: 5-10% combined

### Middle Income (15-25M VND/month)
- Food: 20-30% of income
- Housing: 20-30%
- Shopping: 10-20%
- Entertainment: 8-15%
- Other categories: balanced distribution

### High Income (40-80M VND/month)
- Shopping: 20-30% of income
- Entertainment: 15-25%
- Housing: 15-25%
- Food: 10-20%
- Other categories: flexible spending

---

## 🔑 Sample Login Credentials

```
Email: lethanh@outlook.com
Password: password123
Name: Lê Thanh
Income: 14,805,732 VND/month
City: Can Tho

Email: vuvanthanh@moneyflow.vn
Password: password123
Name: Vũ Văn Thanh
Income: 53,730,525 VND/month
City: Ho Chi Minh City

Email: buitu460@moneyflow.vn
Password: password123
Name: Bùi Tú
Income: 25,887,253 VND/month
City: Ho Chi Minh City

Email: lamlan@yahoo.com
Password: password123
Name: Lâm Lan
Income: 17,378,083 VND/month
City: Can Tho

Email: dinhhoa210@yahoo.com
Password: password123
Name: Đinh Hoa
Income: 5,617,297 VND/month
City: Can Tho
```

**All 50 users use the same password**: `password123`

---

## 📁 Generated Files

1. **data/generated_users.json** - Complete user profiles (50 users)
2. **moneyflow.db** - SQLite database with all data
3. **data/DATA_FEATURES_DOCUMENTATION.md** - Detailed feature documentation
4. **data/DATA_GENERATION_SUMMARY.md** - This summary file

---

## 🎯 Data Quality & Realism

### Based on Real Vietnamese Data
- ✅ Average salary: 17.3M VND/month (Vietnam 2024)
- ✅ Cost of living patterns from major cities
- ✅ Realistic spending distributions
- ✅ Authentic Vietnamese names and locations
- ✅ Proper Vietnamese Unicode characters
- ✅ Realistic transaction descriptions

### Transaction Realism
- ✅ Daily expenses (food, transport) - smaller, frequent amounts
- ✅ Monthly bills (housing, utilities) - larger, regular amounts
- ✅ Occasional expenses (shopping, entertainment) - variable amounts
- ✅ Salary payments on 5th-10th of month
- ✅ Seasonal variations included

### Cultural Authenticity
- ✅ Vietnamese naming conventions
- ✅ Common Vietnamese occupations
- ✅ Major Vietnamese cities
- ✅ Local brands and services (Highlands Coffee, Grab, etc.)
- ✅ Vietnamese spending habits

---

## 🚀 How to Use This Data

### 1. Access the Database
The data is already populated in `moneyflow.db`. Start the backend server:
```bash
python run_backend.py
```

### 2. Login to Frontend
Start the frontend server:
```bash
python manage.py runserver
```

Login with any of the 50 user credentials (password: `password123`)

### 3. Explore the Data
- View transactions in the dashboard
- Check analytics for spending patterns
- Filter by category, date range, type
- See realistic Vietnamese financial data

### 4. API Access
All data accessible via FastAPI endpoints:
- GET /api/transactions/ - List transactions
- GET /api/analytics/summary - Monthly summary
- GET /api/analytics/by-category - Category breakdown
- GET /api/analytics/monthly-comparison - 6-month comparison

---

## 📊 Data Analysis Opportunities

This dataset is perfect for:

1. **Financial Analysis**
   - Spending pattern analysis by income class
   - Budget optimization recommendations
   - Savings rate calculations

2. **Machine Learning**
   - Transaction categorization
   - Spending prediction
   - Anomaly detection
   - Budget forecasting

3. **Data Visualization**
   - Income vs. expense trends
   - Category distribution charts
   - City-based spending comparisons
   - Time series analysis

4. **Business Intelligence**
   - User segmentation
   - Behavioral analysis
   - Market research insights

---

## ✨ Key Achievements

✅ **50 realistic Vietnamese user profiles** with authentic names and demographics  
✅ **26,672 transactions** spanning 13 months (May 2024 - May 2025)  
✅ **100% Vietnamese language** descriptions and categories  
✅ **Realistic spending patterns** based on actual Vietnam 2024 data  
✅ **Multiple income classes** representing Vietnamese socioeconomic diversity  
✅ **7 major cities** with proper geographic distribution  
✅ **20 different occupations** reflecting Vietnamese job market  
✅ **Proper Unicode support** for Vietnamese characters  
✅ **Ready for immediate use** in MoneyFlow application  

---

## 📝 Notes

- All monetary values in Vietnamese Dong (VND)
- All dates in YYYY-MM-DD format
- All text in Vietnamese with proper diacritics
- Database ready for production use
- Data can be regenerated with different random seed for variation

---

**Generated by**: Vietnamese User Data Generator  
**For**: MoneyFlow Personal Finance Management System  
**Research Based On**: Vietnam 2024-2025 demographic and financial data

