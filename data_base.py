import sqlite3

conn = sqlite3.connect("geodatabase.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

# Создание таблицы
# cursor.execute("""CREATE TABLE albums
#                   (title text, artist text, release_date text,
#                    publisher text, media_type text)
#                """)
# conn.commit()

lst = ('qwerty', 'Mikhey', None, 'qq', 'pov')

cursor.execute("""INSERT INTO albums
                  VALUES (?, ?, ?, ?, ?)""", lst)

conn.commit()

sql = "SELECT * FROM albums WHERE artist=?"
cursor.execute(sql, [("Mikhey")])
print(cursor.fetchall()) # or use fetchone()
