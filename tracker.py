import csv
import os
from datetime import date

FILE_NAME = "applications.csv"
FIELDS = ["id", "company", "role", "date_applied", "status", "notes"]


def ensure_file_exists():
    """Create applications.csv with headers if it doesn't exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(FIELDS)


def load_apps():
    """Load all applications from the CSV file."""
    ensure_file_exists()
    apps = []
    with open(FILE_NAME, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            apps.append(row)
    return apps


def save_apps(apps):
    """Save all applications back to the CSV file."""
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(apps)


def get_next_id(apps):
    """Return the next ID number."""
    if not apps:
        return 1
    return max(int(a["id"]) for a in apps) + 1


def add_application():
    apps = load_apps()

    company = input("Company: ").strip()
    role = input("Role: ").strip()

    if company == "" or role == "":
        print("\n❌ Company and Role are required.\n")
        return

    date_applied = input("Date applied (YYYY-MM-DD) [Enter for today]: ").strip()
    if date_applied == "":
        date_applied = str(date.today())

    status = input("Status (Applied/Interview/Rejected/Offer) [default Applied]: ").strip()
    if status == "":
        status = "Applied"

    notes = input("Notes (optional): ").strip()

    new_app = {
        "id": str(get_next_id(apps)),
        "company": company,
        "role": role,
        "date_applied": date_applied,
        "status": status,
        "notes": notes
    }

    apps.append(new_app)
    save_apps(apps)

    print("\n✅ Saved!\n")


def view_all():
    apps = load_apps()

    if not apps:
        print("\nNo applications yet.\n")
        return

    print("\n--- Applications ---")
    for a in apps:
        print(f'#{a["id"]} | {a["company"]} | {a["role"]} | {a["date_applied"]} | {a["status"]}')
        if a["notes"]:
            print(f'Notes: {a["notes"]}')
        print()


def search():
    apps = load_apps()
    keyword = input("Search company/role: ").strip().lower()

    results = []
    for a in apps:
        if keyword in a["company"].lower() or keyword in a["role"].lower():
            results.append(a)

    if not results:
        print("\nNo matches found.\n")
        return

    print("\n--- Results ---")
    for a in results:
        print(f'#{a["id"]} | {a["company"]} | {a["role"]} | {a["status"]}')


def update_status():
    apps = load_apps()
    app_id = input("Enter ID to update: ").strip()

    for a in apps:
        if a["id"] == app_id:
            print(f'Current status: {a["status"]}')
            new_status = input("New status (Applied/Interview/Rejected/Offer): ").strip()
            if new_status == "":
                print("\nNo change made.\n")
                return
            a["status"] = new_status
            save_apps(apps)
            print("\n✅ Status updated!\n")
            return

    print("\n❌ ID not found.\n")


def menu():
    while True:
        print("=== Internship Tracker ===")
        print("1) Add application")
        print("2) View all")
        print("3) Search")
        print("4) Update status")
        print("5) Exit")

        choice = input("Choose (1-5): ").strip()

        if choice == "1":
            add_application()
        elif choice == "2":
            view_all()
        elif choice == "3":
            search()
        elif choice == "4":
            update_status()
        elif choice == "5":
            print("\nGood luck — keep applying daily 💪\n")
            break
        else:
            print("\nPlease choose 1-5.\n")


if __name__ == "__main__":
    menu()
