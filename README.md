# Student Management System

A command-line application to manage student records with full CRUD operations, JSON persistence, and input validation. Built with Python OOP principles.

---

## Features

- Add, update, delete, and list student records
- Fields: student ID, full name, grade (A–F)
- Unique ID validation — no duplicates allowed
- Data persisted to `students.json` automatically
- Formatted table output in the terminal
- Reloads records from file on every startup

---

## Project Structure

```
student_mgmt/
├── main.py        # CLI entry point and interactive menu
├── manager.py     # StudentManager class — CRUD + file I/O
├── student.py     # Student class — data model + validation
└── students.json  # Auto-created on first run
```

---

## Requirements

- Python 3.10 or higher (uses `dict[str, Student]` type hints)
- No third-party packages required

---

## Getting Started

```bash
# Clone or download the project, then run:
python3 main.py
```

On first run, `students.json` is created automatically in the same directory.

---

## Usage

The app presents a numbered menu:

```
════════════════════════════════════════════════════
  Student Management System
════════════════════════════════════════════════════
  Data file : students.json
  Records   : 3

────────────────────────────────────────────────────
  [1]  List all students
  [2]  Add student
  [3]  Update student
  [4]  Delete student
  [5]  View student
  [q]  Quit
────────────────────────────────────────────────────
  Choose:
```

### Add a student

```
  Student ID: S001
  Full name: Alice Johnson
  Grade (A / B / C / D / F)
  Grade: A

  ✓  Added: Alice Johnson (ID: S001, Grade: A)
```

### List all students

```
  ID           Name                      Grade
────────────────────────────────────────────────────
  S001         Alice Johnson             A
  S002         Bob Smith                 B
  S003         Carlos Rivera             C
────────────────────────────────────────────────────
  Total: 3 student(s)
```

### Update a student

Press Enter to keep the current value for any field.

### Delete a student

Prompts for confirmation (`yes` required) before deleting.

---

## Validation Rules

| Field | Rule |
|-------|------|
| Student ID | Required, must be unique |
| Name | Required, cannot be blank |
| Grade | Must be one of: A, B, C, D, F (case-insensitive) |

---

## Data Storage

Records are saved to `students.json` in the working directory after every write operation. Example:

```json
[
  { "id": "S001", "name": "Alice Johnson", "grade": "A" },
  { "id": "S002", "name": "Bob Smith",     "grade": "B" }
]
```

---

## Design Overview

### `Student` class (`student.py`)

- Constructor validates all three fields on creation
- `to_dict()` / `from_dict()` for JSON serialization
- Validation methods reused by `StudentManager` during updates

### `StudentManager` class (`manager.py`)

- Holds an in-memory `dict[id → Student]` for O(1) lookups
- `_load()` reads from JSON at startup; `_save()` writes after every mutation
- Raises `ValueError` for bad input — the CLI layer catches and displays these

### `main.py`

- Simple loop: print menu → read choice → call command function
- Each command handles its own prompts and output formatting
- `success()` / `error()` helpers for consistent feedback

---

## Extending the Project

Some ideas for next steps:

- **Search by name** — add a `search(query)` method to `StudentManager`
- **Grade filtering** — list only students with a given grade
- **CSV export** — write records to `.csv` using Python's `csv` module
- **GPA calculation** — add a numeric GPA field alongside letter grades
- **Sorting options** — sort by name or grade in addition to ID