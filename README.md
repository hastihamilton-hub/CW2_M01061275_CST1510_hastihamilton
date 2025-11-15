# Project for module CST1510
Week 7: Secure Authentication System

Student Name: Hasti Hamilton
Student ID: M01061275
Course: CST1510 – CW2 – Multi-Domain Intelligence Platform

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
