"""
Vietnamese Transaction Data Generator for MoneyFlow Application
Generates realistic transactions from May 2024 to May 2025

Based on Vietnamese spending patterns:
- Food: 3-8M VND/month
- Transportation: 1-3M VND/month  
- Housing: 5-15M VND/month
- Utilities: 500K-2M VND/month
- Entertainment: 1-3M VND/month
"""

import random
import json
from datetime import datetime, timedelta
from decimal import Decimal

# Vietnamese Transaction Descriptions
TRANSACTION_DESCRIPTIONS = {
    "Ăn uống": [  # Food & Dining
        "Ăn sáng phở", "Cơm trưa văn phòng", "Cà phê Highlands", "Ăn tối gia đình",
        "Lẩu cuối tuần", "Bánh mì sáng", "Trà sữa", "Bún chả", "Cơm tấm",
        "Nhà hàng buffet", "Gọi đồ ăn Grab", "Siêu thị Co.opmart", "Chợ Bến Thành",
        "Ăn vặt", "Quán ăn vỉa hè", "Pizza Hut", "KFC", "Lotteria", "Jollibee"
    ],
    "Di chuyển": [  # Transportation
        "Xăng xe máy", "Grab bike", "Grab car", "Xe buýt", "Taxi Mai Linh",
        "Bảo dưỡng xe", "Rửa xe", "Gửi xe", "Vé máy bay", "Vé tàu",
        "Sửa xe", "Thay nhớt", "Phí đường cao tốc", "Gửi xe tháng"
    ],
    "Mua sắm": [  # Shopping
        "Quần áo", "Giày dép", "Mỹ phẩm", "Điện thoại", "Laptop",
        "Đồ gia dụng", "Nội thất", "Sách", "Đồ chơi", "Phụ kiện",
        "Vincom", "Aeon Mall", "Shopee", "Lazada", "Tiki"
    ],
    "Hóa đơn": [  # Bills & Utilities
        "Tiền điện", "Tiền nước", "Internet FPT", "Điện thoại Viettel",
        "Gas", "Phí quản lý chung cư", "Bảo hiểm", "Trả góp"
    ],
    "Giải trí": [  # Entertainment
        "Xem phim CGV", "Karaoke", "Du lịch Đà Lạt", "Du lịch Vũng Tàu",
        "Gym", "Yoga", "Spa", "Massage", "Game online", "Netflix",
        "Spotify", "Sách", "Nhạc cụ", "Thể thao"
    ],
    "Y tế": [  # Healthcare
        "Khám bệnh", "Mua thuốc", "Nha khoa", "Xét nghiệm", "Vitamin",
        "Bảo hiểm y tế", "Phòng khám", "Bệnh viện", "Thuốc cảm"
    ],
    "Giáo dục": [  # Education
        "Học phí", "Sách giáo khoa", "Khóa học online", "Tiếng Anh",
        "Học lái xe", "Văn phòng phẩm", "Đào tạo nghề"
    ],
    "Nhà ở": [  # Housing
        "Tiền thuê nhà", "Tiền nhà", "Sửa chữa nhà", "Đồ nội thất"
    ],
    "Khác": [  # Other
        "Quà tặng", "Từ thiện", "Tiết kiệm", "Đầu tư", "Khác"
    ]
}

INCOME_DESCRIPTIONS = {
    "Lương": [  # Salary
        "Lương tháng", "Lương cơ bản", "Lương net"
    ],
    "Thưởng": [  # Bonus
        "Thưởng tháng", "Thưởng quý", "Thưởng Tết", "Thưởng dự án",
        "Thưởng hiệu suất", "Thưởng KPI"
    ],
    "Đầu tư": [  # Investment
        "Cổ tức", "Lãi tiết kiệm", "Lãi đầu tư", "Bán cổ phiếu"
    ],
    "Quà tặng": [  # Gifts
        "Tiền mừng", "Quà sinh nhật", "Tiền lì xì"
    ],
    "Thu nhập khác": [  # Other income
        "Freelance", "Part-time", "Bán đồ cũ", "Thu nhập phụ"
    ]
}

# Spending patterns by income class
SPENDING_PATTERNS = {
    "low": {
        "Ăn uống": (0.30, 0.40),      # 30-40% of income
        "Di chuyển": (0.10, 0.15),
        "Nhà ở": (0.25, 0.35),
        "Hóa đơn": (0.05, 0.10),
        "Giải trí": (0.02, 0.05),
        "Y tế": (0.02, 0.05),
        "Giáo dục": (0.01, 0.03),
        "Mua sắm": (0.05, 0.10),
        "Khác": (0.01, 0.03)
    },
    "lower-mid": {
        "Ăn uống": (0.25, 0.35),
        "Di chuyển": (0.10, 0.15),
        "Nhà ở": (0.20, 0.30),
        "Hóa đơn": (0.05, 0.10),
        "Giải trí": (0.05, 0.10),
        "Y tế": (0.03, 0.07),
        "Giáo dục": (0.02, 0.05),
        "Mua sắm": (0.08, 0.15),
        "Khác": (0.02, 0.05)
    },
    "middle": {
        "Ăn uống": (0.20, 0.30),
        "Di chuyển": (0.08, 0.12),
        "Nhà ở": (0.20, 0.30),
        "Hóa đơn": (0.05, 0.10),
        "Giải trí": (0.08, 0.15),
        "Y tế": (0.03, 0.08),
        "Giáo dục": (0.03, 0.08),
        "Mua sắm": (0.10, 0.20),
        "Khác": (0.03, 0.08)
    },
    "upper-mid": {
        "Ăn uống": (0.15, 0.25),
        "Di chuyển": (0.08, 0.12),
        "Nhà ở": (0.15, 0.25),
        "Hóa đơn": (0.05, 0.08),
        "Giải trí": (0.10, 0.20),
        "Y tế": (0.05, 0.10),
        "Giáo dục": (0.05, 0.10),
        "Mua sắm": (0.15, 0.25),
        "Khác": (0.05, 0.10)
    },
    "high": {
        "Ăn uống": (0.10, 0.20),
        "Di chuyển": (0.05, 0.10),
        "Nhà ở": (0.15, 0.25),
        "Hóa đơn": (0.03, 0.07),
        "Giải trí": (0.15, 0.25),
        "Y tế": (0.05, 0.10),
        "Giáo dục": (0.05, 0.15),
        "Mua sắm": (0.20, 0.30),
        "Khác": (0.05, 0.15)
    }
}

def generate_transaction_amount(category, monthly_income, income_class):
    """Generate realistic transaction amount based on category and income"""
    pattern = SPENDING_PATTERNS.get(income_class, SPENDING_PATTERNS["middle"])
    
    if category in pattern:
        min_pct, max_pct = pattern[category]
        # Monthly budget for this category
        monthly_budget = monthly_income * random.uniform(min_pct, max_pct)
        
        # Individual transaction is a portion of monthly budget
        # More transactions = smaller amounts
        if category in ["Ăn uống", "Di chuyển"]:
            # Daily expenses - smaller amounts
            amount = monthly_budget / random.randint(20, 40)
        elif category in ["Nhà ở", "Hóa đơn"]:
            # Monthly bills - larger amounts
            amount = monthly_budget / random.randint(1, 3)
        else:
            # Occasional expenses
            amount = monthly_budget / random.randint(3, 10)
        
        # Round to nearest 1000 VND
        return int(round(amount / 1000) * 1000)
    
    return random.randint(50000, 500000)

def generate_income_transaction(monthly_income, date):
    """Generate income transaction"""
    # Salary on 5th-10th of month
    if date.day >= 5 and date.day <= 10 and random.random() > 0.3:
        category = "Lương"
        amount = monthly_income
    # Bonus occasionally
    elif random.random() > 0.95:
        category = random.choice(["Thưởng", "Đầu tư", "Quà tặng", "Thu nhập khác"])
        amount = int(monthly_income * random.uniform(0.1, 0.5))
    else:
        return None
    
    description = random.choice(INCOME_DESCRIPTIONS[category])
    
    return {
        "type": "income",
        "category": category,
        "description": description,
        "amount": amount,
        "date": date.strftime("%Y-%m-%d")
    }

def generate_expense_transaction(monthly_income, income_class, date):
    """Generate expense transaction"""
    # Weight categories by frequency
    category_weights = {
        "Ăn uống": 40,
        "Di chuyển": 20,
        "Mua sắm": 10,
        "Giải trí": 8,
        "Hóa đơn": 5,
        "Y tế": 5,
        "Giáo dục": 5,
        "Nhà ở": 5,
        "Khác": 2
    }
    
    categories = list(category_weights.keys())
    weights = list(category_weights.values())
    category = random.choices(categories, weights=weights)[0]
    
    amount = generate_transaction_amount(category, monthly_income, income_class)
    description = random.choice(TRANSACTION_DESCRIPTIONS[category])
    
    return {
        "type": "expense",
        "category": category,
        "description": description,
        "amount": amount,
        "date": date.strftime("%Y-%m-%d")
    }

def generate_user_transactions(user, start_date, end_date):
    """Generate all transactions for a user"""
    transactions = []
    current_date = start_date
    
    monthly_income = user["monthly_income"]
    income_class = user["income_class"]
    
    while current_date <= end_date:
        # Income transactions (1-3 per month)
        income_tx = generate_income_transaction(monthly_income, current_date)
        if income_tx:
            transactions.append(income_tx)
        
        # Expense transactions (10-30 per month depending on income class)
        if income_class in ["low", "lower-mid"]:
            daily_tx_prob = 0.4  # Less frequent transactions
        else:
            daily_tx_prob = 0.7  # More frequent transactions
        
        if random.random() < daily_tx_prob:
            num_tx = random.randint(1, 3)
            for _ in range(num_tx):
                expense_tx = generate_expense_transaction(monthly_income, income_class, current_date)
                transactions.append(expense_tx)
        
        current_date += timedelta(days=1)
    
    return transactions

if __name__ == "__main__":
    print("Transaction generator ready. Use generate_user_transactions() to create data.")

