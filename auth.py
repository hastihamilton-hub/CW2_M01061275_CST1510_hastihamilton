import bcrypt
import os
USER_DATA_FILE = "users.txt"


def hash_password(plain_text_password):

    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_text_password, hashed_password):

    password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def register_user(username, password):
    try:
        with open(USER_DATA_FILE, "r") as f:
            for line in f:
                existing_username, _ = line.strip().split(",", 1)
                if existing_username == username:
                    print("Username already exists.")
                    return False
    except FileNotFoundError:        
        pass

    hashed_password = hash_password(password)

    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username},{hashed_password}\n")

    print("User registered successfully.")
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
    try:
       
        with open(USER_DATA_FILE, "r") as f:
            for line in f:
                
                existing_username, stored_hash = line.strip().split(",", 1)
                
                
                if existing_username == username:
                    
                    if verify_password(password, stored_hash):
                        print("Login successful!")
                        return True
                    else:
                        print("Incorrect password.")
                        return False

    except FileNotFoundError:
        print("No users registered yet.")
        return False

    print("Username not found.")
    return False

#register_user("hasti", "hello123")
#login_user("hasti", "hello123")  
#login_user("hasti", "wrongpass")  

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
