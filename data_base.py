import sqlite3


class DataBase:
    """ Класс отвечающий за базу данных """

    def __init__(self):
        """ Инициализация и создание базы данных """
        self.conn = sqlite3.connect(r"data/geodatabase.db")
        self.cursor = self.conn.cursor()

    def create_table_geo(self):
        """ Создание таблицы с геоданными """
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS geo
                          (id int primary key, lat real, lon real, 
                          city text default null, street text default null, 
                          housenumber text default null, postcode int default null)""")
        self.conn.commit()

    def create_table_nodes(self):
        """ Создание временной таблицы точек """
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS nodes
                          (id int primary key, lat real, lon real, tags text)""")
        self.conn.commit()

    def create_table_ways(self):
        """ Создание временной таблицы путей """
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS ways
                          (id int primary key, nodes text, tags text)""")
        self.conn.commit()

    def delete_table_nodes(self):
        """ Удаление временной таблицы точек """
        self.cursor.execute("DROP TABLE IF EXISTS nodes")
        self.conn.commit()

    def delete_table_ways(self):
        """ Удаление временной таблицы путей """
        self.cursor.execute("DROP TABLE IF EXISTS ways")
        self.conn.commit()

    def add_data_to_geo(self, data):
        """ Добавление данных в таблицу geo """
        self.cursor.executemany("insert or replace into geo values(?, ?, ?, ?, ?, ?, ?)", data)
        self.conn.commit()

    def add_nodes(self, nodes):
        """ Добавление точек в таблицу nodes """
        self.cursor.executemany("insert or replace into nodes values(?, ?, ?, ?)", nodes)
        self.conn.commit()

    def add_ways(self, ways):
        """ Добавление путей в таблицу ways """
        self.cursor.executemany("insert or replace into ways values(?, ?, ?)", ways)
        self.conn.commit()

    def get_nodes_with_tags(self):
        """ Возвращает точки, у которых есть теги """
        self.cursor.execute("select * from nodes where tags is not null")
        return self.cursor.fetchall()

    def get_ways(self):
        """ Возвращает пути, у которых есть теги """
        self.cursor.execute("select * from ways where tags is not null")
        return self.cursor.fetchall()

    def get_coords_by_id(self, ids):
        """ Возвращает координаты по данным id """
        sql = "select lat, lon from nodes where id=?"
        coords = []
        for id in ids:
            self.cursor.execute(sql, [id])
            coords.append(self.cursor.fetchone())
        return coords
