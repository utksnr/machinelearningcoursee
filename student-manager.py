import sys

DATA_FILE = "students.txt"

class StudentManager:
    def __init__(self):
        # Using a dictionary comprehension to load data
        self.students = self._load_records()

    def _load_records(self) -> dict:
        """Loads records from file using error handling and the walrus operator."""
        try:
            with open(DATA_FILE, "r") as f:
                # Efficiently parse lines: filter out empty lines and split by comma
                return {
                    parts[0]: float(parts[1]) 
                    for line in f 
                    if (parts := line.strip().split(",")) and len(parts) == 2
                }
        except FileNotFoundError:
            return {}
        except (ValueError, IndexError):
            print("Warning: Data file format is corrupted. Starting with empty records.")
            return {}

    def save_records(self):
        """Saves records to a text file."""
        try:
            with open(DATA_FILE, "w") as f:
                for name, marks in self.students.items():
                    f.write(f"{name},{marks}\n")
        except IOError as e:
            print(f"Failed to save data: {e}")

    @property
    def stats(self):
        """Calculates performance metrics on the fly using a Property."""
        if not self.students:
            return None
        marks = list(self.students.values())
        return {
            "avg": sum(marks) / len(marks),
            "max": max(marks),
            "min": min(marks)
        }

    def add_or_update(self):
        """Combines add and update logic."""
        name = input("Enter student name: ").strip()
        try:
            marks = float(input(f"Enter marks for {name}: "))
            self.students[name] = marks
            print(f"Record for {name} updated.")
        except ValueError:
            print("Error: Marks must be a numerical value.")

    def view_students(self):
        """Displays students sorted by marks descending."""
        if not self.students:
            return print("\nNo student records found.")

        print(f"\n{'Name':<20} | {'Marks':<10}")
        print("-" * 33)
        
        # Intermediate: Sorting dictionary items by value
        for name, marks in sorted(self.students.items(), key=lambda x: x[1], reverse=True):
            print(f"{name:<20} | {marks:<10.2f}")

        if s := self.stats:
            print("-" * 33)
            print(f"Avg: {s['avg']:.2f} | Max: {s['max']} | Min: {s['min']}")

    def search_student(self):
        """Searches for a student by name."""
        name = input("Enter name to search: ").strip()
        if (marks := self.students.get(name)) is not None:
            print(f"Found: {name} - {marks}")
        else:
            print("Student not found.")

    def delete_student(self):
        """Deletes a record using pop for efficiency."""
        name = input("Enter name to delete: ").strip()
        if self.students.pop(name, None) is not None:
            print(f"Deleted {name}.")
        else:
            print("Student not found.")

def main():
    manager = StudentManager()
    # Mapping choices to methods for a cleaner loop
    menu_map = {
        "1": manager.add_or_update,
        "2": manager.view_students,
        "3": manager.search_student,
        "4": manager.delete_student,
    }

    while True:
        print("\n--- Student Management System ---")
        print("1. Add/Update Student\n2. View Records\n3. Search\n4. Delete\n5. Save & Exit")
        
        choice = input("Select an option: ")

        if choice == "5":
            manager.save_records()
            print("Goodbye.")
            break
        
        # Execute the mapped function or show error
        action = menu_map.get(choice)
        if action:
            action()
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()