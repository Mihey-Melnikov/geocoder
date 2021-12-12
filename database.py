import sqlite3


class DataBase:
    """ Класс отвечающий за базу данных """

    def __init__(self, path=r"data/geodatabase.db"):
        """ Инициализация и создание базы данных """

        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def close(self):
        """ Разрывает соединение с базой """

        if self.cursor is not None:
            self.cursor.close()

        if self.conn is not None:
            self.conn.close()

    def create_table_geo(self):
        """ Создание таблицы с геоданными """

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS geo
                          (id int primary key, lat real, lon real,
                          city text default null,
                          street text default null,
                          housenumber text default null,
                          postcode int default null)""")
        self.conn.commit()

    def create_temp_table_nodes(self):
        """ Создание временной таблицы точек """

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS nodes
                          (id int primary key,
                          lat real, lon real, tags text)""")
        self.conn.commit()

    def create_temp_table_ways(self):
        """ Создание временной таблицы путей """

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS ways
                          (id int primary key, nodes text, tags text)""")
        self.conn.commit()

    def create_subtable_cities(self):
        """ Создание вспомогательной таблицы городов """

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS cities
                                  (id integer primary key autoincrement,
                                  city text, streets text)""")
        self.conn.commit()

    def delete_table(self, table):
        """ Удаление таблицы """

        self.cursor.execute(f"DROP TABLE IF EXISTS {table}")
        self.conn.commit()

    def add_data_to_table(self, data, table):
        """ Добавление данных в таблицу """

        data_count = len(data[0])
        sql = f"""INSERT OR REPLACE INTO {table} VALUES({"?, " * (data_count - 1)}?)"""
        self.cursor.executemany(sql, data)
        self.conn.commit()

    def get_data_with_tags_from_table(self, table):
        """ Возвращает данные из таблиц, у которых есть теги """

        self.cursor.execute(f"SELECT * FROM {table} WHERE tags IS NOT NULL")
        return self.cursor.fetchall()

    def get_coords_by_id(self, ids):
        """ Возвращает координаты по данным id """

        sql = "SELECT lat, lon FROM nodes WHERE id=?"
        coords = []
        for id in ids:
            self.cursor.execute(sql, [id])
            coords.append(self.cursor.fetchone())
        return coords

    def get_data_from_table(self, data, table):
        """ Возвращает данные из таблицы """

        self.cursor.execute(f"SELECT {data} FROM {table}")
        return list(self.cursor.fetchall())

    def get_streets_by_city_in_geo(self, city):
        """ Возвращает все улицы города """

        sql = f"SELECT DISTINCT street FROM geo WHERE city=?"
        self.cursor.execute(sql, [city])
        return list(self.cursor.fetchall())

    def add_data_to_cities(self, city, streets):
        """ Заполняет вспомогательную таблицу улиц по городу """

        self.cursor.execute(
            f"""INSERT INTO cities (city, streets) VALUES ("{city}", "{streets}")""")
        self.conn.commit()

    def get_rows_by(self, city=None, street=None, housenumber=None):
        """ Возвращает возможные варианты адресов """

        if city and street and housenumber:
            sql = f"SELECT * FROM geo WHERE " \
                  f"city LIKE '%{city}%' AND " \
                  f"street LIKE '%{street}%' AND " \
                  f"housenumber LIKE '%{housenumber}%'"
        elif street and housenumber:
            sql = f"SELECT * FROM geo WHERE " \
                  f"street LIKE '%{street}%' AND " \
                  f"housenumber LIKE '%{housenumber}%'"
        elif city and street:
            sql = f"SELECT * FROM geo WHERE " \
                  f"city LIKE '%{city}%' AND " \
                  f"street LIKE '%{street}%'"
        else:
            return "Неккоректно написан адрес!"
        self.cursor.execute(sql)
        return list(self.cursor.fetchall())

    def get_data_count(self, data, table):
        """ Возвращает количество уникальных данных в таблице """

        self.cursor.execute(f"SELECT COUNT(DISTINCT {data}) FROM {table}")
        return self.cursor.fetchone()
