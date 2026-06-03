# 🗳 Online Voting System

A modern, secure, and responsive Online Voting System built using Flask, MySQL, HTML, CSS, and JavaScript.

The platform enables users to register, log in, cast votes securely, and view election results while allowing administrators to manage candidates, election schedules, and result publication.

---

# 🌐 Live Demo

https://online-voting-system-1-zghy.onrender.com

---

# 🚀 Features

## 👤 User Features

* User Registration & Login
* Secure Password Hashing
* One Vote Per User
* Election Status Tracking
* Real-Time Countdown Timers
* Responsive Voting Interface
* Public Election Results
* Vote Percentage Calculation
* Winner & Tie Detection
* Session Management

---

## 🛠 Admin Features

* Admin Authentication
* Add Candidates
* Delete Candidates
* Manage Election Timings
* Configure Result Publish Time
* Automatic Vote Reset for New Elections
* Dynamic Election Management
* Candidate Duplicate Prevention

---

# 🧠 Advanced Functionalities

* Election Start & End Validation
* Result Visibility Control
* Duplicate Candidate Prevention
* Duplicate Party Prevention
* Duplicate Email Prevention
* Automatic Vote Reset
* No Participation Handling
* Tie Detection Logic
* Responsive Design
* Public Result Publishing

---

# 💻 Tech Stack

## Frontend

* HTML5
* CSS3
* JavaScript

## Backend

* Flask (Python)

## Database

* MySQL

## Deployment

* Render
* Railway MySQL

---

# 🏗 System Architecture

```text
User
  │
  ▼
Flask Application
  │
  ▼
MySQL Database
  │
  ▼
Election Management
  │
  ▼
Voting & Results
```

---

# 📂 Project Structure

```bash
Online-Voting-System/
│
├── static/
│
├── templates/
│
├── screenshots/
│
├── app.py
│
├── requirements.txt
│
├── README.md
│
├── LICENSE
│
├── CONTRIBUTING.md
│
├── CODE_OF_CONDUCT.md
│
├── .env.example
│
└── .gitignore
```

---

# ⚙️ Installation & Setup

## 1. Clone Repository

```bash
git clone https://github.com/your-username/Online-Voting-System.git
```

---

## 2. Navigate To Project

```bash
cd Online-Voting-System
```

---

## 3. Create Virtual Environment

```bash
python -m venv venv
```

---

## 4. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 6. Create MySQL Database

```sql
CREATE DATABASE voting_system;
```

---

## 7. Configure Environment Variables

Create a `.env` file:

```env
MYSQLHOST=localhost
MYSQLUSER=root
MYSQLPASSWORD=your_password
MYSQLDATABASE=voting_system
MYSQLPORT=3306

ADMIN_EMAIL=admin@gmail.com
ADMIN_PASSWORD=your_password
```

---

## 8. Run Application

```bash
python app.py
```

---

# 📸 Screenshots

## 🏠 Home Page

![Home Page](screenshots/home-page.png)

## 📝 Registration Page

![Registration Page](screenshots/register-page.png)

## 🔐 Login Page

![Login Page](screenshots/login-page.png)

## 🗳 Voting Page

![Voting Page](screenshots/vote-page.png)

## 📊 Results Page

![Results Page](screenshots/results-page.png)

## ⚙️ Admin Dashboard

![Admin Dashboard](screenshots/admin-dashboard.png)

---

# 🔒 Security Features

* Password Hashing using Werkzeug
* Session Management
* Admin Authentication
* Duplicate Vote Prevention
* Duplicate Email Prevention
* Candidate Validation
* Party Validation

---

# 📱 Responsive Design

The application is fully responsive and works across:

* Desktop
* Laptop
* Tablet
* Mobile Devices

---

# 🎯 Open Source Contribution Areas

Contributors can work on:

* Dark Mode
* Email OTP Verification
* Election History Tracking
* Candidate Profile Pictures
* Export Results as PDF
* Live Analytics Dashboard
* Accessibility Improvements
* Mobile UI Enhancements
* Multi-Admin Support
* Email Notifications

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push to your fork.
5. Create a Pull Request.

Please read the CONTRIBUTING.md file before contributing.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👩‍💻 Developed By

**Yashaswini**

---

# ⭐ Support

If you found this project useful, consider giving it a star on GitHub.

It helps the project reach more developers and contributors.
