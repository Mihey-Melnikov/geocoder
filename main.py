import re
# Вход: адрес в свободной форме
# Выход: координаты и полный адрес

def parse_tags(tags):
    reg_tag = re.compile(r"""<tag k="(.+?)" v="(.+?)"\/>""")
    all_match = re.findall(reg_tag, tags)
    tags_dict = {}
    for match in all_match:
        tags_dict[match[0]] = match[1]
    return tags_dict


def get_data_for_bd(xml_data):
    reg_node = re.compile(
        r"""<node id="(?P<id>\d+)" lat="(?P<lat>\d+\.\d+)" lon="(?P<lon>\d+\.\d+)" version="\d+">(?P<tags>(\s+?<tag k=".+?" v=".+?"\/>)+?)\s+?<\/node>""")
    all_match = re.findall(reg_node, xml_data)
    mini_bd = []
    for match in all_match:
        new_node = {"id": match[0], "lat": match[1], "lon": match[2], "tags": parse_tags(match[3])}
        mini_bd.append(new_node)
    return mini_bd


def read_osm():
    with open("test.txt", "r", encoding='utf-8') as file:
        xml_data = file.read()
    return xml_data


bd = get_data_for_bd(read_osm())
for i in bd:
    print(i)







