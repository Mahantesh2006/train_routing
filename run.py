import uvicorn
import os
import sys

# Ensure root and backend directories are in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))

if __name__ == "__main__":
    print("Starting RailConnect Indirect Train & Connecting Route Planner...")
    print("Web Application available at: http://localhost:8000")
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=True)
