# 🚆 RailConnect

A smart railway route planner that helps users find direct and connecting train options with realistic transfer timing.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 📌 Overview

RailConnect is a web-based train routing system that searches for both direct and indirect routes. It evaluates transfer stations, waiting time between trains, and route ranking to suggest practical travel plans.

---

## 📸 Project Preview

![RailConnect project preview](static/railconnect-preview.png)

---

## ✨ Features

- Find direct and connecting train routes
- Support layover buffer control for realistic transfers
- Rank routes by fastest travel, shortest layover, lowest fare, or earliest arrival
- Provide a modern dark-themed web interface with route visualization

---

## 🛠️ Tech Stack

- Python
- FastAPI
- SQLite
- HTML, CSS, JavaScript
- Pytest

---

## 📂 Project Structure

```text
train_routing/
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── routing_engine.py
│   └── seed_data.py
├── static/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── test_routing.py
├── requirements.txt
├── run.py
└── README.md
```

---

## ⚙️ Quick Start

```bash
git clone https://github.com/Mahantesh2006/train_routing.git
cd train_routing
pip install -r requirements.txt
python backend/seed_data.py
python run.py
```

Then open: http://localhost:8000

---

## 🧪 Testing

```bash
pytest test_routing.py
```

---

## 🤝 Contributing

Contributions are welcome. Feel free to fork the repository and submit a pull request.

5. Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Mahantesh Ingale**

GitHub: https://github.com/Mahantesh2006

---

<p align="center">
⭐ If you like this project, don't forget to star the repository!
</p>
