class Student:
    """Represents a single student record."""

    VALID_GRADES = {"A", "B", "C", "D", "F"}
    MIN_SEMESTER = 1
    MAX_SEMESTER = 8

    def __init__(self, student_id: str, name: str, grade: str, reg_no: str, semester: int):
        self.student_id = self._validate_id(student_id)
        self.name = self._validate_name(name)
        self.grade = self._validate_grade(grade)
        self.reg_no = self._validate_reg_no(reg_no)
        self.semester = self._validate_semester(semester)

    def _validate_id(self, student_id: str) -> str:
        student_id = str(student_id).strip()
        if not student_id:
            raise ValueError("Student ID cannot be empty.")
        return student_id

    def _validate_name(self, name: str) -> str:
        name = name.strip()
        if not name:
            raise ValueError("Student name cannot be empty.")
        return name

    def _validate_grade(self, grade: str) -> str:
        grade = grade.strip().upper()
        if grade not in self.VALID_GRADES:
            raise ValueError(
                f"Invalid grade '{grade}'. Must be one of: {', '.join(sorted(self.VALID_GRADES))}"
            )
        return grade

    def _validate_reg_no(self, reg_no: str) -> str:
        reg_no = str(reg_no).strip()
        if not reg_no:
            raise ValueError("Registration number cannot be empty.")
        return reg_no

    def _validate_semester(self, semester) -> int:
        try:
            semester = int(semester)
        except (ValueError, TypeError):
            raise ValueError("Semester must be a whole number.")
        if not (self.MIN_SEMESTER <= semester <= self.MAX_SEMESTER):
            raise ValueError(
                f"Semester must be between {self.MIN_SEMESTER} and {self.MAX_SEMESTER}."
            )
        return semester

    def to_dict(self) -> dict:
        return {
            "id": self.student_id,
            "name": self.name,
            "grade": self.grade,
            "reg_no": self.reg_no,
            "semester": self.semester,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        return cls(data["id"], data["name"], data["grade"], data["reg_no"], data["semester"])

    def __repr__(self) -> str:
        return (
            f"Student(id={self.student_id!r}, name={self.name!r}, "
            f"grade={self.grade!r}, reg_no={self.reg_no!r}, semester={self.semester})"
        )