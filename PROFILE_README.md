# 🚆 RailConnect

A smart railway routing project that finds indirect and connecting train routes with a modern, interactive web interface.

![RailConnect Preview](static/railconnect-preview.png)

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Pytest](https://img.shields.io/badge/Testing-Pytest-FF6B6B?style=for-the-badge)

## ✨ What this project does

- Finds direct and connecting train routes between two stations
- Supports layover buffer control for realistic transfers
- Ranks results by fastest, shortest layover, lowest fare, or earliest arrival
- Includes a dark glassmorphism UI with an interactive route canvas

## 🛠️ Tech Stack

- Python
- FastAPI
- SQLite
- HTML, CSS, JavaScript
- Pytest

## ▶️ Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/train_routing.git
cd train_routing
pip install -r requirements.txt
python backend/seed_data.py
python run.py
```

Then open: http://localhost:8000

## 📌 Project Highlights

- Advanced 3-phase route search engine
- Realistic transfer timing and buffer validation
- Modern UI for visualizing train connections
- Automated tests for routing logic

## 🔗 Repository

- Main README: [README.md](README.md)
- Project screenshot: [static/railconnect-preview.png](static/railconnect-preview.png)
