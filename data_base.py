import sqlite3


class DataBase:
    """ Класс отвечающий за базу данных """

    def __init__(self):
        """ Инициализация и создание базы данных """
        self.conn = sqlite3.connect(r"data/geodatabase.db")
        self.cursor = self.conn.cursor()

    def create_table_geo_bd(self):
        """ Создание таблицы """
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS geo_bd
                          (id int primary key, lat real, lon real, 
                          city text default null, street text default null, 
                          housenumber text default null, postcode int default null)
                       """)
        self.conn.commit()

    def add_data(self, data):
        """ Добавление данных в таблицу """
        self.cursor.executemany("insert into geo_bd values(?, ?, ?, ?, ?, ?, ?)", data)
        self.conn.commit()

    def show_all_data_by_street(self, street):
        """ Тест """
        sql = "select * from geo_bd where street=?"
        self.cursor.execute(sql, [(street)])
        print(self.cursor.fetchall())
