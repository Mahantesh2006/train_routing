# 🚆 RailConnect: Indirect Train & Connecting Route Planner

> An advanced railway route search and connecting train engine built with **Python**, **FastAPI**, **SQLite**, and a modern **Dark Glassmorphic Web UI**.

![RailConnect UI Architecture](https://img.shields.io/badge/Architecture-FastAPI%20%2B%20SQLite%20%2B%20Canvas-00f2fe?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-green?style=for-the-badge)

---

## 📌 Overview

Finding direct trains between two major hubs is straightforward ($\text{WHERE origin} = A \text{ AND destination} = C$). However, when direct trains are sold out or unavailable, finding **1-stop connecting routes** requires evaluating transfer junctions, operating calendar days, platform layover windows, and multi-day train schedules.

**RailConnect** implements a 3-Phase Connection Engine that discovers optimal transfer junctions $B$ and enforces layover buffer constraints:

$$\Delta t_{min} \le \text{Departure}(Train_2) - \text{Arrival}(Train_1) \le \Delta t_{max}$$

---

## 📐 System Architecture

```
 [ Client / Frontend (HTML5 + Glassmorphism CSS + Canvas Map) ]
                            │
                            ▼  (POST /api/search: Origin, Destination, Date, Buffer Sliders)
 [ FastAPI REST API Layer (backend/app.py) ]
                            │
                            ▼
 [ 3-Phase Connection Engine (backend/routing_engine.py) ] ◄─── [ SQLite Database (railway.db) ]
                            │
                            ▼  (Validates Operating Days, Midnight Crossovers & Layover Windows)
 [ Multi-Criteria Ranking (Fastest, Shortest Layover, Lowest Fare) ]
                            │
                            ▼
 [ JSON Route Timeline Response ]
```

---

## ⚡ Core Search Logic (3-Phase Routing Engine)

### Phase 1: Identify Junction Stations
Query all candidate transfer stations $B$ forming the set intersection:
$$\text{Candidate Junctions } B = \{ \text{Stations reachable from Origin } A \} \cap \{ \text{Stations connecting to Destination } C \}$$

### Phase 2: Apply Time & Day-of-Week Constraints
For each candidate junction $B$ and pairs $(Train_1, Train_2)$:
- **Operating Day Matching**: Check train run bitmasks (`runs_mon` ... `runs_sun`) accounting for multi-day offsets (`day_number`).
- **Buffer Window Filtering**: Ensure wait time at Junction $B$ satisfies:
  $$\Delta t_{min} \le \text{Wait Time} \le \Delta t_{max}$$

### Phase 3: Rank & Sort Options
Sort generated routes by user preference:
- ⚡ **Total Journey Duration** (Origin $A \rightarrow$ Destination $C$)
- ⏳ **Shortest Layover Duration**
- 💎 **Lowest Fare**
- 🌅 **Earliest Final Arrival**

---

## ✨ Features

- 🎨 **Dark Glassmorphism Interface**: Sleek glowing UI, animated journey timelines, platform transfer badges.
- 🎚️ **Dynamic Buffer Sliders**: Custom range controls for minimum buffer ($\Delta t_{min}$) and maximum layover ($\Delta t_{max}$).
- 🌐 **Interactive Railway Canvas**: HTML5 Canvas rendering station nodes and connecting train route edges.
- 🧪 **Unit Test Suite**: Built-in `pytest` suite testing direct routing, connecting search, and sorting logic.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure you have **Python 3.10+** and `git` installed.

### 2. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/train_routing.git
cd train_routing
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize & Seed Database
```bash
python backend/seed_data.py
```

### 5. Run the Server
```bash
python run.py
```
Open your browser and navigate to **`http://localhost:8000`**.

---

## 🧪 Running Tests

To run the automated `pytest` suite:
```bash
pytest test_routing.py
```

---

## 📂 Project Structure

```
train_routing/
├── backend/
│   ├── app.py              # FastAPI REST endpoints & static server
│   ├── database.py         # SQLite schema initialization
│   ├── routing_engine.py   # 3-Phase Connection Engine & buffer validation
│   └── seed_data.py        # Seed script for 16 stations & 40+ train schedules
├── static/
│   ├── index.html          # Web UI layout & control matrix
│   ├── styles.css          # Dark glassmorphism stylesheet
│   └── app.js              # Fetch handlers, route rendering & canvas graph
├── test_routing.py         # Pytest unit tests
├── requirements.txt        # Python dependencies
├── run.py                  # Server entrypoint script
└── README.md               # Documentation
```

---

## 📜 License

Distributed under the **MIT License**.
