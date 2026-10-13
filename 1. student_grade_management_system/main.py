"""Student Grade Management System
Command-line application: add students, store marks, get average, grade and rank.
Data is saved in students.json so it survives between runs."""

import json
import os

DATA_FILE = "students.json"

# ---------- file handling ----------
def load_data():
    """Read students from the JSON file. Return empty dict if none yet."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Data file is corrupted, starting fresh.")
        return {}

def save_data(students):
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=4)

# ---------- Calculations ----------
def calculate_average(marks):
    return sum(marks.values()) / len(marks) if marks else 0

def get_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    return "E"

def get_rankings(students):
    """Return list of (name, average) sorted highest first."""
    scores = [(name, calculate_average(data["marks"])) for name, data in students.items()]
    return sorted(scores, key=lambda x: x[1], reverse=True)

# ---------- input helpers ----------
def read_mark(subject):
    """Keep asking until the user enters a number between 0 and 100."""
    while True:
        try:
            mark = float(input(f" Marks in {subject} (0-100): "))
            if 0 <= mark <= 100:
                return mark
            print(" Marks must be between 0 and 100.")
        except ValueError:
            print(" Please enter a valid number.")

# ---------- menu actions ----------
def add_student(students):
    name = input("Student name:").strip().title()
    if not name:
        print("Name cannot be empty.")
        return 
    if name in students:
        print(f"{name} already exists.")
        return

    marks = {}
    while True:
        subject = input("Subject name (or press Enter to finish): ").strip().title()
        if subject == "":
            break
        marks[subject] = read_mark(subject)

    if not marks:
        print("No marks entered, student not added.")
        return

    students[name] = {"marks": marks}
    save_data(students)
    print(f"{name} added.")

def view_student(students):
    name = input("Student name: ").strip().title()
    if name not in students:
        print("Student not found.")
        return
    marks = students[name]["marks"]
    avg = calculate_average(marks)
    rank = [n for n, _ in get_rankings(students)].index(name) + 1

    print(f"\n{name}")
    for subject, mark in marks.items():
        print(f"  {subject}: {mark}")
    print(f" Average: {avg:.2f} | Grade: {get_grade(avg)} | Rank: {rank}/{len(students)}")

def show_rankings(students):
    if not students:
        print("No students yet.")
        return
    print(f"\n{'Rank':<6}{'Name':<15}{'Average':<10}Grade")
    for i, (name, avg) in enumerate(get_rankings(students), start=1):
        print(f"{i:<6}{name:<15}{avg:<10.2f}{get_grade(avg)}")

def delete_student(students):
    name = input("Student to delete:").strip().title()
    if name in students:
        del students[name]
        save_data(students)
        print(f"{name} deleted.")
    else:
        print("Student not found.")

# ---------- main loop ----------
def main():
    students = load_data()
    while True:
        print("\n=== Student Grade Management System ===")
        print("1. Add student")
        print("2. View student")
        print("3. Show rankings")
        print("4. Delete student")
        print("5. Exit")
        choice = input("Choose (1-5): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_student(students)
        elif choice == "3":
            show_rankings(students)
        elif choice == "4":
            delete_student(students)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, enter a number from 1 to 5.")

if __name__ == "__main__":
    main()