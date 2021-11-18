import data_base
import preprocess

db = data_base.DataBase()
db.create_table_nodes()
db.create_table_ways()
db.create_table_geo()
preprocess.run(db)


