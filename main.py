import json
import Network
from devices.Switch import *
from devices.PC import *
from Network import *
from packet_types.ARP import ARP


def save(filename):
    with open(filename, 'w') as file:
        file.write(to_json())


def load(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        from_json(data)


if __name__ == '__main__':
    while True:
        # try:
            cmd = input("> ").split(' ')
            if cmd[0] == "add":
                if cmd[1] == "pc":
                    add_object(PC(1))
                elif cmd[1] == "switch":
                    count = int(cmd[2])
                    add_object(Switch(count))
            elif cmd[0] == "list":
                print_objects()
            elif cmd[0] == "edit":
                if int(cmd[1]) in Network.objects:
                    cmd_1 = [""]
                    while not cmd_1[0] == "exit":
                        cmd_1 = input(f"ID: {cmd[1]} > ").split(" ")
                        if cmd_1[0] == "int" and int(cmd_1[1]) <= len(Network.objects[int(cmd[1])].interfaces) - 1:
                            cmd_2 = [""]
                            while not cmd_2[0] == "exit":
                                cmd_2 = input(f"ID {cmd[1]}; int {cmd_1[1]} > ").split(" ")
                                if cmd_2[0] == "ip":
                                    Network.objects[int(cmd[1])].interfaces[int(cmd_1[1])].ipv4 = [int(x) for x in cmd_2[1].split('.')]
                                    if len(cmd_2) >= 3:
                                        Network.objects[int(cmd[1])].interfaces[int(cmd_1[1])].net_mask = [int(x) for x in cmd_2[2].split('.')]
                                    if len(cmd_2) >= 4:
                                        Network.objects[int(cmd[1])].interfaces[int(cmd_1[1])].gateway = [int(x) for x in cmd_2[3].split('.')]
                                elif cmd_2[0] == "list":
                                    print(Network.objects[int(cmd[1])].interfaces[int(cmd_1[1])])
                        elif cmd_1[0] == "list":
                            for inter in Network.objects[int(cmd[1])].interfaces:
                                print(inter)
                        elif cmd_1[0] == "ping":
                            Network.objects[int(cmd[1])].send_icmp(int(cmd_1[1]), [int(x) for x in cmd_1[2].split(".")], "ping")
                        elif cmd_1[0] == "arp":
                            for arp in Network.objects[int(cmd[1])].arp_table:
                                print(arp)
            elif cmd[0] == "link":
                create_link(int(cmd[1]), int(cmd[2]))
            elif cmd[0] == "links":
                print_links()
            elif cmd[0] == "load":
                load(cmd[1])
            elif cmd[0] == "save":
                save(cmd[1])

        # except Exception as e:
        #     print("Wrong input!", e)
