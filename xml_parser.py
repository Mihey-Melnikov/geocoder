import re


def parse_tags(tags):
    reg_tag = re.compile(r"""<tag k="(.+?)" v="(.+?)"\/>""")
    all_match = re.findall(reg_tag, tags)
    tags_dict = {}
    for match in all_match:
        tags_dict[match[0]] = match[1]
    return tags_dict


def get_data_for_xml(xml_data):
    reg_node = re.compile(
        r"""<node id="(?P<id>\d+)" version="\d+" timestamp=".+?" lat="(?P<lat>\d+\.\d+)" lon="(?P<lon>\d+\.\d+)">(?P<tags>(\s+?<tag k=".+?" v=".+?"\/>)+?)\s+?<\/node>""")
    reg1_node = re.compile(
        r"""<node id="(?P<id>\d+)" lat="(?P<lat>\d+\.\d+)" lon="(?P<lon>\d+\.\d+)" version="\d+">(?P<tags>(\s+?<tag k=".+?" v=".+?"\/>)+?)\s+?<\/node>""")
    reg1_way = re.compile(
        r"""<way id="(?P<id>\d+)" version="\d+">(?P<nds>(\s+?<nd ref=".+?"\/>)+?)\s+?(?P<tags>(\s+?<tag k=".+?" v=".+?"\/>)+?)\s+?<\/way>""")
    all_node_match = re.findall(reg1_node, xml_data)
    all_way_match = re.findall(reg1_way, xml_data)
    mini_bd = {}
    for node in all_node_match:
        new_node = {"id": node[0], "lat": node[1], "lon": node[2], "tags": parse_tags(node[3])}
        mini_bd[node[0]] = new_node
    for way in all_way_match:
        new_way = {"id": way[0], "lat": 'pass', "lon": 'pass', "tags": parse_tags(way[3])}
        mini_bd[way[0]] = new_way
    return mini_bd


def window(part):
    file = open(part, 'r', encoding='utf-8')
    bd = {}
    previous_data = ''
    while True:
        new_data = file.read(2**15)
        if not new_data:
            break
        new_bd = get_data_for_xml(previous_data + new_data)
        bd |= new_bd
        previous_data = new_data
    return list(bd.values())


def make_data_for_bd(data):
    all_values = []
    for d in data:
        all_values.append((d['id'], d['lat'], d['lon'],
                           d['tags'].get('addr:city'),
                           d['tags'].get('addr:street'),
                           d['tags'].get('addr:housenumber'),
                           d['tags'].get('addr:postcode')))
    return all_values
