class Address:
    def __init__(self, id=None, city=None, street=None, house=None, postcode=None, lat=None, lon=None):
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

    def add(self, city=None, street=None, house=None, postcode=None, lat=None, lon=None):
        if self.city is None and city is not None:
            self.city = city
        if self.street is None and street is not None:
            self.street = street
        if self.house is None and house is not None:
            self.house = house
        if self.postcode is None and postcode is not None:
            self.postcode = postcode
        if self.lat is None and lat is not None:
            self.lat = lat
        if self.lon is None and lon is not None:
            self.lon = lon

    def full_addr(self):
        return f"Полный адрес: {self.city}, {self.street}, {self.house}, {self.postcode}\n" \
               f"Координаты: {self.lat}, {self.lon}"

