import request_parser
from database import DataBase
import unittest
import os


class RequestParserTester(unittest.TestCase):
    """ Класс-тестировщик модуля request_parser """

    @staticmethod
    def create_bd():
        db = DataBase("./testdatabase.db")
        db.create_table_geo()
        data = [(1, 60.1, 50.1, "London", "Big", 123, None),
                (2, 60.2, 50.2, "Berlin", "Small", 8, 9874),
                (3, 60.3, 50.3, "Paris", "Large", 42, 3141),
                (4, 60.4, 50.4, "Dresden", "Medium", 0, 33)]
        db.add_data_to_table(data, "geo")
        return db

    def test_check_city(self):
        db = self.create_bd()
        self.assertEqual(request_parser.check_city(db, "Paris"), "Paris")
        self.assertEqual(request_parser.check_city(db, "london"), "London")
        self.assertIsNone(request_parser.check_city(db, "Magnitogorsk"))
        db.close()
        os.remove("./testdatabase.db")

    def test_check_street(self):
        db = self.create_bd()
        self.assertEqual(request_parser.check_street(db, "Small"), "Small")
        self.assertEqual(request_parser.check_street(db, "large"), "Large")
        self.assertIsNone(request_parser.check_street(db, "little"))
        db.close()
        os.remove("./testdatabase.db")

    def test_parse_question(self):
        db = self.create_bd()
        self.assertEqual(request_parser.parse_question("London Big 123", db),
                         ("London", "Big", "123"))
        self.assertEqual(request_parser.parse_question("berlin small", db),
                         ("Berlin", "Small", None))
        self.assertEqual(request_parser.parse_question("Large 42", db),
                         (None, "Large", "42"))
        self.assertEqual(request_parser.parse_question("Dresden", db),
                         "Все плохо! Мало данных!")
        db.close()
        os.remove("./testdatabase.db")


if __name__ == '__main__':
    unittest.main()
