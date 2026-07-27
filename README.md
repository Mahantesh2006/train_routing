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
