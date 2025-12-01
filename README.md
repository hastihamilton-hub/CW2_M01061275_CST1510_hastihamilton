# Project for module CST1510

Student Name: Hasti Hamilton
Student ID: M01061275
Course: CST1510 – CW2 – Multi-Domain Intelligence Platform

Week 7: Secure Authentication System

Project Description:
This project implements a secure command-line authentication system in Python.
It allows users to register accounts and log in using properly hashed and verified passwords.
The system uses bcrypt for security, validates user inputs, and stores user credentials in a local file.

Features:
- Secure password hashing using bcrypt (automatic salting)
- User registration with duplicate username prevention
- User login with password verification
- Input validation for usernames and passwords
- Local file storage (users.txt) for user data
- Clear success/error messages
- Menu-driven interface for easy interaction

Technical Implementation:
- Hashing Algorithm: bcrypt (one-way hashing + automatic salting)
- Data Storage: Plain text file (users.txt) using comma-separated values
- Password Security: No plaintext passwords stored — only salted hashes
- Validation Rules:
    - Username: must be ≥ 3 characters, letters/numbers/underscore only
    - Password: ≥ 8 characters, must contain
    - uppercase letter
    - lowercase letter
    - number
    - special character

All core functionalities were tested:

Test 1: Register New User
- Input: username alice, password SecurePass123
- Expected: Success → user registered
- Result: PASS

Test 2: Duplicate Registration
- Try registering alice again
- Expected: Error → user already exists
- Result: PASS

Test 3: Successful Login
- Login with correct credentials
- Expected: Welcome message
- Result: PASS

Test 4: Wrong Password
- Login with incorrect password
- Expected: Invalid password
- Result: PASS

Test 5: Non-existent User
- Login using username bob
- Expected: Username not found
- Result: PASS

How to Run the Program:

1. Install dependencies:
pip3 install bcrypt

2. Run the main program:
python main.py

3. Follow the interactive menu to register or log in.

Files:
- auth.py  # hashing, validation, registration, login
- main.py  # menu + main program loop
- users.txt  # auto-generated user storage
- README.md  # documentation

Week 8: Database System for Multi-Domain Intelligence Platform

Project Description:
This project implements the full database system required for Week 8 of the Intelligence Platform project.
The program creates an SQLite database, builds all required tables, loads three CSV datasets, and provides full CRUD (Create, Read, Update, Delete) functionality for all domains.
The system also includes secure authentication using bcrypt, user migration from a legacy text file, and analytical SQL queries.

Features:
- SQLite database connection and automatic creation
- Four fully implemented tables:
    - users
    - cyber_incidents
    - datasets_metadata
    - it_tickets
- CSV file loading for all domains
- Secure password hashing (bcrypt)
- User registration and login
- User migration from users.txt
- CRUD operations for:
    - Users
    - Incidents
    - Datasets
    - IT Tickets
- Analytical SQL queries using parameterized statements
- Full automated test script

Technical Implementation:
Database:
- Engine: SQLite
- File: DATA/intelligence_platform.db
- Tables created using SQL in schema.py
- Safe queries using ? placeholders (prevents SQL injection)

Authentication:
- bcrypt hashing with automatically generated salts
- Secure compare for login
- Duplicate username checking
- Migration of existing users from users.txt

CSV files loaded:
- cyber_incidents.csv
- datasets_metadata.csv
- it_tickets.csv
Each CSV is inserted row-by-row using manual insert statements.

CRUD Modules:
- users.py — user CRUD
- incidents.py — incident CRUD
- datasets.py — dataset CRUD
- tickets.py — ticket CRUD
All CRUD operations were successfully tested in main2.py

All core database functions were tested:
Test 1: Authentication:
- Register test user → PASS
- Login (correct password) → PASS
- Login (wrong password) → PASS

Test 2: CRUD Operations:
- Create incident → PASS
- Read incident → PASS
- Update incident → PASS
- Delete incident → PASS

Test 3: Analytical Queries:
- Incidents grouped by type → PASS
- High severity incidents → PASS

All Week 8 required tests passed successfully.

Week 9: Streamlit Multi-Page App (Login + Dashboard):

This week I created a simple multi-page Streamlit application to demonstrate UI elements, widgets, layouts, session management, and navigation. The app includes a Login/Register page and a protected Dashboard page that only logged-in users can access.

Streamlit Fundamentals (Practice Files):
As part of the Week 9 tutorial, I practiced the core Streamlit features by building four demo files inside the week9_part1 folder:

- basic_page_elements.py – displays titles, headers, markdown, images, and sample data.

- basic_interactive_widgets.py – demonstrates user input components such as text inputs, buttons, sliders, checkboxes, and select boxes.

- layout_demo.py – explores Streamlit layouts including sidebars, columns, expanders, and wide-page configuration.

- mini_dashboard.py – combines filters, charts, layouts, and example data into a small working dashboard.

Main Features of the Week 9 App:
- Multi-page Streamlit structure (Home.py + pages/1_Dashboard.py)
- Login and Register tabs using st.tabs()
- Session management using st.session_state
- Page navigation using st.switch_page()
- Widgets demonstrated: text inputs, buttons, sliders, checkboxes, selectboxes, multiselects
- Basic charts using Streamlit built-ins: line chart, bar chart
- Example sidebar filters and expandable sections
- Basic “mini dashboard” layout using columns and sidebars

How to Run:

1. Install Streamlit:
pip install streamlit

2. Run the app from inside the week9_app folder:
streamlit run .\week9_app\Home.py

File Structure
week9_app/
│── Home.py                 # Login/Register page
└── pages/
    └── 1_Dashboard.py      # Protected dashboard page

Summary:
The goal of Week 9 was to learn how to build interactive Streamlit web applications.
I practiced text elements, widgets, charts, layouts, session state, and multi-page navigation.
The final result is a working login system and a simple dashboard page that demonstrates real Streamlit functionality.