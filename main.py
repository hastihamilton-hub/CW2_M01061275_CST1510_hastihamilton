from auth import register_user, login_user

def menu():
    print("*" * 30)
    print("* Welcome to my system *")
    print("Choose from the following options:")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    print("*" * 30)

def main():
    while True:
        menu()
        choice = input("> ").strip()

        if choice == "1":
            username = input("Enter a username: ").strip()
            password = input("Enter a password: ").strip()
            register_user(username, password)

        elif choice == "2":
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

