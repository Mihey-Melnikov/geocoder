# Вход: адрес в свободной форме
# Выход: координаты и полный адрес
import xml_parser
import data_base

data = xml_parser.window("data/mgn.osm")
DB = data_base.DataBase()
DB.create_table_geo_bd()
qw = xml_parser.make_data_for_bd(data)
DB.add_data(qw)

DB = data_base.DataBase()
DB.show_all_data_by_street("проспект Ленина")


