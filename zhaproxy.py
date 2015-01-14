#!/usr/bin/env python
#turn on stats unix socket /etc/haproxy/haproxy.cfg


import socket
import sys
import getopt

HA_STAT_MAPPING = {
    'qcur': 0,
    'qmax': 1,
    'scur': 2,
    'smax': 3,
    'slim': 4,
    'stot': 5,
    'bin': 6,
    'bout': 7,
    'dreq': 8,
    'dresp': 9,
    'ereq': 10,
    'econ': 11,
    'eresp': 12,
    'wretr': 13,
    'wredis': 14,
    'status': 15,
    'chkfail': 19,
    'rate': 31,
    'hrsp_1xx': 37,
    'hrsp_2xx': 38,
    'hrsp_3xx': 39,
    'hrsp_4xx': 40,
    'hrsp_5xx': 41,
    'hrsp_other': 42,
    'req_rate': 44,
    'cli_abrt': 47,
}

ERROR_MSG = 'ZBX_NOTSUPPORTED'


def connect(socket_path='/var/run/haproxy.sock'):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(socket_path)
    return s


def send_command(command):
    s = connect()
    result = ''
    if command[-1] != '\n':
        command += '\n'
    s.send(command)
    while 1:
        data = s.recv(1024)
        if not data:
            break
        result += data
    s.close()
    return result


def show_stat():
    result = {}
    output = send_command("show stat")
    for line in output.split('\n'):
        if(len(line) == 0 or line[0] == '#'):
            continue
        fields = line.split(",")
        result[fields[0] + '.' + fields[1]] = fields[2:]
    return result


def get_sv_stat(pxname, svname, hastat):
    output = show_stat()
    try:
        result = output['.'.join([pxname, svname])][HA_STAT_MAPPING[hastat]]
    except KeyError:
        result = ERROR_MSG
    if(len(result) == 0):
        result = ERROR_MSG
    return result


def discover_prxy_srv():
    output = show_stat()
    #JSON data header
    result = '{ "data": [\n'
    for key in output:
        (pxname, svname) = key.split('.')
        result += '{ "{#PROXY_NAME}":"%s", "{#SRV_NAME}":"%s" },\n' % (pxname, svname)
    #JSON data footer
    result += ']}'
    return result

#check all proxyname status
def check_prxy_srv():
    output = show_stat()
    Msg = 0
    for key in output:
	 result= output[key][15] 
         if result == 'OPEN' or result == 'UP':
            continue
         elif result == 'DOWN':
              #print "please check %10s" %key
              Msg += 1
    return Msg

if __name__ == "__main__":
    discover = False
    pxname = svname = value = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'dchp:s:v:')
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    for o, a in opts:
        if o == '-d':
            discover = True
            break
        if o == '-c':
            allstat = True
            break
        if o == '-h':
            break
        if o == '-p':
            pxname = a
        if o == '-s':
            svname = a
        if o == '-v':
            value = a
    if(discover):
        result = discover_prxy_srv()
    elif(len(pxname) * len(svname) * len(value) > 0):
        result = get_sv_stat(pxname, svname, value)
    elif(allstat):
        result = check_prxy_srv() 
    else:
        print ERROR_MSG
        sys.exit(2)
#format status output
    if result == 'OPEN' or result == 'UP':
        result = '1'
    elif result == 'DOWN':
	result = '0'
    print result 
