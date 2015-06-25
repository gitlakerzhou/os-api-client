#!/usr/bin/env python
import sys
import json

networks = []

def readInput():
    global networks
    with open('OS_networks.json') as data_file:
		networks = json.load(data_file)


def main(argv):
    global networks
    cmds = ''
    evc = 1
    vlan = 0
    l = len(argv)
    if l < 1:
        print "usage: python gen65cmd <evc_start_num>  [vlan_diff]"
        print "example: python gen65cmd 1 500"
        print "       evc start from 1"
        print "       new vlan tag = 500 + old vlan tag"
        exit(1)
    if l == 1:
        evc = int(argv[0])
    if l == 2:
        evc = int(argv[0])
        vlan = int(argv[1])

    n = -1
    readInput()

    for net in networks:
        n = n+1
        cur_evc = evc + n
        if vlan != 0:
            nvlan = vlan+ int(net['provider_segmentation_id'])
            cmds += "evc " + str(cur_evc) + " vid " + str(nvlan) + ' interface 2.5GigabitEthernet 1/2 learning policer none \n'
        else:
            cmds += "evc " + str(cur_evc) + " vid " + net['new_vlan'] + ' interface 2.5GigabitEthernet 1/2 learning policer none\n'
        cmds += 'evc ece ' + str(cur_evc) + ' interface GigabitEthernet 1/2 outer-tag match type c-tagged vid ' + str(net['provider_segmentation_id']) + " policer none pop 1\n"

        f = open('swapvlan.cmd', 'w+')
        f.write(cmds)
        f.close()

if __name__ == "__main__":
   main(sys.argv[1:])

