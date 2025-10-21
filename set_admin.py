"""
Script to set a user as admin
Usage: python set_admin.py <email>
"""

import sys
from backend.database import SessionLocal
from backend.models import User


def set_admin(email: str):
    """Set a user as admin by email"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print(f"❌ User with email '{email}' not found!")
            return False
        
        if user.is_admin:
            print(f"✅ User '{user.full_name}' ({email}) is already an admin!")
            return True
        
        user.is_admin = True
        db.commit()
        print(f"✅ Successfully set '{user.full_name}' ({email}) as admin!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()


def list_admins():
    """List all admin users"""
    db = SessionLocal()
    try:
        admins = db.query(User).filter(User.is_admin == True).all()
        
        if not admins:
            print("No admin users found.")
            return
        
        print(f"\n📋 Admin Users ({len(admins)}):")
        print("-" * 80)
        for admin in admins:
            status = "✅ Active" if admin.is_active else "❌ Inactive"
            print(f"  • {admin.full_name} ({admin.email}) - {status}")
        print("-" * 80)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python set_admin.py <email>")
        print("   or: python set_admin.py --list")
        print("\nExamples:")
        print("  python set_admin.py lethanh@outlook.com")
        print("  python set_admin.py --list")
        sys.exit(1)
    
    if sys.argv[1] == "--list":
        list_admins()
    else:
        email = sys.argv[1]
        if set_admin(email):
            print("\n📋 Current admin users:")
            list_admins()

