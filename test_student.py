from Student import Student
import pytest


@pytest.fixture
def student_1():
    return Student("Иван Иванов", "subjects.csv")


def test_subject(student_1):
    with pytest.raises(ValueError):
        student_1.add_grade("Биология", 4)


def test_name():
    with pytest.raises(ValueError):
        Student("Петр 852", "subjects.csv")


def test_add_grade(student_1):
    with pytest.raises(ValueError):
        student_1.add_grade("Математика", 6)


def test_test_score(student_1):
    with pytest.raises(ValueError):
        student_1.add_test_score("История", 105)


def test_average_test_score(student_1):
    student_1.add_test_score("Физика", 60)
    student_1.add_test_score("Физика", 80)
    assert student_1.get_average_test_score("Физика") == 70.0


def test_average_grade(student_1):
    student_1.add_grade("Математика", 4)
    student_1.add_grade("История", 5)
    assert student_1.get_average_grade() == 4.5