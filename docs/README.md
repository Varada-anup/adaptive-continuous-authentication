# Adaptive Continuous Authentication Using Behavioural Biometrics

## 📌 Project Overview

This project implements an **Adaptive Continuous Authentication System** that verifies users continuously based on their behavioural patterns such as typing dynamics and mouse movements.

Unlike traditional login systems, this system keeps monitoring user behaviour **throughout the session** to detect suspicious activity and intrusions.

---

## 🚀 Key Features

* Continuous authentication after login
* Behavioural biometrics (keystroke + mouse dynamics)
* Real-time anomaly detection
* Intruder detection with session termination
* Adaptive learning of user behaviour over time
* Email alert system for suspicious activity

---

## 🧠 Technologies Used

* Python (Flask)
* NumPy
* HTML, CSS, JavaScript
* SQLite (users.db)

---

## ⚙️ System Workflow

1. User logs in
2. System collects behavioural data:

   * Keystroke timings
   * Mouse movement patterns
3. Feature extraction is performed
4. Decision engine compares behaviour with stored profile
5. System classifies user as:

   * Genuine
   * Suspicious
   * Intruder
6. If intruder detected:

   * Session terminated
   * Alert email sent

---

## 📊 Core Modules

### 1. Feature Extractor

Extracts behavioural features such as:

* Typing speed
* Key hold time
* Mouse movement speed

### 2. Decision Engine

* Calculates similarity score
* Uses threshold-based classification
* Maintains strike system for anomalies

### 3. Adaptive Learning

* Updates user profile over time
* Uses Exponential Moving Average (EMA)

### 4. Alert System

* Sends email alerts when intrusion is detected

---

## ▶️ How to Run the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python backend/app.py
```

Open browser:

```
http://localhost:5000
```

---

## 🔐 Security Features

* Continuous verification during session
* Behaviour-based authentication
* Intrusion detection with automatic logout
* Email alert system

---

## 📌 Future Improvements

* Machine learning-based classification
* Multi-user scalability
* Mobile behaviour tracking
* Advanced anomaly detection models

---

## 👩‍💻 Author
## Screenshots

### Login Page

![Login Page](screenshots/login-page.png)

### Dashboard

![Dashboard](screenshots/interaction_area.png)

### Intruder Detection

![Intruder Detection](screenshots/intruder-detected.png)

Varada Anup
MCA Student

---
