#!/usr/bin/env python3
"""
Student Management System
--------------------------
CLI for managing student records (add / update / delete / list).
Data is persisted to students.json in the current directory.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from manager import StudentManager

# ── Display helpers ────────────────────────────────────────────────────────────

WIDTH = 52

def hr(char="─"):
    print(char * WIDTH)

def header(title: str):
    print()
    hr("═")
    print(f"  {title}")
    hr("═")

def print_student_table(students):
    if not students:
        print("  (no records found)")
        return
    print(f"  {'ID':<10} {'Reg No':<14} {'Name':<22} {'Sem':<5} {'Grade':<5}")
    hr()
    for s in students:
        print(f"  {s.student_id:<10} {s.reg_no:<14} {s.name:<22} {s.semester:<5} {s.grade:<5}")
    hr()
    print(f"  Total: {len(students)} student(s)")

def success(msg): print(f"\n  ✓  {msg}")
def error(msg):   print(f"\n  ✗  {msg}")
def prompt(label, required=True):
    while True:
        val = input(f"  {label}: ").strip()
        if val or not required:
            return val
        print("    (this field is required)")

# ── Menu actions ───────────────────────────────────────────────────────────────

def cmd_list(mgr: StudentManager):
    header("All Students")
    print_student_table(mgr.list_all())

def cmd_add(mgr: StudentManager):
    header("Add Student")
    student_id = prompt("Student ID")
    name       = prompt("Full name")
    reg_no     = prompt("Reg No")
    semester   = prompt("Semester (1–8)")
    print(f"  Grade (A / B / C / D / F)")
    grade = prompt("Grade")
    try:
        s = mgr.add(student_id, name, grade, reg_no, int(semester))
        success(f"Added: {s.name} (ID: {s.student_id}, Reg: {s.reg_no}, Sem: {s.semester}, Grade: {s.grade})")
    except (ValueError, TypeError) as e:
        error(e)

def cmd_update(mgr: StudentManager):
    header("Update Student")
    student_id = prompt("Student ID to update")
    try:
        s = mgr.get(student_id)
        print(f"  Current → Name: {s.name}  Reg: {s.reg_no}  Semester: {s.semester}  Grade: {s.grade}")
        print("  (press Enter to keep current value)")
        new_name     = prompt("New name    ", required=False) or None
        new_reg_no   = prompt("New reg no  ", required=False) or None
        new_semester = prompt("New semester", required=False) or None
        new_grade    = prompt("New grade   ", required=False) or None
        if all(v is None for v in [new_name, new_reg_no, new_semester, new_grade]):
            print("\n  No changes made.")
            return
        s = mgr.update(
            student_id,
            name=new_name,
            grade=new_grade,
            reg_no=new_reg_no,
            semester=int(new_semester) if new_semester else None,
        )
        success(f"Updated: {s.name} (ID: {s.student_id}, Reg: {s.reg_no}, Sem: {s.semester}, Grade: {s.grade})")
    except (ValueError, TypeError) as e:
        error(e)

def cmd_delete(mgr: StudentManager):
    header("Delete Student")
    student_id = prompt("Student ID to delete")
    confirm = input(f"  Are you sure? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("\n  Cancelled.")
        return
    try:
        s = mgr.delete(student_id)
        success(f"Deleted: {s.name} (ID: {s.student_id})")
    except ValueError as e:
        error(e)

def cmd_view(mgr: StudentManager):
    header("View Student")
    student_id = prompt("Student ID")
    try:
        s = mgr.get(student_id)
        print()
        print(f"  ID       : {s.student_id}")
        print(f"  Name     : {s.name}")
        print(f"  Reg No   : {s.reg_no}")
        print(f"  Semester : {s.semester}")
        print(f"  Grade    : {s.grade}")
    except ValueError as e:
        error(e)

# ── Main loop ──────────────────────────────────────────────────────────────────

MENU = [
    ("1", "List all students",  cmd_list),
    ("2", "Add student",        cmd_add),
    ("3", "Update student",     cmd_update),
    ("4", "Delete student",     cmd_delete),
    ("5", "View student",       cmd_view),
    ("q", "Quit",               None),
]

def main():
    mgr = StudentManager("students.json")
    print()
    hr("═")
    print("  Student Management System")
    hr("═")
    print(f"  Data file : students.json")
    print(f"  Records   : {mgr.count()}")

    while True:
        print()
        hr()
        for key, label, _ in MENU:
            print(f"  [{key}]  {label}")
        hr()
        choice = input("  Choose: ").strip().lower()

        if choice == "q":
            print("\n  Goodbye!\n")
            break

        action = next((fn for k, _, fn in MENU if k == choice and fn), None)
        if action:
            action(mgr)
        else:
            error("Invalid choice. Try again.")

if __name__ == "__main__":
    main()