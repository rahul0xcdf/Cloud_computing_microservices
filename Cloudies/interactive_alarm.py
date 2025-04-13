from inputimeout import inputimeout, TimeoutOccurred
import time

def menu():
    print("\nMENU:")
    print("1. Say Hello")
    print("2. Wait and Trigger Alarm")
    print("3. Exit")

def main():
    while True:
        menu()
        try:
            choice = inputimeout(prompt="Choose an option (1-3) within 10 seconds: ", timeout=10)
        except TimeoutOccurred:
            print("\n[ALARM] Timeout occurred. Returning to menu.")
            continue

        if choice == "1":
            print("Hello!")
        elif choice == "2":
            print("Sleeping for 12 seconds...")
            time.sleep(12)
            print("\n[ALARM] Timeout occurred. Returning to menu.")
        elif choice == "3":
            print("Thank you!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
