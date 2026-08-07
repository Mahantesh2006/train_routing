# 🚆 RailConnect // Real-Time Signal & Train Routing Control

A modern, high-performance railway route planning system and real-time signal control room dashboard built with Python (FastAPI), React 18, Tailwind CSS v4, and SQLite.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-v4-38B2AC?style=for-the-badge&logo=tailwind-css)
![Vercel](https://img.shields.io/badge/Vercel-Deployed-000000?style=for-the-badge&logo=vercel)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 📌 Overview

RailConnect is an end-to-end railway routing and telemetry control platform. It calculates direct and 1-stop connecting routes across 22 major Indian railway hubs while evaluating layover buffers ($\Delta t_{min} \le \Delta t \le \Delta t_{max}$), multi-day schedule offsets, and train operating matrix constraints.

It features an **Obsidian Dark-Mode Real-Time Signal & Control Room Dashboard** with an interactive track schematic canvas, live junction switches, signal overlap conflict resolvers, and emergency overrides.

🔗 **Live Vercel Deployment**: [https://train-routing-two.vercel.app](https://train-routing-two.vercel.app)

---

## 📸 Project Preview

![RailConnect project preview](static/railconnect-preview.png)

---

## ✨ Key Features

- **Real-Time Signal & Control Room Dashboard**: Obsidian dark-mode (`#090D16`) dispatch interface with interactive track node schematics, live train velocity gauges, and signal block indicators.
- **Conflict Resolver**: Active alert card detecting track signal overlaps with 1-click *Reroute via Track 2B* and *Hold Signal S-402* actions.
- **Interactive Junction Switches**: Clickable junctions (`J-101` to `J-106`) with live state toggles (`OPEN`, `CLOSED`, `DIVERGING`).
- **Karnataka Regional & National Expansion**: Full route coverage across 22 hubs including **Kalaburagi (Gulbarga)**, **Vijayapura (Bijapur)**, **Belagavi**, **Mysuru**, and **Bengaluru (KSR, Yesvantpur, SMVT)**.
- **Transfer Layover Buffer Control**: Configurable transfer buffer windows with day-of-week validation.
- **Multi-Criteria Ranking**: Rank routes by fastest total journey duration, shortest layover time, lowest fare, or earliest arrival.

---

## 🛠️ Tech Stack

- **Frontend**: React 18, Tailwind CSS v4, Pure SVG Inline Icons, Interactive Canvas & SVG Schematic
- **Backend**: Python 3.10+, FastAPI, SQLite
- **Deployment**: Vercel Serverless (`@vercel/python`, `vercel.json`, `/tmp` DB replication)
- **Testing**: Pytest

---

## 📂 Project Structure

```text
train_routing/
├── api/
│   └── index.py             # Vercel serverless function entrypoint
├── backend/
│   ├── app.py               # FastAPI REST API server & routing endpoints
│   ├── database.py          # SQLite connection pool & Vercel /tmp DB handler
│   ├── routing_engine.py    # Core pathfinding & set-intersection search
│   └── seed_data.py         # 22-station dataset & bi-directional schedules
├── static/
│   ├── index.html           # React 18 SPA Control Room & Planner UI
│   └── styles.css           # Glassmorphism & control room theme utilities
├── test_routing.py          # Pytest unit & integration test suite
├── requirements.txt         # Dependencies
├── vercel.json              # Vercel serverless configuration
├── run.py                   # Local dev server runner
└── README.md
```

---

## ⚙️ Quick Start (Local Setup)

```bash
git clone https://github.com/Mahantesh2006/train_routing.git
cd train_routing
pip install -r requirements.txt
python backend/seed_data.py
python run.py
```

Then open: **http://localhost:8000**

---

## 🧪 Testing

```bash
pytest test_routing.py
```

---

## ▲ Deploy on Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Mahantesh2006/train_routing)

1. **Sign in** to [vercel.com](https://vercel.com/) with GitHub.
2. Click **Add New...** $\rightarrow$ **Project**.
3. Import **`Mahantesh2006/train_routing`**.
4. Vercel automatically detects `vercel.json` and `@vercel/python` configuration.
5. Click **Deploy**.

---

## 📄 License

This project is licensed under the MIT License.

---

<p align="center">
⭐ If you like this project, don't forget to star the repository on GitHub!
</p>
