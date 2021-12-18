import re


def check_city(db, city):
    """
    Проверяет, является ли входная строка городом
    Возвращает город в правильном виде
    Иначе None
    """
    cities = [c[0] for c in db.get_data_from_table("city", "geo")]
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
    streets = list(set([s[0] for s in db.get_data_from_table("street", "geo")]))
    streets = list(filter(lambda x: x is not None, streets))
    for probably_street in streets:
        if street.lower() in probably_street.lower():  # проблема здесь!
            return probably_street
    return None


def parse_question(input, db, street_types):
    """
    Парсит запрос пользователя
    Возвращает город, улицу и дом в правильном формате
    """
    addr = list(filter(lambda x: len(x) != 0 and x not in street_types, re.split("[;,. ]", input)))
    addr = list(map(lambda x: x.lower(), addr))
    city = street = house = None

    for i in range(len(addr)):
        probably_city = check_city(db, addr[i])
        if probably_city is not None and city is None:
            city = probably_city
            for x in city.split():
                if x.lower() in addr:
                    del addr[addr.index(x.lower())]
            break

    for i in range(len(addr)):
        probably_street = check_street(db, addr[i])
        if probably_street is not None and street is None:
            street = probably_street
            for x in street.split():
                if x.lower() in addr:
                    del addr[addr.index(x.lower())]
            break

    if len(addr) != 0:
        for x in addr:
            if not x.isalpha():
                house = x
                break

    print(city, street, house)
    return city, street, house

# ищет не то Мира 19