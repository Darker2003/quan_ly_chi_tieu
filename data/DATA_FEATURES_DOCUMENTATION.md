# Vietnamese User Data Features Documentation

## Overview
This document describes all numeric and non-numeric features used in the MoneyFlow Vietnamese user dataset, based on 2024-2025 Vietnam demographic and financial research.

## Data Sources
- **Average Salary**: 17.3 million VND/month (~$697 USD) as of August 2024
- **Middle Class**: Projected to reach 26% of population by 2026
- **Cost of Living**: Based on major Vietnamese cities (HCMC, Hanoi, Da Nang)
- **Consumer Behavior**: Vietnamese spending patterns and financial habits

---

## NON-NUMERIC FEATURES

### 1. User Identity Features

#### **full_name** (String)
- **Description**: Full Vietnamese name following Vietnamese naming conventions
- **Format**: [Surname] [Middle Name (optional)] [Given Name]
- **Examples**: 
  - "Nguyễn Văn Minh"
  - "Trần Thị Hương"
  - "Lê Quốc Dũng"
- **Data Source**: Common Vietnamese surnames (Nguyễn, Trần, Lê, Phạm, etc.) and given names
- **Character Set**: Vietnamese Unicode characters (đ, ă, â, ê, ô, ơ, ư, etc.)

#### **email** (String)
- **Description**: Email address derived from user's name
- **Format**: [romanized_name][optional_number]@[domain]
- **Examples**:
  - "nguyenvanminh123@gmail.com"
  - "tranthihuong@yahoo.com"
  - "lequocdung@moneyflow.vn"
- **Domains**: gmail.com, yahoo.com, outlook.com, moneyflow.vn
- **Note**: Vietnamese characters converted to ASCII equivalents

#### **gender** (String, Categorical)
- **Description**: User's gender
- **Values**: "Male", "Female"
- **Distribution**: Approximately 50/50 split

#### **city** (String, Categorical)
- **Description**: City of residence in Vietnam
- **Values**:
  - "Ho Chi Minh City" (40% weight)
  - "Hanoi" (30% weight)
  - "Da Nang" (15% weight)
  - "Can Tho" (5% weight)
  - "Hai Phong" (5% weight)
  - "Bien Hoa" (3% weight)
  - "Nha Trang" (2% weight)
- **Impact**: Affects income levels (HCMC and Hanoi typically 10-30% higher)

#### **occupation** (String, Categorical)
- **Description**: User's profession or job title
- **Values**: 20 different occupations including:
  - Software Engineer
  - Teacher
  - Office Worker
  - Sales Manager
  - Accountant
  - Marketing Specialist
  - Business Owner
  - Freelancer
  - Designer
  - Engineer
  - Doctor
  - Nurse
  - And more...
- **Distribution**: Random selection

#### **income_class** (String, Categorical)
- **Description**: Socioeconomic class based on monthly income
- **Values**:
  - "low" (15% of users)
  - "lower-mid" (25% of users)
  - "middle" (30% of users)
  - "upper-mid" (20% of users)
  - "high" (10% of users)
- **Impact**: Determines spending patterns and transaction frequency

### 2. Transaction Features

#### **transaction_type** (String, Categorical)
- **Description**: Type of financial transaction
- **Values**: "income", "expense"
- **Distribution**: 
  - Income: 1-3 transactions per month
  - Expense: 10-30 transactions per month

#### **category** (String, Categorical)
- **Description**: Transaction category in Vietnamese
- **Expense Categories**:
  - "Ăn uống" (Food & Dining)
  - "Di chuyển" (Transportation)
  - "Mua sắm" (Shopping)
  - "Hóa đơn" (Bills & Utilities)
  - "Giải trí" (Entertainment)
  - "Y tế" (Healthcare)
  - "Giáo dục" (Education)
  - "Nhà ở" (Housing)
  - "Khác" (Other)
- **Income Categories**:
  - "Lương" (Salary)
  - "Thưởng" (Bonus)
  - "Đầu tư" (Investment)
  - "Quà tặng" (Gifts)
  - "Thu nhập khác" (Other Income)

#### **description** (String, Free Text)
- **Description**: Detailed transaction description in Vietnamese
- **Examples**:
  - "Ăn sáng phở" (Breakfast pho)
  - "Xăng xe máy" (Motorbike fuel)
  - "Cà phê Highlands" (Highlands coffee)
  - "Tiền điện" (Electricity bill)
  - "Lương tháng" (Monthly salary)
- **Language**: Vietnamese with proper diacritics
- **Count**: 100+ unique descriptions across all categories

#### **date** (Date String)
- **Description**: Transaction date
- **Format**: "YYYY-MM-DD"
- **Range**: 2024-05-01 to 2025-05-31 (13 months)
- **Distribution**: Daily transactions with varying frequency

---

## NUMERIC FEATURES

### 1. User Demographics

#### **age** (Integer)
- **Description**: User's age in years
- **Range**: 22-60 years
- **Distribution**:
  - 22-28 years: 25% (Young professionals)
  - 28-35 years: 35% (Established professionals)
  - 35-45 years: 25% (Senior professionals)
  - 45-60 years: 15% (Experienced professionals)
- **Unit**: Years

#### **monthly_income** (Integer)
- **Description**: User's monthly income in Vietnamese Dong (VND)
- **Range**: 5,000,000 - 80,000,000 VND
- **Distribution by Income Class**:
  - Low: 5M - 10M VND (15%)
  - Lower-mid: 10M - 15M VND (25%)
  - Middle: 15M - 25M VND (30%)
  - Upper-mid: 25M - 40M VND (20%)
  - High: 40M - 80M VND (10%)
- **Average**: ~17.3M VND (based on Vietnam 2024 data)
- **Unit**: Vietnamese Dong (VND)
- **Note**: Adjusted 10-30% higher for HCMC and Hanoi residents

### 2. Transaction Amounts

#### **amount** (Integer)
- **Description**: Transaction amount in Vietnamese Dong
- **Range**: 10,000 - 80,000,000 VND
- **Typical Ranges by Category**:
  - **Food & Dining**: 20,000 - 500,000 VND per transaction
  - **Transportation**: 15,000 - 300,000 VND per transaction
  - **Housing**: 3,000,000 - 15,000,000 VND per transaction
  - **Utilities**: 200,000 - 2,000,000 VND per transaction
  - **Shopping**: 100,000 - 5,000,000 VND per transaction
  - **Entertainment**: 100,000 - 3,000,000 VND per transaction
  - **Healthcare**: 100,000 - 2,000,000 VND per transaction
  - **Education**: 500,000 - 5,000,000 VND per transaction
  - **Salary**: Equal to monthly_income
  - **Bonus**: 10-50% of monthly_income
- **Unit**: Vietnamese Dong (VND)
- **Rounding**: Rounded to nearest 1,000 VND

### 3. Derived Numeric Features

#### **transaction_count** (Integer)
- **Description**: Number of transactions per user per month
- **Range**: 10-40 transactions/month
- **Factors**:
  - Income class (higher income = more transactions)
  - Category frequency (food/transport = daily, housing = monthly)
- **Total Dataset**: ~15,000-25,000 transactions for 50 users over 13 months

#### **savings_rate** (Float, Percentage)
- **Description**: Percentage of income saved (income - expenses)
- **Range**: -20% to 40%
- **Typical Values**:
  - Low income: 0-10%
  - Middle income: 10-20%
  - High income: 20-40%
- **Note**: Can be negative (spending > income) in some months

---

## SPENDING PATTERNS BY INCOME CLASS

### Low Income (5-10M VND/month)
- Food: 30-40% of income
- Housing: 25-35%
- Transportation: 10-15%
- Utilities: 5-10%
- Entertainment: 2-5%
- Healthcare: 2-5%
- Education: 1-3%
- Shopping: 5-10%
- Other: 1-3%

### Middle Income (15-25M VND/month)
- Food: 20-30% of income
- Housing: 20-30%
- Transportation: 8-12%
- Utilities: 5-10%
- Entertainment: 8-15%
- Healthcare: 3-8%
- Education: 3-8%
- Shopping: 10-20%
- Other: 3-8%

### High Income (40-80M VND/month)
- Food: 10-20% of income
- Housing: 15-25%
- Transportation: 5-10%
- Utilities: 3-7%
- Entertainment: 15-25%
- Healthcare: 5-10%
- Education: 5-15%
- Shopping: 20-30%
- Other: 5-15%

---

## DATA QUALITY NOTES

1. **Realistic Patterns**: All data based on actual Vietnamese consumer behavior research
2. **Seasonal Variations**: Includes Tết (Lunar New Year) spending spikes
3. **Currency**: All amounts in Vietnamese Dong (VND)
4. **Language**: Vietnamese with proper Unicode diacritics
5. **Date Range**: 13 months (May 2024 - May 2025)
6. **User Count**: 50 diverse users
7. **Transaction Count**: ~15,000-25,000 total transactions

---

## USAGE INSTRUCTIONS

To generate and populate the database:

```bash
cd data
python populate_vietnamese_data.py
```

This will:
1. Generate 50 Vietnamese user profiles
2. Create realistic transactions for each user
3. Populate the MoneyFlow database
4. Save user profiles to `generated_users.json`
5. Display summary statistics

Default password for all users: `password123`

