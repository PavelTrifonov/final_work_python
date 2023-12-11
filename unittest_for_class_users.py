from homework12 import Student as St

import unittest


class TestCaseName(unittest.TestCase):
    def setUp(self):
        self.student = St("Т", "subjects.csv")
        self.student.add_grade("Математика", 4)
        self.student.add_test_score("Математика", 87)
        self.student.add_test_score("Математика", 95)
        self.student.add_grade("История", 5)
        self.average_grade = self.student.get_average_grade()
        self.average_test_score = self.student.get_average_test_score("Математика")

    def test_average_grade(self):
        self.assertEqual(self.average_grade, 4.5, msg='Неверный подсчет \
средней оценки по предметам')

    def test_average_test_score(self):
        self.assertEqual(self.average_test_score, 91, msg='Неверный подсчет \
среднего балла по Математике')

    def test_subjects_dict(self):
        self.assertEqual(St.load_subjects(self, "subjects.csv"),
                         ["Математика", "Физика", "История", "Литература"],
                         msg='Неверный подсчет среднего балла по Математике')


if __name__ == '__main__':
    unittest.main()
