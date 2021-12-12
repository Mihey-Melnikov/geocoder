class Address:
    """ Класс, хранящий в себе данные адреса из базы """

    def __init__(self, id=None, city=None, street=None,
                 house=None, postcode=None, lat=None, lon=None):
        """ Инициализация """

        self.id = id
        self.city = city
        self.street = street
        self.house = house
        self.postcode = postcode
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return f"{self.city}, {self.street}, {self.house}"

    def __str__(self):
        return repr(self)

    def full_addr(self):
        """ Возвращает строку полного адреса """

        return f"Полный адрес: {self.city}, {self.street}, " \
               f"{self.house}, {self.postcode}\n" \
               f"Координаты: {self.lat}, {self.lon}"
