import json
from proto.Interface import Interface


class Network(object):
    objects = dict()
    interfaces = dict()
    links = []
    id_counter = 0


def to_json():
    main_dict = {'objects': list(),
                 'links': Network.links,
                 'id_counter': Network.id_counter}
    for obj in Network.objects:
        main_dict['objects'].append(Network.objects[obj].to_dict())
    return json.dumps(main_dict)


def from_json(main_dict):
    from devices.PC import PC
    from devices.Switch import Switch

    Network.objects = dict()
    for obj in main_dict['objects']:
        Network.objects[obj['id']] = locals()[obj['class']](0)
        Network.objects[obj['id']].id = obj['id']
        ints = obj['interfaces']

        for i in ints:
            inter = Interface(Network.objects[obj['id']])
            inter.id = i['id']
            inter.mac = i['mac']
            inter.ipv4 = i['ipv4']
            inter.gateway = i['gateway']
            inter.net_mask = i['net_mask']
            Network.objects[obj['id']].interfaces.append(inter)
            Network.interfaces[inter.id] = inter
        if obj['class'] == "PC":
            Network.objects[obj['id']].arp_table = obj['arp_table']
        elif obj['class'] == "Switch":
            Network.objects[obj['id']].mac_table = obj['mac_table']
    Network.links = main_dict['links']
    Network.id_counter = main_dict['id_counter']


def add_object(obj):
    Network.objects[obj.id] = obj


def remove_object(obj_id: int):
    del Network.objects[obj_id]


def add_interface(inter):
    Network.interfaces[inter.id] = inter


def remove_interface(int_id):
    del Network.interfaces[int_id]


def create_link(int_id1, int_id2):
    Network.links.append((int_id1, int_id2))


def remove_link(any_int_id):
    for i in range(len(Network.links)):
        if Network.links[i][0] == any_int_id or Network.links[i][1] == any_int_id:
            del Network.links[i]


def find_int_mac(int_mac):
    for key in Network.interfaces:
        if Network.interfaces[key].mac == int_mac:
            return Network.interfaces[key].id
    return -1


def find_id_link(mac):
    link_id = find_int_mac(mac)

    for i in range(len(Network.links)):
        if Network.links[i][0] == link_id or Network.links[i][1] == link_id:
            return i
    return -1


def print_objects():
    for key in Network.objects:
        print(Network.objects[key])
        for inter in Network.objects[key].interfaces:
            print(f"\t{inter}")


def print_links():
    for link in Network.links:
        print(link)


def handle_frame(frame):
    start_mac = frame.sender_address
    link_id = find_id_link(start_mac)
    if link_id >= 0:
        end_id = Network.links[link_id][0] if start_mac == Network.interfaces[Network.links[link_id][1]].mac else Network.links[link_id][1]
        Network.interfaces[end_id].receive_frame(frame)
