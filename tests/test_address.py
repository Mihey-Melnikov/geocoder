import unittest
from address import Address


class AddressTester(unittest.TestCase):
    """ Класс-тестировщик класса Address """

    def test_init(self):
        addr = Address()
        self.assertTrue([addr.id, addr.city, addr.street, addr.house,
                         addr.postcode, addr.lat, addr.lon] == [None] * 7)
        addr = Address(id=1, city="Ekb", street="Mat", house="Mex",
                       postcode=123, lat=60.1, lon=50.1)
        self.assertEqual([addr.id, addr.city, addr.street, addr.house,
                         addr.postcode, addr.lat, addr.lon],
                         [1, "Ekb", "Mat", "Mex", 123, 60.1, 50.1])

    def test_str(self):
        addr = Address(id=1, city="Ekb", street="Mat", house="Mex",
                       postcode=123, lat=60.1, lon=50.1)
        output = "Ekb, Mat, Mex"
        self.assertEqual(str(addr), output)

    def test_full_addr(self):
        addr = Address(id=1, city="Ekb", street="Mat", house="Mex",
                       postcode=123, lat=60.1, lon=50.1)
        output = "Полный адрес: Ekb, Mat, Mex, 123\nКоординаты: 60.1, 50.1"
        self.assertEqual(addr.full_addr(), output)


if __name__ == '__main__':
    unittest.main()
