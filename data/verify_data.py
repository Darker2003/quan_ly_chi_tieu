"""
Verify the generated Vietnamese data in the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.models import User, Transaction, Category
from sqlalchemy import func

def verify_data():
    db = SessionLocal()
    
    try:
        print("=" * 80)
        print("MONEYFLOW DATABASE VERIFICATION")
        print("=" * 80)
        
        # Count users
        user_count = db.query(User).count()
        print(f"\n✓ Total Users: {user_count}")
        
        # Count transactions
        tx_count = db.query(Transaction).count()
        print(f"✓ Total Transactions: {tx_count:,}")
        
        # Count by type
        income_count = db.query(Transaction).filter(Transaction.type == "income").count()
        expense_count = db.query(Transaction).filter(Transaction.type == "expense").count()
        print(f"  - Income Transactions: {income_count:,}")
        print(f"  - Expense Transactions: {expense_count:,}")
        
        # Sample users
        print("\n" + "=" * 80)
        print("SAMPLE USERS (First 5)")
        print("=" * 80)
        
        users = db.query(User).limit(5).all()
        for u in users:
            income_tx = db.query(Transaction).filter(
                Transaction.user_id == u.id,
                Transaction.type == "income"
            ).count()
            expense_tx = db.query(Transaction).filter(
                Transaction.user_id == u.id,
                Transaction.type == "expense"
            ).count()
            
            print(f"\n{u.id}. {u.full_name}")
            print(f"   Email: {u.email}")
            print(f"   Transactions: {income_tx} income, {expense_tx} expense")
        
        # Sample transactions
        print("\n" + "=" * 80)
        print("SAMPLE TRANSACTIONS (First 15)")
        print("=" * 80)
        print(f"{'Date':<12} | {'Type':<8} | {'Amount':>15} | {'Description':<40}")
        print("-" * 80)
        
        txs = db.query(Transaction).limit(15).all()
        for t in txs:
            print(f"{t.date.strftime('%Y-%m-%d'):<12} | {t.type:<8} | {t.amount:>12,} VND | {t.description:<40}")
        
        # Category distribution
        print("\n" + "=" * 80)
        print("TRANSACTION DISTRIBUTION BY CATEGORY")
        print("=" * 80)
        
        categories = db.query(
            Category.name,
            Category.type,
            func.count(Transaction.id).label('count')
        ).join(Transaction).group_by(Category.name, Category.type).all()
        
        print(f"\n{'Category':<20} | {'Type':<8} | {'Count':>10}")
        print("-" * 45)
        for cat_name, cat_type, count in sorted(categories, key=lambda x: x[2], reverse=True):
            print(f"{cat_name:<20} | {cat_type:<8} | {count:>10,}")
        
        # Monthly distribution
        print("\n" + "=" * 80)
        print("TRANSACTIONS BY MONTH")
        print("=" * 80)
        
        monthly = db.query(
            func.strftime('%Y-%m', Transaction.date).label('month'),
            func.count(Transaction.id).label('count')
        ).group_by('month').order_by('month').all()
        
        print(f"\n{'Month':<10} | {'Transactions':>15}")
        print("-" * 30)
        for month, count in monthly:
            print(f"{month:<10} | {count:>15,}")
        
        # Amount statistics
        print("\n" + "=" * 80)
        print("TRANSACTION AMOUNT STATISTICS")
        print("=" * 80)
        
        stats = db.query(
            func.min(Transaction.amount).label('min'),
            func.max(Transaction.amount).label('max'),
            func.avg(Transaction.amount).label('avg')
        ).first()
        
        print(f"\nMinimum Amount: {stats.min:>15,} VND")
        print(f"Maximum Amount: {stats.max:>15,} VND")
        print(f"Average Amount: {int(stats.avg):>15,} VND")
        
        print("\n" + "=" * 80)
        print("✓ DATA VERIFICATION COMPLETE")
        print("=" * 80)
        print("\nThe database contains realistic Vietnamese financial data!")
        print("All users can login with password: password123")
        print("\n")
        
    finally:
        db.close()

if __name__ == "__main__":
    verify_data()

