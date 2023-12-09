import csv
import logging
import os


class InvalidSubjectError(ValueError):
    pass


class InvalidValue(ValueError):
    pass


class InvalidAttribute(ValueError):
    pass


logging.basicConfig(level=logging.DEBUG, filename='project.log.', filemode='w',
                    encoding='utf-8')


class Student:
    subjects_dict = {}

    def __init__(self, name, subjects_file):
        '''Конструктор класса. Принимает имя студента и файл с
        предметами и их результатами. Инициализирует атрибуты
        name и subjects и вызывает метод load_subjects для
        загрузки предметов из файла.'''
        self.name = name
        self.subjects_file = subjects_file
        self.subjects = self.load_subjects(self.subjects_file)
        for i in self.subjects:
            if i not in self.subjects_dict:
                self.subjects_dict[i] = {"grades": [], "test_score": []}
        logging.debug(msg=f"Создание экземпляра класса 'Student'\
c атрибутами name='{name}', subjects_file='{subjects_file}'")

    def __setattr__(self, attrname, value):
        logging.debug(
            msg=f"Проверяет корректность значения атрибута {attrname}"
                      )
        if attrname == 'name':
            if isinstance(value, str) and value[0].isupper():
                self.__dict__[attrname] = value
            else:
                logging.error(
                    msg=f"Некорректное значение атрибута '{attrname}'"
                              )
                raise InvalidAttribute(
                    f"Некорректное значение атрибута '{attrname}'"
                                       )
        if attrname == "subjects_file":
            if value in os.listdir(os.getcwd()):
                self.__dict__[attrname] = value
            else:
                logging.error(
                    msg=f"Некорректное значение атрибута '{attrname}'"
                              )
                raise InvalidAttribute("Файл не найден")
        else:
            # для остальных атрибутов, просто
            # присваиваем новое значение
            self.__dict__[attrname] = value

    def __str__(self):
        '''Возвращает строковое представление студента,
        включая имя и список предметов.'''
        res = []
        for k, v in self.subjects_dict.items():
            if len(v["grades"]) > 0 or len(v["test_score"]) > 0:
                res.append(k)
        return f"Студент: {self.name}\nПредметы: {', '.join(res)}"

    def load_subjects(self, subjects_file):
        '''Загружает предметы из файла CSV. Использует модуль
        csv для чтения данных из файла и добавляет предметы
        в атрибут subjects.'''
        logging.debug(msg=f"Загружает предметы из файла CSV \
c атрибутом subjects_file='{subjects_file}'")
        subjects_list = None
        with open(subjects_file, 'r', newline='', encoding="utf-8") as f:
            for i in csv.reader(f):
                subjects_list = i
            return subjects_list

    def add_grade(self, subject, grade):
        '''Добавляет оценку по заданному предмету.
        Убеждается, что оценка является целым числом от 2 до 5.'''
        logging.debug(msg=f"Добавляет оценку {grade} к предмету {subject}")
        try:
            if isinstance(grade, int) and 1 < grade < 6:
                self.subjects_dict[subject]["grades"].append(grade)
        except Exception as e:
            logging.error(msg=f"Предмет {e} не найден")
            raise InvalidSubjectError(f"Предмет {e} не найден")

    def add_test_score(self, subject, test_score):
        '''Добавляет результат теста по заданному предмету.
        Убеждается, что результат теста является целым числом от 0 до 100.'''
        logging.debug(msg=f"Добавляет результат теста {test_score} \
к предмету {subject}")
        try:
            if isinstance(test_score, int) and 0 <= test_score <= 100:
                self.subjects_dict[subject]["test_score"].append(test_score)
            else:
                logging.error(msg=f"Некорректные данные атрибута {test_score}")
        except Exception as e:
            logging.error(msg=f"Предмет {e} не найден")
            raise InvalidSubjectError(f"Предмет {e} не найден")

    def get_average_test_score(self, subject):
        '''Возвращает средний балл по тестам для заданного предмета.'''
        logging.debug(msg=f"Возвращает средний балл по тестам для {subject}")
        try:
            res = self.subjects_dict[subject]["test_score"]
            if len(res) > 0:
                return sum(res)/len(res)
            else:
                return 0
        except Exception as e:
            logging.error(msg=f"Предмет {e} не найден")
            raise InvalidSubjectError(f"Предмет {e} не найден")

    def get_average_grade(self):
        '''Возвращает средний балл по всем предметам.'''
        logging.debug(msg="Возвращает средний балл по всем предметам")
        sum_grades = 0
        len_grades = 0
        for key in self.subjects_dict:
            sum_grades += sum(self.subjects_dict[key]["grades"])
            len_grades += len(self.subjects_dict[key]["grades"])
        if len_grades > 0:
            return sum_grades/len_grades
        else:
            return 0


if __name__ == "__main__":
    student = Student("Т", "subjects.csv")
    student.add_grade("Математика", 4)
    student.add_test_score("Математика", 101)

    student.add_grade("История", 5)
    student.add_test_score("История", 92)

    average_grade = student.get_average_grade()
    print(f"Средний балл: {average_grade}")

    average_test_score = student.get_average_test_score("Математика")
    print(f"Средний результат по тестам по математике: {average_test_score}")

    print(student)

    student = Student("Сидоров Сидор", "subjects.csv")
    average_history_score = student.get_average_test_score("Биология")
