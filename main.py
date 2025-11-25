from auth import register_user, login_user, validate_username, validate_password, check_password_strength

def menu():
    print("*" * 40)
    print("*        Welcome to my system        *")
    print("*" * 40)
    print("Choose from the following options:")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    print("*" * 40)

def main():
    while True:
        menu()
        choice = input("> ").strip()

        if choice == "1":
            print("\n--- USER REGISTRATION ---")

            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()

            # Validate password strength & rules
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            # Show password strength
            strength = check_password_strength(password)
            print(f"Password strength: {strength}")

            # NEW: choose a role
            print("\nChoose a role for this user:")
            print("1. user")
            print("2. admin")
            print("3. analyst")
            role_choice = input("> ").strip()

            if role_choice == "2":
                role = "admin"
            elif role_choice == "3":
                role = "analyst"
            else:
                role = "user"   # default

            # Confirm password
            confirm = input("Confirm password: ").strip()
            if confirm != password:
                print("Error: Passwords do not match.")
                continue

            # Register user WITH ROLE
            register_user(username, password, role)

        elif choice == "2":
            print("\n--- USER LOGIN ---")

            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            if login_user(username, password):
                print("You have logged in!!")
            else:
                print("Incorrect login!!!")

        elif choice == "3":
            print("Goodbye!!!")
            break

        else:
            print("Invalid choice! Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()

    