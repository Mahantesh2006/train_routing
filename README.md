# 🚆 Train Routing System

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_App-black?style=for-the-badge&logo=flask)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

</p>

---

## 📌 Overview

The **Train Routing System** is an intelligent route-planning application that helps users find train routes between a source and destination—even when no direct train is available.

Instead of showing only direct trains, the system identifies possible transfer stations, suggests connecting trains, and calculates waiting times between trains to provide a practical travel plan.

**RailConnect** implements a 3-Phase Connection Engine that discovers optimal transfer junctions $B$ and enforces layover buffer constraints:

$$\Delta t_{min} \le \text{Departure}(Train_2) - \text{Arrival}(Train_1) \le \Delta t_{max}$$

---

## 📸 Project Preview

![RailConnect project preview](static/railconnect-preview.png)

This screenshot is ready to be used in your GitHub repository README or profile README.

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

- 🚆 Search train routes between two stations
- 🔄 Find indirect routes with train transfers
- ⏱️ Calculate waiting time between connecting trains
- 📍 Display complete journey details
- ⚡ Fast and efficient route search
- 💻 Clean and easy-to-use interface

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend Logic |
| Flask | Web Framework |
| HTML | Frontend |
| CSS | Styling |
| JavaScript | User Interaction |

---

## 📂 Project Structure

```text
train_routing/
│── app.py
│── routes.py
│── templates/
│── static/
│── images/
│── README.md
│── requirements.txt
```

---

# 📸 Screenshots

### 🏠 Home Page

<p align="center">
<img src="images/home.png" width="80%">
</p>

---

### 🔍 Search Route

<p align="center">
<img src="images/search.png" width="80%">
</p>

---

### 🚉 Route Found

<p align="center">
<img src="images/route_found.png" width="80%">
</p>

---

### 🔄 Train Transfer Details

<p align="center">
<img src="images/transfer.png" width="80%">
</p>

---

### 📋 Journey Summary

<p align="center">
<img src="images/journey_summary.png" width="80%">
</p>

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Mahantesh2006/train_routing.git
```

Move into the project directory

```bash
cd train_routing
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open your browser and visit

```
http://127.0.0.1:5000
```

---

## 🚀 Usage

1. Launch the application.
2. Enter the **Source Station**.
3. Enter the **Destination Station**.
4. Click **Search**.
5. View:
   - Available train route
   - Transfer station (if required)
   - Waiting time
   - Complete journey details

---

## 💡 Example

**Input**

```
Source: Bangalore
Destination: Mysore
```

**Output**

```
Train 101
Bangalore → Mandya

Wait: 18 minutes

Train 205
Mandya → Mysore
```

---

## 🎯 Future Improvements

- 🌍 Real-time train schedule integration
- 📍 Live train tracking
- 💰 Fare estimation
- 📱 Mobile responsive interface
- 🗺️ Interactive route visualization
- ⭐ Save favorite routes
- 🔔 Delay notifications

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a new branch.

```bash
git checkout -b feature-name
```

3. Commit your changes.

```bash
git commit -m "Add new feature"
```

4. Push to your branch.

```bash
git push origin feature-name
```

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
