# Вход: адрес в свободной форме
# Выход: координаты и полный адрес
import xml_parser
import data_base


# xml_data = xml_parser.read_osm()
# data = xml_parser.get_data_for_xml(xml_data)
# DB = data_base.DataBase()
# DB.create_table_geo_bd()
# qw = xml_parser.make_data_for_bd(data)
# DB.add_data(qw)

DB = data_base.DataBase()
DB.show_all_data_by_street("улица Крауля")
