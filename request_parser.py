# формат вывода:
# %имя% [область, край, республика],
# [город, деревня, поселок, село] %имя%,
# [улица, проспект, переулок] %имя%,
# [дом, корпус] %номер%
# [, почтовый индекс %номер%]
# ______________________________________
# формат ввода:
# [область] город улица дом

STREET_TYPES = ["улица", "проспект", "переулок", "шоссе", "посёлок", "поселок",
                "проезд", "заезд", "бульвар", "аллея", "бульвар"]

# def get_addr_data(input, db):
#     city, street, house = parse(input)
#     all_streets = db.get_streets_by_city_in_cities(city)


def check_city(db, city):
    cities = [c[0] for c in db.get_cities_from_geo()]
    for probably_city in cities:
        if city.lower() in probably_city.lower():
            return probably_city
    return None


def check_street(db, street):
    streets = [s[0] for s in db.get_streets_from_geo()]
    for probably_street in streets:
        if street.lower() in probably_street.lower():
            return probably_street
    return None


def parse_question(input, db):
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
            print("Все плохо! Не нашли город и улицу!")
    else:
        print("Все плохо! Мало данных!")
    return city, street, house


def parse_answer(data_list):
    print(f"По вашему запросу нашлось {len(data_list)} адресов:\n")
    for addr in data_list:
        print(f"""Полный адрес: {addr[3]}, {addr[4]}, {addr[5]}, индекс {addr[6]}
Широта: {addr[1]}, Долгота: {addr[2]}\n""")
