import unittest
from database import DataBase
import os
import sqlite3


class DBTester(unittest.TestCase):
    """ Класс-тестировщик модуля database """

    # def __init__(self):
    #     super().__init__()
    #     self.db = DataBase("./testdatabase.db")

    def test_init(self):
        db = DataBase("./testdatabase.db")
        self.assertTrue(os.path.exists("./testdatabase.db"))
        self.assertIsNotNone(db.conn)
        self.assertIsNotNone(db.cursor)
        db.close()
        os.remove("./testdatabase.db")

    def test_close(self):
        db = DataBase("./testdatabase.db")
        db.close()
        with self.assertRaises(sqlite3.ProgrammingError):
            db.conn.cursor()
        with self.assertRaises(sqlite3.ProgrammingError):
            db.cursor.execute("""CREATE TABLE test (id int, test text)""")
        os.remove("./testdatabase.db")

    def test_create_table(self):
        db = DataBase("./testdatabase.db")
        db.create_table_geo()
        self.assertEqual(self.find_table(db, "geo")[0], "geo")
        db.create_temp_table_ways()
        self.assertEqual(self.find_table(db, "ways")[0], "ways")
        db.create_temp_table_nodes()
        self.assertEqual(self.find_table(db, "nodes")[0], "nodes")
        db.create_subtable_cities()
        self.assertEqual(self.find_table(db, "cities")[0], "cities")
        self.assertIsNone(self.find_table(db, "notExist"))
        db.close()
        os.remove("./testdatabase.db")

    @staticmethod
    def find_table(db, table):
        db.cursor.execute(
            f"SELECT name FROM sqlite_master WHERE "
            f"type='table' AND name='{table}'")
        return db.cursor.fetchone()

    def test_delete(self):
        db = DataBase("./testdatabase.db")
        db.create_table_geo()
        db.delete_table("geo")
        self.assertIsNone(self.find_table(db, "geo"))
        db.close()
        os.remove("./testdatabase.db")

    def test_add(self):
        db = DataBase("./testdatabase.db")
        db.create_table_geo()
        with self.assertRaises(sqlite3.OperationalError):
            db.add_data_to_table([(1, 2, 3)], "notExistTable")
        with self.assertRaises(sqlite3.OperationalError):
            db.add_data_to_table([(1, 2, 3)], "geo")

        db.add_data_to_table([(1, 60.1, 50.1, "Ekb", "Mat", "Mex", 123456)],
                             "geo")
        db.cursor.execute("SELECT * FROM geo")
        self.assertEqual(db.cursor.fetchone(),
                         (1, 60.1, 50.1, "Ekb", "Mat", "Mex", 123456))
        db.close()
        os.remove("./testdatabase.db")

    def test_get_with_tags(self):
        db = DataBase("./testdatabase.db")
        db.create_temp_table_nodes()
        db.add_data_to_table([(1, 50.1, 60.1, "tag1;tag2"),
                              (2, 50.2, 60.2, None)],
                             "nodes")
        self.assertEqual(db.get_data_with_tags_from_table("nodes"),
                         [(1, 50.1, 60.1, "tag1;tag2")])
        db.close()
        os.remove("./testdatabase.db")

    def test_get_coords(self):
        db = DataBase("./testdatabase.db")
        db.create_temp_table_nodes()
        db.add_data_to_table([(1, 50.1, 60.1, "tag1;tag2"),
                              (2, 50.2, 60.2, None),
                              (3, 50.3, 60.3, "tag3")], "nodes")
        self.assertEqual(db.get_coords_by_id([1, 3]),
                         [(50.1, 60.1), (50.3, 60.3)])
        db.close()
        os.remove("./testdatabase.db")

    def test_get_data(self):
        db = DataBase("./testdatabase.db")
        db.create_table_geo()
        db.add_data_to_table([(1, 60.1, 50.1, "Ekb", "Mat", "Mex", 123456)],
                             "geo")
        with self.assertRaises(sqlite3.OperationalError):
            self.assertTrue(db.get_data_from_table("street", "notExists"))
        with self.assertRaises(sqlite3.OperationalError):
            self.assertTrue(db.get_data_from_table("something", "geo"))
        self.assertEqual(db.get_data_from_table("street", "geo"), [("Mat",)])
        db.close()
        os.remove("./testdatabase.db")

    def test_get_streets(self):
        db = DataBase("./testdatabase.db")
        db.create_table_geo()
        db.add_data_to_table(
            [(1, 60.1, 50.1, "Ekb", "Mat", "Mex", 123456),
             (2, 60.2, 50.2, "Mgn", "MGTU", "FIIT", None),
             (3, 60.3, 50.3, "Ekb", "Love", "Python", 654321)],
            "geo")
        self.assertEqual(db.get_streets_by_city_in_geo("notExists"), [])
        self.assertEqual(db.get_streets_by_city_in_geo("Ekb"), [("Mat",), ("Love",)])
        db.close()
        os.remove("./testdatabase.db")

    def test_add_to_cities(self):
        db = DataBase("./testdatabase.db")
        db.create_subtable_cities()
        db.add_data_to_cities("Mat", "Mex")
        db.cursor.execute("SELECT * FROM cities")
        self.assertEqual(db.cursor.fetchone(), (1, "Mat", "Mex"))
        db.close()
        os.remove("./testdatabase.db")

    def test_get_rows_by(self):
        db = DataBase("./testdatabase.db")
        db.create_table_geo()
        db.add_data_to_table(
            [(1, 60.1, 50.1, "Ekb", "Mat", "Mex", 123456),
             (2, 60.2, 50.2, "Mgn", "MGTU", "FIIT", None),
             (3, 60.3, 50.3, "Ekb", "Love", "Python", 654321)],
            "geo")
        self.assertEqual(db.get_rows_by(), "Неккоректно написан адрес!")
        self.assertEqual(db.get_rows_by("Ekb"), "Неккоректно написан адрес!")
        self.assertEqual(db.get_rows_by(city="notExists", street="notExists",
                                        housenumber="notExists"), [])
        db.close()
        os.remove("./testdatabase.db")

    def test_get_data_count(self):
        db = DataBase("./testdatabase.db")
        db.create_table_geo()
        db.add_data_to_table(
            [(1, 60.1, 50.1, "Ekb", "Mat", "Mex", 123456),
             (2, 60.2, 50.2, "Mgn", "MGTU", "FIIT", None),
             (3, 60.3, 50.3, "Ekb", "Love", "Python", 654321)],
            "geo")
        with self.assertRaises(sqlite3.OperationalError):
            db.get_data_count("notExists", "geo")
        with self.assertRaises(sqlite3.OperationalError):
            db.get_data_count("street", "notExists")
        self.assertEqual(db.get_data_count("city", "geo"), (2,))
        self.assertEqual(db.get_data_count("id", "geo"), (3,))
        self.assertEqual(db.get_data_count("postcode", "geo"), (2,))
        self.assertEqual(db.get_data_count("lat", "geo"), (3,))
        db.close()
        os.remove("./testdatabase.db")


if __name__ == '__main__':
    unittest.main()
