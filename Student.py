# Взять класс студент из дз 12-го семинара, добавить запуск из командной строки(передача в качестве 
# аргумента название csv-файла с предметами), логирование и написать 3-5 тестов с использованием pytest.

import logging
import csv
import argparse

logging.basicConfig(filename='Student.log',
                    encoding='utf-8',
                    level=logging.DEBUG)

class Student:

    def __init__(self, name, subjects_file):
        self.name = name
        self.subjects = {}
        self.load_subjects(subjects_file)
        logging.debug(f"Создан экземпляр класса Student с параметрами: "
                      f"{name}, {subjects_file}")

    def __setattr__(self, name, value):
        if name == 'name':
            if not value.replace(' ', '').isalpha() or not value.istitle():
                raise ValueError("ФИО должно состоять только из букв и"
                                 "начинаться с заглавной буквы")
        super().__setattr__(name, value)

    def __getattr__(self, name):
        if name in self.subjects:
            return self.subjects[name]
        else:
            raise AttributeError(f"Предмет {name} не найден")

    def __str__(self):
        return f"Студент: {self.name}\nПредметы: {', '.join(self.subjects.keys())}"

    def load_subjects(self, subjects_file):
        with open(subjects_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                for subject in row:
                    if subject not in self.subjects:
                        self.subjects[subject] = {'grades': [], 'test_scores': []}

    def add_grade(self, subject, grade):
        if subject not in self.subjects:
            raise ValueError(f"Предмет {subject} не найден")
        if not isinstance(grade, int) or grade < 2 or grade > 5:
            raise ValueError("Оценка должна быть целым числом от 2 до 5")
        self.subjects[subject]['grades'].append(grade)
        logging.debug(f"У {self.name} к предмету {subject} добавлена оценка: "
                      f"{grade}")

    def add_test_score(self, subject, test_score):
        if subject not in self.subjects:
            raise ValueError(f"Предмет {subject} не найден")
        if (not isinstance(test_score, int) or
                test_score < 0 or test_score > 100):
            raise ValueError("Результат теста должен быть целым числом"
                             "от 0 до 100")
        self.subjects[subject]['test_scores'].append(test_score)
        logging.debug(f"У {self.name} к предмету {subject} добавлен результат "
                      f"теста: {test_score}")

    def get_average_test_score(self, subject):
        if subject not in self.subjects:
            raise ValueError(f"Предмет {subject} не найден")
        test_scores = self.subjects[subject]['test_scores']
        if len(test_scores) == 0:
            logging.debug(f"Для {self.name} запрошен средний бал тестов по "
                          f"предмету {subject}: результатов тестов не найдено")
            return 0
        res = sum(test_scores) / len(test_scores)
        logging.debug(f"Для {self.name} запрошен средний бал тестов по "
                      f"предмету {subject}: {res}")
        return res

    def get_average_grade(self):
        total_grades = []
        for subject in self.subjects:
            grades = self.subjects[subject]['grades']
            if len(grades) > 0:
                total_grades.extend(grades)
        if len(total_grades) == 0:
            logging.debug(f"Для {self.name} запрошена средняя оценка "
                          f"по предметам: оценок не найдено")
            return 0
        res = sum(total_grades) / len(total_grades)
        logging.debug(f"Для {self.name} запрошена средняя оценка "
                      f"по предметам: {res}")
        return res

def cl_parser():
    parser = argparse.ArgumentParser(description="Student's marks")
    parser.add_argument('-name', type=str, default='Инкогнито')
    parser.add_argument('file')

    args = parser.parse_args()
    print(args.name, args.file)
    student = Student(args.name, args.file)
    return student


if __name__ == "__main__":
    cl_parser()  # python .\Student.py -name="Иван Иванов"  subjects.csv

    student = Student("Иван Иванов", "subjects.csv")
    student.add_grade("Математика", 4)
    student.add_test_score("Математика", 85)
    student.add_grade("Математика", 5)
    student.add_test_score("История", 92)
    average_grade = student.get_average_grade()
    print(f"Средний балл: {average_grade}")
    average_test_score = student.get_average_test_score("Математика")
    print(f"Средний результат по тестам по математике: {average_test_score}")
    print(student)