import data_base
from preprocessor import run
from request_parser import parse_question, parse_answer


def preprocess(db, path):
    run(db, path)


db = data_base.DataBase()
# preprocess(db, "data/big_mgn.osm")  # big_
# db.delete_table_geo()
while True:
    addr = input()
    city, street, house = parse_question(addr, db)
    parse_answer(db.get_rows_by(city, street, house))
