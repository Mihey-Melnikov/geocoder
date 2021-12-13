import unittest
import preprocessor
from database import DataBase
import os


class PreprocessorTester(unittest.TestCase):
    """ Класс-тестировщик модуля preprocessor """

    def test_parse_simple_node(self):
        xml_data = """
        <node id="1" lat="50.1" lon="60.1" version="1"/>
        <node id="2" lat="50.2" lon="60.2" version="1"/>
        <node id="3" lat="50.3" lon="60.3" version="1"/>"""
        output_data = [("1", "50.1", "60.1", None),
                       ("2", "50.2", "60.2", None),
                       ("3", "50.3", "60.3", None)]
        self.assertEqual(preprocessor.parse_simple_nodes(xml_data),
                         output_data)
        self.assertEqual(preprocessor.parse_simple_nodes("something"), [])

    def test_parse_tags(self):
        xml_tags = """
        <tag k="Mat" v="Mex"/>
        <tag k="Python" v="geocoder"/>"""
        self.assertEqual(preprocessor.parse_tags(xml_tags),
                         "Mat,Mex;Python,geocoder")
        self.assertEqual(preprocessor.parse_tags("something"), "")

    def test_parse_complex_nodes(self):
        xml_data = """
        <node id="1" lat="50.1" lon="60.1" version="1">
            <tag k="Mat" v="Mex"/>
            <tag k="Python" v="geocoder"/>
        </node>"""
        self.assertEqual(preprocessor.parse_complex_nodes(xml_data),
                         [("1", "50.1", "60.1", "Mat,Mex;Python,geocoder")])
        self.assertEqual(preprocessor.parse_complex_nodes("something"), [])

    def test_parse_ways(self):
        xml_data = """
        <way id="123" version="1">
            <nd ref="1"/>
            <nd ref="2"/>
            <tag k="Mat" v="Mex"/>
            <tag k="Python" v="geocoder"/>
        </way>"""
        self.assertEqual(preprocessor.parse_ways(xml_data),
                         [("123", "1;2", "Mat,Mex;Python,geocoder")])
        self.assertEqual(preprocessor.parse_ways("something"), [])

    def test_parse_nodes(self):
        xml_data = """
        <nd ref="123"/>
        <nd ref="234"/>
        <nd ref="234"/>"""
        self.assertEqual(preprocessor.parse_nodes(xml_data), "123;234;234")
        self.assertEqual(preprocessor.parse_nodes("something"), "")

    def test_add_data_to_db(self):
        db = DataBase("./testdatabase.db")
        db.create_temp_table_nodes()
        db.create_temp_table_ways()
        db.create_table_geo()
        xml_data = """
        <node id="1" lat="50.1" lon="60.1" version="1"/>
        <node id="2" lat="50.2" lon="60.2" version="1"/>
        <node id="3" lat="50.3" lon="60.3" version="1"/>
        <node id="42" lat="50.42" lon="60.42" version="1">
            <tag k="Mgn" v="FIIT"/>
            <tag k="qwe" v="rty"/>
        </node>
        <way id="123" version="1">
            <nd ref="1"/>
            <nd ref="2"/>
            <tag k="Mat" v="Mex"/>
            <tag k="Python" v="geocoder"/>
        </way>"""
        preprocessor.add_data_to_db(xml_data, db)
        nodes_table_data = [(1, 50.1, 60.1, None),
                            (2, 50.2, 60.2, None),
                            (3, 50.3, 60.3, None),
                            (42, 50.42, 60.42, 'Mgn,FIIT;qwe,rty')]
        ways_table_data = [(123, '1;2', 'Mat,Mex;Python,geocoder')]
        self.assertEqual(db.get_data_from_table("*", "nodes"),
                         nodes_table_data)
        self.assertEqual(db.get_data_from_table("*", "ways"),
                         ways_table_data)
        db.close()
        os.remove("./testdatabase.db")

    def test_format_node_for_geo_db(self):
        db = DataBase("./testdatabase.db")
        db.create_temp_table_nodes()
        xml_data = """
            <node id="42" lat="50.42" lon="60.42" version="1">
                <tag k="addr:city" v="FIIT"/>
                <tag k="addr:street" v="qwerty"/>
                <tag k="addr:housenumber" v="42"/>
            </node>"""
        preprocessor.add_data_to_db(xml_data, db)
        nodes = db.get_data_with_tags_from_table("nodes")
        self.assertEqual(preprocessor.format_node_for_geo_db(nodes),
                         [(42, 50.42, 60.42, 'FIIT', 'qwerty', '42', None)])
        self.assertEqual(preprocessor.format_node_for_geo_db(["something"]),
                         [])
        db.close()
        os.remove("./testdatabase.db")

    def test_get_mass_center(self):
        mass_data = [(50, 60), (40, 50), (60, 70), (50, 60)]
        self.assertEqual(preprocessor.get_mass_center(mass_data),
                         (50.0, 60.0))

    def test_get_addr_data(self):
        addr = "addr:city,Mgn;addr:street,FIIT;" \
               "addr:housenumber,42;addr:postcode,123"
        self.assertEqual(preprocessor.get_addr_data(addr),
                         ("Mgn", "FIIT", "42", "123"))
        addr = "addr:city,Mgn;addr:street,FIIT;addr:housenumber,42"
        self.assertEqual(preprocessor.get_addr_data(addr),
                         ("Mgn", "FIIT", "42", None))
        addr = "addr:city,Mgn;addr:street,FIIT"
        self.assertEqual(preprocessor.get_addr_data(addr), None)
        self.assertEqual(preprocessor.get_addr_data("something"), None)


if __name__ == '__main__':
    unittest.main()
