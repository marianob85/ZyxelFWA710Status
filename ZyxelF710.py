import telnetlib
import re
import json
import argparse

def telnet(args):
    tn = telnetlib.Telnet(args.client)
    tn.read_until(b"FWA710 login: ")
    tn.write("{}\r\n".format( args.username ).encode('UTF-8') )
    tn.read_until(b"Password: ")
    tn.write("{}\r\n".format( args.password ).encode('UTF-8'))
    tn.write(b"cfg cellwan_status get\r\n")
    data = tn.read_until(match=b"SCC 1 information", timeout=5).decode('ascii')
    tn.close()
    return data

test_data = """
ZySH> cfg cellwan_status get
Cell ID:                       57732897
Physical Cell ID:              90
UL Bandwidth (MHz):            15
DL Bandwidth (MHz):            15
RFCN:                          3025
RSSI:                          -65
RSRP:                          -84
RSRQ:                          -18
RSCP:                          -120
EcNo:                          -240
SINR:                          4
TAC:                           52502
LAC:                           N/A
RAC:                           N/A
BSIC:                          N/A
CQI:                           0
MCS:                           1
RI:                            2
PMI:                           0

SCC 1 information:"""

if __name__ == '__main__': 

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=True, help='Username for access to RouterOS, default: local username')
    parser.add_argument('-p', '--password', required=True, help='password for access to RouterOS, default:')
    parser.add_argument('-c', '--client', required=True, help='RouterOS host to upgrade')
    args = parser.parse_args()

    data = telnet(args)
    objects = {}
    values = ["Cell ID", "RFCN", "RSSI", "RSRP", "RSRQ", "SINR", "TAC"]
    for line in data.splitlines():
        for value in values:
            search_line = ( rf'^{value}:(.+)' )
            match = re.search(search_line, line )
            if match:
                objects[ value.replace(" ", "_") ] = int( match.group(1).strip() )
    json_data = json.dumps(objects, indent=2)
    print( json_data )