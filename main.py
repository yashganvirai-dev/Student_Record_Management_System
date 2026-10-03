import csv
import json
import os

CSV_FILE = "students.csv"
JSON_FILE = "students.json"


def load_students():
    """Load student records from JSON if available, otherwise from CSV."""
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
        except (json.JSONDecodeError, OSError):
            print("Warning: Could not read JSON file. Loading CSV instead.")

    students = []
    if os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                students = list(reader)
        except OSError:
            print("Warning: Could not read CSV file.")

    return students


def save_students(students):
    """Save records to both CSV and JSON."""
    fieldnames = ["id", "name", "age", "course", "marks"]

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)

    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)


def get_student_id():
    while True:
        student_id = input("Enter student ID: ").strip()
        if student_id:
            return student_id
        print("ID cannot be empty.")


def add_student(students):
    student_id = get_student_id()

    if any(student["id"] == student_id for student in students):
        print("A student with this ID already exists.")
        return

    name = input("Enter name: ").strip()

    try:
        age = int(input("Enter age: "))
        marks = float(input("Enter marks: "))
    except ValueError:
        print("Please enter valid numbers for age and marks.")
        return

    course = input("Enter course: ").strip()

    student = {
        "id": student_id,
        "name": name,
        "age": str(age),
        "course": course,
        "marks": str(marks)
    }

    students.append(student)
    save_students(students)
    print("Student added successfully.")


def view_students(students):
    if not students:
        print("No student records found.")
        return

    print("\n" + "-" * 75)
    print(f"{'ID':<10}{'Name':<20}{'Age':<8}{'Course':<20}{'Marks':<10}")
    print("-" * 75)

    for student in students:
        print(
            f"{student['id']:<10}"
            f"{student['name']:<20}"
            f"{student['age']:<8}"
            f"{student['course']:<20}"
            f"{student['marks']:<10}"
        )

    print("-" * 75)


def search_student(students):
    student_id = get_student_id()

    for student in students:
        if student["id"] == student_id:
            print("\nStudent Found")
            print(f"ID     : {student['id']}")
            print(f"Name   : {student['name']}")
            print(f"Age    : {student['age']}")
            print(f"Course : {student['course']}")
            print(f"Marks  : {student['marks']}")
            return

    print("Student not found.")


def update_student(students):
    student_id = get_student_id()

    for student in students:
        if student["id"] == student_id:
            print("Press Enter to keep the current value.")

            name = input(f"Name [{student['name']}]: ").strip()
            age_input = input(f"Age [{student['age']}]: ").strip()
            course = input(f"Course [{student['course']}]: ").strip()
            marks_input = input(f"Marks [{student['marks']}]: ").strip()

            if name:
                student["name"] = name
            if age_input:
                try:
                    student["age"] = str(int(age_input))
                except ValueError:
                    print("Invalid age. Keeping old value.")

            if course:
                student["course"] = course
            if marks_input:
                try:
                    student["marks"] = str(float(marks_input))
                except ValueError:
                    print("Invalid marks. Keeping old value.")

            save_students(students)
            print("Student updated successfully.")
            return

    print("Student not found.")


def delete_student(students):
    student_id = get_student_id()

    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            save_students(students)
            print("Student deleted successfully.")
            return

    print("Student not found.")


def main():
    students = load_students()

    while True:
        print("\n===== Student Record Management System =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                add_student(students)
            elif choice == "2":
                view_students(students)
            elif choice == "3":
                search_student(students)
            elif choice == "4":
                update_student(students)
            elif choice == "5":
                delete_student(students)
            elif choice == "6":
                print("Thank you for using the system!")
                break
            else:
                print("Invalid choice. Please choose 1-6.")
        except (OSError, csv.Error) as error:
            print(f"File operation error: {error}")
        except Exception as error:
            print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
