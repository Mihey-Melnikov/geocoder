import sqlite3


class DataBase:
    """ Класс отвечающий за базу данных """

    def __init__(self):
        """ Инициализация и создание базы данных """

        self.conn = sqlite3.connect(r"data/geodatabase.db",
                                    check_same_thread=False)
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

    def delete_table_nodes(self):
        """ Удаление временной таблицы точек """

        self.cursor.execute("DROP TABLE IF EXISTS nodes")
        self.conn.commit()

    def delete_table_ways(self):
        """ Удаление временной таблицы путей """

        self.cursor.execute("DROP TABLE IF EXISTS ways")
        self.conn.commit()

    def delete_table_geo(self):
        """ Удаление временной таблицы путей """

        self.cursor.execute("DROP TABLE IF EXISTS geo")
        self.conn.commit()

    def add_data_to_geo(self, data):
        """ Добавление данных в таблицу geo """

        self.cursor.executemany(
            "INSERT OR REPLACE INTO geo VALUES(?, ?, ?, ?, ?, ?, ?)", data)
        self.conn.commit()

    def add_nodes(self, nodes):
        """ Добавление точек в таблицу nodes """

        self.cursor.executemany(
            "INSERT OR REPLACE INTO nodes VALUES(?, ?, ?, ?)", nodes)
        self.conn.commit()

    def add_ways(self, ways):
        """ Добавление путей в таблицу ways """

        self.cursor.executemany(
            "INSERT OR REPLACE INTO ways VALUES(?, ?, ?)", ways)
        self.conn.commit()

    def get_nodes_with_tags(self):
        """ Возвращает точки, у которых есть теги """

        self.cursor.execute("SELECT * FROM nodes WHERE tags IS NOT NULL")
        return self.cursor.fetchall()

    def get_ways(self):
        """ Возвращает пути, у которых есть теги """

        self.cursor.execute("SELECT * FROM ways WHERE tags IS NOT NULL")
        return self.cursor.fetchall()

    def get_coords_by_id(self, ids):
        """ Возвращает координаты по данным id """

        sql = "SELECT lat, lon FROM nodes WHERE id=?"
        coords = []
        for id in ids:
            self.cursor.execute(sql, [id])
            coords.append(self.cursor.fetchone())
        return coords

    def get_rows_by_street(self, street):
        """ Возвращает возможные варианты по улице """

        sql = f"SELECT * FROM geo WHERE street LIKE '%{street}%'"
        self.cursor.execute(sql)
        return list(self.cursor.fetchall())

    def get_rows_by_city(self, city):
        """ Возвращает возможные варианты по улице """

        sql = f"SELECT * FROM geo WHERE city LIKE '%{city}%'"
        self.cursor.execute(sql)
        return list(self.cursor.fetchall())

    def get_rows_by_postcode(self, postcode):
        """ Возвращает возможные варианты по улице """

        sql = f"SELECT * FROM geo WHERE postcode LIKE '%{postcode}%'"
        self.cursor.execute(sql)
        return list(self.cursor.fetchall())

    def get_rows_by_coord(self, lat, lon):
        """ Возвращает возможные варианты по улице """

        sql = f"SELECT * FROM geo WHERE lat LIKE '%{lat}%' AND lon LIKE '%{lon}%'"
        self.cursor.execute(sql)
        return list(self.cursor.fetchall())

    def get_cities_from_geo(self):
        """ Возвращает список городов всех """

        sql = "SELECT city FROM geo"
        self.cursor.execute(sql)
        return list(self.cursor.fetchall())

    def get_streets_from_geo(self):
        """ Возвращает улицы из таблицы geo """
        sql = "SELECT street FROM geo"
        self.cursor.execute(sql)
        return list(self.cursor.fetchall())

    def get_streets_by_city_in_geo(self, city):
        """ Возвращает все улицы города """

        sql = f"SELECT street FROM geo WHERE city=?"
        self.cursor.execute(sql, [city])
        return list(self.cursor.fetchall())

    def add_data_to_cities(self, city, streets):
        """ Заполняет вспомогательную таблицу улиц по городу """

        self.cursor.execute(
            f"""INSERT INTO cities (city, streets) VALUES ("{city}", "{streets}")""")
        self.conn.commit()

    def get_streets_by_city_in_cities(self, city):
        """ Возвращает все улицы города быстрее """

        sql = f"SELECT streets FROM cities WHERE city=?"
        self.cursor.execute(sql, [city])
        return list(self.cursor.fetchall())

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

    def get_cities_count(self):
        """ Возвращает количество городов """

        sql = "SELECT count(city) FROM cities"
        self.cursor.execute(sql)
        return self.cursor.fetchone()
