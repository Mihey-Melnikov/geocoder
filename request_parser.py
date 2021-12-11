def check_city(db, city):
    """
    Проверяет, является ли входная строка городом
    Возвращает город в правильном виде
    Иначе None
    """
    cities = [c[0] for c in db.get_cities_from_geo()]
    for probably_city in cities:
        if city.lower() in probably_city.lower():
            return probably_city
    return None


def check_street(db, street):
    """
    Проверяет, является ли входная строка улицей
    Возвращает улицу в правильном виде
    Иначе None
    """
    streets = [s[0] for s in db.get_streets_from_geo()]
    for probably_street in streets:
        if street.lower() in probably_street.lower():
            return probably_street
    return None


def parse_question(input, db):
    """
    Парсит запрос пользователя
    Возвращает город, улицу и дом в правильном формате
    """
    addr = input.split()
    city = street = house = None
    if len(addr) == 3:
        city = check_city(db, addr[0])
        street = check_street(db, addr[1])
        house = addr[2]
    elif len(addr) == 2:
        probably_city = check_city(db, addr[0])
        probably_street = check_street(db, addr[0])
        if probably_city:
            city = probably_city
            street = check_street(db, addr[1])
        elif probably_street:
            street = probably_street
            house = addr[1]
        else:
            return "Все плохо! Не нашли город и улицу!"
    else:
        return "Все плохо! Мало данных!"
    return city, street, house
