"""
Check user data in the database
"""

from backend.database import SessionLocal
from backend.models import User, Transaction
from sqlalchemy import func

db = SessionLocal()

print("=" * 70)
print("CHECKING USER DATA")
print("=" * 70)

# Check user
user = db.query(User).filter(User.email == 'lethanh@outlook.com').first()

if not user:
    print("❌ User 'lethanh@outlook.com' NOT FOUND!")
    print("\nAvailable users:")
    users = db.query(User).limit(5).all()
    for u in users:
        print(f"  - {u.email} ({u.full_name})")
else:
    print(f"✅ User Found: {user.full_name}")
    print(f"   Email: {user.email}")
    print(f"   User ID: {user.id}")
    print(f"   Is Active: {user.is_active}")
    print(f"   Is Admin: {user.is_admin}")
    print()
    
    # Check transactions
    tx_count = db.query(Transaction).filter(Transaction.user_id == user.id).count()
    print(f"📊 Transaction Statistics:")
    print(f"   Total Transactions: {tx_count}")
    
    if tx_count > 0:
        income_count = db.query(Transaction).filter(
            Transaction.user_id == user.id,
            Transaction.type == 'income'
        ).count()
        
        expense_count = db.query(Transaction).filter(
            Transaction.user_id == user.id,
            Transaction.type == 'expense'
        ).count()
        
        income_total = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user.id,
            Transaction.type == 'income'
        ).scalar() or 0
        
        expense_total = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user.id,
            Transaction.type == 'expense'
        ).scalar() or 0
        
        print(f"   Income Transactions: {income_count}")
        print(f"   Expense Transactions: {expense_count}")
        print()
        print(f"💰 Financial Summary:")
        print(f"   Total Income:  {income_total:>15,.0f} VND")
        print(f"   Total Expense: {expense_total:>15,.0f} VND")
        print(f"   Balance:       {income_total - expense_total:>15,.0f} VND")
        print()
        
        # Show sample transactions
        print("📝 Sample Transactions (last 5):")
        recent_txs = db.query(Transaction).filter(
            Transaction.user_id == user.id
        ).order_by(Transaction.date.desc()).limit(5).all()
        
        for tx in recent_txs:
            print(f"   {tx.date} | {tx.type:7s} | {tx.amount:>12,.0f} VND | {tx.description}")
    else:
        print("   ⚠️  No transactions found for this user!")
        print()
        print("   This is why the dashboard shows 0 for all values.")
        print()
        print("   To add transactions for this user:")
        print("   1. Login to the web app")
        print("   2. Click 'Thêm Giao Dịch' (Add Transaction)")
        print("   3. Fill in the transaction details")
        print()
        print("   OR use another user account that has data:")
        users_with_data = db.query(User).join(Transaction).group_by(User.id).limit(5).all()
        if users_with_data:
            print("\n   Users with transaction data:")
            for u in users_with_data:
                tx_cnt = db.query(Transaction).filter(Transaction.user_id == u.id).count()
                print(f"   - {u.email} ({u.full_name}) - {tx_cnt} transactions")

print("=" * 70)

db.close()

