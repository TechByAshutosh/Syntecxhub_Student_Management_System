import json
import os
from student import Student


class StudentManager:
    """Manages a collection of Student records with JSON persistence."""

    def __init__(self, filepath: str = "students.json"):
        self.filepath = filepath
        self._students: dict[str, Student] = {}
        self._load()

    # ── Persistence ────────────────────────────────────────────────────────────

    def _load(self):
        """Load students from JSON file (creates file if absent)."""
        if not os.path.exists(self.filepath):
            return
        try:
            with open(self.filepath, "r") as f:
                records = json.load(f)
            for record in records:
                s = Student.from_dict(record)
                self._students[s.student_id] = s
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"  [warning] Could not load data: {e}")

    def _save(self):
        """Persist current student records to JSON file."""
        with open(self.filepath, "w") as f:
            json.dump([s.to_dict() for s in self._students.values()], f, indent=2)

    # ── CRUD Operations ────────────────────────────────────────────────────────

    def add(self, student_id: str, name: str, grade: str, reg_no: str, semester: int) -> Student:
        """Add a new student. Raises ValueError on duplicate ID."""
        student_id = student_id.strip()
        if student_id in self._students:
            raise ValueError(f"Student ID '{student_id}' already exists.")
        student = Student(student_id, name, grade, reg_no, semester)
        self._students[student.student_id] = student
        self._save()
        return student

    def update(self, student_id: str, name: str = None, grade: str = None,
               reg_no: str = None, semester: int = None) -> Student:
        """Update fields for an existing student."""
        student = self._get_or_raise(student_id)
        if name is not None:
            student.name = student._validate_name(name)
        if grade is not None:
            student.grade = student._validate_grade(grade)
        if reg_no is not None:
            student.reg_no = student._validate_reg_no(reg_no)
        if semester is not None:
            student.semester = student._validate_semester(semester)
        self._save()
        return student

    def delete(self, student_id: str) -> Student:
        """Remove a student by ID. Returns the deleted student."""
        student = self._get_or_raise(student_id)
        del self._students[student_id.strip()]
        self._save()
        return student

    def get(self, student_id: str) -> Student:
        """Retrieve a single student by ID."""
        return self._get_or_raise(student_id)

    def list_all(self) -> list[Student]:
        """Return all students sorted by ID."""
        return sorted(self._students.values(), key=lambda s: s.student_id)

    def count(self) -> int:
        return len(self._students)

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _get_or_raise(self, student_id: str) -> Student:
        student_id = student_id.strip()
        if student_id not in self._students:
            raise ValueError(f"No student found with ID '{student_id}'.")
        return self._students[student_id]