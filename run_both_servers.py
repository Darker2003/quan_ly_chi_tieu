"""
Script to run both FastAPI backend and Django frontend servers
"""
import subprocess
import sys
import time

def run_servers():
    """Run both servers in separate processes"""
    print("Starting MoneyFlow servers...")
    print("=" * 60)
    
    # Start FastAPI backend
    print("\n[1/2] Starting FastAPI backend on http://127.0.0.1:8001")
    backend_process = subprocess.Popen(
        [sys.executable, "run_backend.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    # Wait a bit for backend to start
    time.sleep(3)
    
    # Start Django frontend
    print("[2/2] Starting Django frontend on http://127.0.0.1:8000")
    frontend_process = subprocess.Popen(
        [sys.executable, "manage.py", "runserver", "127.0.0.1:8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    print("\n" + "=" * 60)
    print("✅ Both servers are running!")
    print("=" * 60)
    print("\n📱 Frontend: http://127.0.0.1:8000")
    print("🔧 Backend API: http://127.0.0.1:8001")
    print("📚 API Docs: http://127.0.0.1:8001/api/docs")
    print("\nPress Ctrl+C to stop both servers")
    print("=" * 60)
    
    try:
        # Keep running and show output
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping servers...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.wait()
        frontend_process.wait()
        print("✅ Servers stopped")

if __name__ == "__main__":
    run_servers()

