import bcrypt
import os
import re
import time 
import secrets
import json

LOCK_FILE = "lockout.json"
LOCKOUT_LIMIT = 3          
LOCKOUT_TIME = 300    

SESSION_FILE = "sessions.txt"
USER_DATA_FILE = "users.txt"

def create_session(username):
    token = secrets.token_hex(16)
    return token

def save_session(username, token):
    with open(SESSION_FILE, "w") as f:
        f.write(f"{username},{token}")

def load_lock_data():
    try:
        with open(LOCK_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_lock_data(data):
    with open(LOCK_FILE, "w") as f:
        json.dump(data, f)

def record_failed_attempt(username, lock_data):
    attempts, last_time = lock_data.get(username, (0, 0))

    attempts += 1
    lock_data[username] = (attempts, time.time())

    save_lock_data(lock_data)

def is_account_locked(username, lock_data):
    if username not in lock_data:
        return (False, 0)

    attempts, last_attempt_time = lock_data[username]

    if attempts < LOCKOUT_LIMIT:
        return (False, 0)

    elapsed = time.time() - last_attempt_time

    if elapsed >= LOCKOUT_TIME:
        # Unlock account after timeout
        lock_data[username] = (0, 0)
        save_lock_data(lock_data)
        return (False, 0)

    remaining = LOCKOUT_TIME - elapsed
    return (True, int(remaining))

def hash_password(plain_text_password):

    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_text_password, hashed_password):

    password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def register_user(username, password, role="user"):

    try:
        with open(USER_DATA_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 1:
                    existing_username = parts[0]
                    if existing_username == username:
                        print(f"Error: Username '{username}' already exists.")
                        return False
    except FileNotFoundError:
        pass

    hashed = hash_password(password)

    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username},{hashed},{role}\n")

    print(f"Success: User '{username}' registered successfully with role '{role}'!")
    return True

def user_exists(username):
    try:
    
        with open(USER_DATA_FILE, "r") as f:
            for line in f:
                existing_username, _ = line.strip().split(",", 1)
                if existing_username == username:
                    return True
    except FileNotFoundError:
        
        return False

    return False

def login_user(username, password):
    lock_data = load_lock_data()

    locked, remaining = is_account_locked(username, lock_data)
    if locked:
        minutes = remaining // 60
        seconds = remaining % 60
        print(f"Error: Account for '{username}' is locked. "
              f"Try again in {minutes}m {seconds}s.")
        return False

    try:
        with open(USER_DATA_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    existing_username, stored_hash = parts
                    stored_role = "user"
                elif len(parts) == 3:
                    existing_username, stored_hash, stored_role = parts
                else:
                    continue

                if existing_username == username:
                    if verify_password(password, stored_hash):
                        
                        if username in lock_data:
                            lock_data[username] = (0, 0.0)
                            save_lock_data(lock_data)

                        session_token = create_session(username)
                        save_session(username, session_token)

                        print(f"Success: Welcome, {username}! (role: {stored_role})")
                        print(f"Your session token: {session_token}")
                        return True
                    else:
                        print("Error: Invalid password.")
                        record_failed_attempt(username, lock_data)
                        return False
    except FileNotFoundError:
        print("Error: Username not found.")
        record_failed_attempt(username, lock_data)
        return False

    print("Error: Username not found.")
    record_failed_attempt(username, lock_data)
    return False


def validate_username(username):
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."

    for char in username:
        if not (char.isalnum() or char == "_"):
            return False, "Username can only contain letters, numbers, and underscores."

    return True, ""

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(c.isupper() for c in password):
        return False, "Password must include at least one uppercase letter."
    if not any(c.islower() for c in password):
        return False, "Password must include at least one lowercase letter."
    if not any(c.isdigit() for c in password):
        return False, "Password must include at least one number."
    if not any(c in "!@#$%^&*()-_=+[]{};:'\",.<>?/" for c in password):
        return False, "Password must include at least one special character."
    
    return True, ""

def check_password_strength(password):

    length = len(password)
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[!@#$%^&*()\-_=+\[\]{};:'\",.<>/?]", password))

    score = 0

    if length >= 8:
        score += 1
    if has_lower and has_upper:
        score += 1
    if has_digit:
        score += 1
    if has_special:
        score += 1

    if score <= 1:
        return "Weak"
    elif score == 2:
        return "Medium"
    else:
        return "Strong"

def create_session(username):
    token = secrets.token_hex(16)  # 32-char secure token
    timestamp = time.time()

    with open(SESSION_FILE, "a") as f:
        f.write(f"{username},{token},{timestamp}\n")

    return token
