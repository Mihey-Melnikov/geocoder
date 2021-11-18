import re


SIMPLE_NODE_RE = re.compile(r"""<node id="(\d+)" lat="(\d+\.\d+)" lon="(\d+\.\d+)" version="\d+"\/>""")
COMPLEX_NODE_RE = re.compile(r"""<node id="(\d+)" lat="(\d+\.\d+)" lon="(\d+\.\d+)" version="\d+">((\s+?<tag k=".+?" v=".+?"\/>)+?)\s+?<\/node>""")
TAGS_RE = re.compile(r"""<tag k="(.+?)" v="(.+?)"\/>""")
WAYS_RE = re.compile(r"""<way id="(\d+)" version="\d+">((\s+?<nd ref=".+?"\/>)+?)\s+?((\s+?<tag k=".+?" v=".+?"\/>)+?)\s+?<\/way>""")
NODE_RE = re.compile(r"""<nd ref="(.+?)"\/>""")


def parse_simple_nodes(xml_data):
    """ Парсит точки из формата XML в формат для БД"""
    all_match = re.findall(SIMPLE_NODE_RE, xml_data)
    nodes_dict = {}
    for match in all_match:
        nodes_dict[match[0]] = (match[0], match[1], match[2], None)
    return list(nodes_dict.values())


def parse_tags(xml_tags):
    """ Парсит теги из формата XML для хранения в БД """
    all_match = re.findall(TAGS_RE, xml_tags)
    tags = []
    for match in all_match:
        tags.append(f"{match[0]},{match[1]}")
    return ";".join(tags)


def parse_complex_nodes(xml_data):
    """ Парсит точки из формата XML для хранения в БД """
    all_match = re.findall(COMPLEX_NODE_RE, xml_data)
    nodes_dict = {}
    for match in all_match:
        nodes_dict[match[0]] = (match[0], match[1], match[2], parse_tags(match[3]))
    return list(nodes_dict.values())


def parse_ways(xml_data):
    """ Парсит пути из формата XML для хранения в БД """
    all_match = re.findall(WAYS_RE, xml_data)
    ways_dict = {}
    for match in all_match:
        ways_dict[match[0]] = (match[0], parse_nodes(match[1]), parse_tags(match[3]))
    return list(ways_dict.values())


def parse_nodes(xml_data):
    """ Парсит id точек для хранения в БД """
    all_match = re.findall(NODE_RE, xml_data)
    nodes = []
    for match in all_match:
        nodes.append(match)
    return ";".join(nodes)


def add_data_to_db(data, db):
    """ Добавляет данные в таблицу geo """
    simple_nodes_db_format = parse_simple_nodes(data)
    if len(simple_nodes_db_format) != 0:
        db.add_nodes(simple_nodes_db_format)

    complex_nodes_db_format = parse_complex_nodes(data)
    if len(complex_nodes_db_format) != 0:
        db.add_nodes(complex_nodes_db_format)

    ways_db_format = parse_ways(data)
    if len(ways_db_format) != 0:
        db.add_ways(ways_db_format)


def window(path, db):
    """ Скользящее окно """
    file = open(path, 'r', encoding='utf-8')
    previous_data = ''
    while True:
        new_data = file.read(2 ** 15)
        if not new_data:
            break
        add_data_to_db(previous_data + new_data, db)
        previous_data = new_data
    file.close()


def format_node_for_geo_db(data):
    """ Форматирует данные точек для загрузки в таблицу geo """
    format_node = []
    for node in data:
        addr_data = get_addr_data(node[3])
        if addr_data is None:
            continue
        format_node.append((node[0], node[1], node[2]) + addr_data)
    return format_node


def get_mass_center(mass):
    """ Возвращает центр масс домов """
    lat = sum(coord[0] for coord in mass[:-1]) / (len(mass) - 1)
    lon = sum(coord[1] for coord in mass[:-1]) / (len(mass) - 1)
    return lat, lon


def format_way_for_geo_db(data, db):
    """ Форматирует данные путей для загрузки в таблицу geo """
    format_way = []
    for way in data:
        addr_data = get_addr_data(way[2])
        if addr_data is None:
            continue
        lat, lon = get_mass_center(db.get_coords_by_id(way[1].split(';')))  # тип инт // стр
        format_way.append((way[0], lat, lon) + addr_data)
    return format_way


def get_addr_data(tags):
    """ Возвращает адрес из тегов """
    if 'addr:city' not in tags or 'addr:street' not in tags or 'addr:housenumber' not in tags:
        return None
    tags_dict = {}
    for pair in tags.split(';'):
        key_value = pair.split(',')
        if len(key_value) < 2:
            continue
        tags_dict[key_value[0]] = key_value[1]
    return (tags_dict.get('addr:city'), tags_dict.get('addr:street'),
            tags_dict.get('addr:housenumber'), tags_dict.get('addr:postcode'))


def fill_geo_db(db):
    """ Заполняет таблицу geo """
    nodes = db.get_nodes_with_tags()
    db.add_data_to_geo(format_node_for_geo_db(nodes))

    ways = db.get_ways()
    db.add_data_to_geo(format_way_for_geo_db(ways, db))


def run(db):
    """ Запускает программу """
    window("data/mgn.osm", db)
    fill_geo_db(db)
