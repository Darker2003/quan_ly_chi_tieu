"""
Vietnamese User Data Generator for MoneyFlow Application
Based on 2024 Vietnam demographic and financial research data

Data Sources:
- Average salary: 17.3 million VND/month (697 USD)
- Cost of living: Food (3-8M VND), Transport (1-3M VND), Housing (5-15M VND)
- Middle class: 26% of population by 2026
- Major cities: Ho Chi Minh City, Hanoi, Da Nang
"""

import random
import json
from datetime import datetime, timedelta
from decimal import Decimal

# Vietnamese Names Data
VIETNAMESE_SURNAMES = [
    "Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Phan", "Vũ", "Võ", "Đặng", "Bùi",
    "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Đinh", "Trương", "Lâm", "Huỳnh", "Mai"
]

VIETNAMESE_MALE_NAMES = [
    "Minh", "Tuấn", "Hùng", "Dũng", "Quang", "Thành", "Hải", "Long", "Nam", "Khoa",
    "Đức", "Anh", "Phong", "Tùng", "Hoàng", "Bảo", "Khang", "Thắng", "Vinh", "Cường",
    "Tân", "Huy", "Kiên", "Sơn", "Toàn", "Trung", "Việt", "Đạt", "Phúc", "Thiện"
]

VIETNAMESE_FEMALE_NAMES = [
    "Hương", "Lan", "Mai", "Linh", "Hà", "Thu", "Nga", "Trang", "Hoa", "Phương",
    "Anh", "Thảo", "Nhung", "Huyền", "Thúy", "Ngọc", "Vy", "My", "Chi", "Diệu",
    "Thanh", "Tâm", "Yến", "Quỳnh", "Như", "Giang", "Tú", "Xuân", "Hạnh", "Dung"
]

# Location Data
CITIES = [
    {"name": "Ho Chi Minh City", "weight": 40},
    {"name": "Hanoi", "weight": 30},
    {"name": "Da Nang", "weight": 15},
    {"name": "Can Tho", "weight": 5},
    {"name": "Hai Phong", "weight": 5},
    {"name": "Bien Hoa", "weight": 3},
    {"name": "Nha Trang", "weight": 2}
]

# Income Brackets (VND per month)
INCOME_BRACKETS = [
    {"range": (5_000_000, 10_000_000), "weight": 15, "class": "low"},      # Low income
    {"range": (10_000_000, 15_000_000), "weight": 25, "class": "lower-mid"}, # Lower-middle
    {"range": (15_000_000, 25_000_000), "weight": 30, "class": "middle"},   # Middle class
    {"range": (25_000_000, 40_000_000), "weight": 20, "class": "upper-mid"}, # Upper-middle
    {"range": (40_000_000, 80_000_000), "weight": 10, "class": "high"}      # High income
]

# Occupation Data
OCCUPATIONS = [
    "Software Engineer", "Teacher", "Office Worker", "Sales Manager", "Accountant",
    "Marketing Specialist", "Business Owner", "Freelancer", "Designer", "Engineer",
    "Doctor", "Nurse", "Pharmacist", "Bank Employee", "Customer Service",
    "HR Manager", "Project Manager", "Data Analyst", "Content Creator", "Consultant"
]

# Age Distribution
AGE_RANGES = [
    {"range": (22, 28), "weight": 25},  # Young professionals
    {"range": (28, 35), "weight": 35},  # Established professionals
    {"range": (35, 45), "weight": 25},  # Senior professionals
    {"range": (45, 60), "weight": 15}   # Experienced professionals
]

def weighted_choice(choices):
    """Select item based on weight"""
    total = sum(c.get("weight", 1) for c in choices)
    r = random.uniform(0, total)
    upto = 0
    for c in choices:
        weight = c.get("weight", 1)
        if upto + weight >= r:
            return c
        upto += weight
    return choices[-1]

def generate_vietnamese_name(gender):
    """Generate realistic Vietnamese name"""
    surname = random.choice(VIETNAMESE_SURNAMES)
    if gender == "Male":
        given_name = random.choice(VIETNAMESE_MALE_NAMES)
    else:
        given_name = random.choice(VIETNAMESE_FEMALE_NAMES)
    
    # Sometimes add middle name
    if random.random() > 0.5:
        middle = random.choice(["Văn", "Thị", "Đình", "Quốc", "Hữu", "Công"])
        return f"{surname} {middle} {given_name}"
    return f"{surname} {given_name}"

def remove_vietnamese_accents(text):
    """Remove Vietnamese accents and diacritics"""
    import unicodedata
    
    # Normalize to NFD (decomposed form)
    text = unicodedata.normalize('NFD', text)
    
    # Remove combining characters (accents)
    result = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
    
    # Manual replacements for specific Vietnamese characters
    replacements = {
        'đ': 'd', 'Đ': 'D',
        'ă': 'a', 'â': 'a', 'ê': 'e', 'ô': 'o', 'ơ': 'o', 'ư': 'u',
        'á': 'a', 'à': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
        'é': 'e', 'è': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
        'í': 'i', 'ì': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
        'ó': 'o', 'ò': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
        'ú': 'u', 'ù': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
        'ý': 'y', 'ỳ': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
        'Á': 'A', 'À': 'A', 'Ả': 'A', 'Ã': 'A', 'Ạ': 'A',
        'É': 'E', 'È': 'E', 'Ẻ': 'E', 'Ẽ': 'E', 'Ẹ': 'E',
        'Í': 'I', 'Ì': 'I', 'Ỉ': 'I', 'Ĩ': 'I', 'Ị': 'I',
        'Ó': 'O', 'Ò': 'O', 'Ỏ': 'O', 'Õ': 'O', 'Ọ': 'O',
        'Ú': 'U', 'Ù': 'U', 'Ủ': 'U', 'Ũ': 'U', 'Ụ': 'U',
        'Ý': 'Y', 'Ỳ': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y', 'Ỵ': 'Y'
    }
    
    for viet, eng in replacements.items():
        result = result.replace(viet, eng)
    
    return result

def generate_email(name):
    """Generate email from name without Vietnamese accents"""
    # Remove Vietnamese characters for email
    name_parts = name.lower().split()
    
    email_name = ""
    for part in name_parts:
        # Remove accents first
        clean_part = remove_vietnamese_accents(part)
        # Remove any remaining non-ASCII characters
        clean_part = ''.join(c for c in clean_part if c.isascii() and c.isalnum())
        email_name += clean_part
    
    # Ensure email name is not empty
    if not email_name:
        email_name = "user"
    
    domains = ["gmail.com", "yahoo.com", "outlook.com", "moneyflow.vn"]
    number = random.randint(1, 999) if random.random() > 0.5 else ""
    return f"{email_name}{number}@{random.choice(domains)}"

def generate_user_profile():
    """Generate a single user profile"""
    gender = random.choice(["Male", "Female"])
    name = generate_vietnamese_name(gender)
    age_bracket = weighted_choice(AGE_RANGES)
    age = random.randint(*age_bracket["range"])
    
    income_bracket = weighted_choice(INCOME_BRACKETS)
    monthly_income = random.randint(*income_bracket["range"])
    
    city_choice = weighted_choice(CITIES)
    city = city_choice["name"]
    
    # Adjust income based on city (HCMC and Hanoi typically higher)
    if city in ["Ho Chi Minh City", "Hanoi"]:
        monthly_income = int(monthly_income * random.uniform(1.1, 1.3))
    
    return {
        "full_name": name,
        "email": generate_email(name),
        "age": age,
        "gender": gender,
        "city": city,
        "occupation": random.choice(OCCUPATIONS),
        "monthly_income": monthly_income,
        "income_class": income_bracket["class"],
        "password": "password123"  # Default password for testing
    }

def generate_all_users(count=50):
    """Generate specified number of users"""
    users = []
    for i in range(count):
        user = generate_user_profile()
        user["user_id"] = i + 1
        users.append(user)
    return users

if __name__ == "__main__":
    # Generate 50 users
    users = generate_all_users(50)
    
    # Save to JSON file
    with open('vietnamese_users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {len(users)} Vietnamese user profiles")
    print("\nSample users:")
    for user in users[:5]:
        print(f"- {user['full_name']} ({user['age']}), {user['occupation']}")
        print(f"  Income: {user['monthly_income']:,} VND/month, City: {user['city']}")

