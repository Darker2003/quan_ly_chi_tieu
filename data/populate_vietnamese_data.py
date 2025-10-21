"""
Main script to populate MoneyFlow database with realistic Vietnamese user data
Generates 50 users with transactions from May 2024 to May 2025
"""

import json
import os
import sys
from datetime import datetime, timedelta

# Add parent directory to path to import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vietnamese_transaction_generator import generate_user_transactions
from vietnamese_user_data_generator import generate_all_users

from backend.database import Base, SessionLocal, engine
from backend.models import Category, Transaction, User
from backend.security import get_password_hash

# Date range for transactions
START_DATE = datetime(2024, 5, 1)
END_DATE = datetime(2025, 5, 31)

def create_default_categories(db, user_id):
    """Create default categories for a user"""
    default_categories = [
        # Expense categories
        {"name": "Ăn uống", "type": "expense", "is_default": True},
        {"name": "Di chuyển", "type": "expense", "is_default": True},
        {"name": "Mua sắm", "type": "expense", "is_default": True},
        {"name": "Hóa đơn", "type": "expense", "is_default": True},
        {"name": "Giải trí", "type": "expense", "is_default": True},
        {"name": "Y tế", "type": "expense", "is_default": True},
        {"name": "Giáo dục", "type": "expense", "is_default": True},
        {"name": "Nhà ở", "type": "expense", "is_default": True},
        {"name": "Khác", "type": "expense", "is_default": True},
        
        # Income categories
        {"name": "Lương", "type": "income", "is_default": True},
        {"name": "Thưởng", "type": "income", "is_default": True},
        {"name": "Đầu tư", "type": "income", "is_default": True},
        {"name": "Quà tặng", "type": "income", "is_default": True},
        {"name": "Thu nhập khác", "type": "income", "is_default": True},
    ]
    
    category_map = {}
    for cat_data in default_categories:
        category = Category(
            name=cat_data["name"],
            type=cat_data["type"],
            is_default=cat_data["is_default"],
            user_id=user_id
        )
        db.add(category)
        db.flush()  # Get the ID
        category_map[cat_data["name"]] = category.id
    
    return category_map

def populate_database():
    """Main function to populate database with Vietnamese data"""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        print("=" * 80)
        print("POPULATING MONEYFLOW DATABASE WITH VIETNAMESE USER DATA")
        print("=" * 80)
        print(f"Date Range: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}")
        print(f"Generating 50 Vietnamese users with realistic financial data...")
        print()
        
        # Generate user profiles
        user_profiles = generate_all_users(50)
        
        total_users = 0
        total_transactions = 0
        
        # Process each user
        for idx, user_profile in enumerate(user_profiles, 1):
            print(f"[{idx}/50] Creating user: {user_profile['full_name']}")
            print(f"        Email: {user_profile['email']}")
            print(f"        City: {user_profile['city']}, Age: {user_profile['age']}")
            print(f"        Occupation: {user_profile['occupation']}")
            print(f"        Monthly Income: {user_profile['monthly_income']:,} VND")
            print(f"        Income Class: {user_profile['income_class']}")
            
            # Create user in database
            db_user = User(
                email=user_profile['email'],
                full_name=user_profile['full_name'],
                password_hash=get_password_hash(user_profile['password'])
            )
            db.add(db_user)
            db.flush()  # Get user ID
            
            # Create default categories
            category_map = create_default_categories(db, db_user.id)
            
            # Generate transactions
            transactions = generate_user_transactions(
                user_profile,
                START_DATE,
                END_DATE
            )
            
            print(f"        Generating {len(transactions)} transactions...")
            
            # Add transactions to database
            for tx_data in transactions:
                category_id = category_map.get(tx_data['category'])
                if not category_id:
                    continue
                
                transaction = Transaction(
                    amount=tx_data['amount'],
                    description=tx_data['description'],
                    date=datetime.strptime(tx_data['date'], '%Y-%m-%d'),
                    type=tx_data['type'],
                    category_id=category_id,
                    user_id=db_user.id
                )
                db.add(transaction)
            
            total_users += 1
            total_transactions += len(transactions)
            
            # Commit every 5 users to avoid memory issues
            if idx % 5 == 0:
                db.commit()
                print(f"        ✓ Committed batch (Users: {idx}, Transactions: {total_transactions})")
            
            print()
        
        # Final commit
        db.commit()
        
        print("=" * 80)
        print("DATABASE POPULATION COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print(f"Total Users Created: {total_users}")
        print(f"Total Transactions Created: {total_transactions:,}")
        print(f"Average Transactions per User: {total_transactions / total_users:.1f}")
        print()
        print("Sample Login Credentials:")
        print("-" * 80)
        for i in range(min(5, len(user_profiles))):
            print(f"Email: {user_profiles[i]['email']}")
            print(f"Password: {user_profiles[i]['password']}")
            print(f"Name: {user_profiles[i]['full_name']}")
            print()
        
        # Generate summary statistics
        print("=" * 80)
        print("DATA SUMMARY")
        print("=" * 80)
        
        # Income class distribution
        income_classes = {}
        for user in user_profiles:
            income_class = user['income_class']
            income_classes[income_class] = income_classes.get(income_class, 0) + 1
        
        print("\nIncome Class Distribution:")
        for income_class, count in sorted(income_classes.items()):
            percentage = (count / len(user_profiles)) * 100
            print(f"  {income_class:12s}: {count:2d} users ({percentage:5.1f}%)")
        
        # City distribution
        cities = {}
        for user in user_profiles:
            city = user['city']
            cities[city] = cities.get(city, 0) + 1
        
        print("\nCity Distribution:")
        for city, count in sorted(cities.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(user_profiles)) * 100
            print(f"  {city:20s}: {count:2d} users ({percentage:5.1f}%)")
        
        # Save user profiles to JSON for reference
        with open('data/generated_users.json', 'w', encoding='utf-8') as f:
            json.dump(user_profiles, f, ensure_ascii=False, indent=2)
        
        print("\n✓ User profiles saved to: data/generated_users.json")
        print()
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    populate_database()

