import data_base
from preprocessor import run
from request_parser import parse_question, parse_answer
from gui import GeoGui


# def preprocess(db, path):
#     run(db, path)
#
#
# db = data_base.DataBase()
# preprocess(db, "data/big_mgn.osm")
# db.delete_table_geo()


GeoGui().show()
