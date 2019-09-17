#!/usr/bin/env python
import psutil
import sys
status_list = ["LISTEN", "ESTABLISHED", "TIME_WAIT", "CLOSE_WAIT", "LAST_ACK", "SYN_SENT"]

def netstat(sport=None, proc=None):
    status_temp = []
    net_connections = psutil.net_connections(kind=proc)
    for key in net_connections:
        if sport is None:
            status_temp.append(key.status)
        else:
            if str(key.laddr[1]) == sport:
                status_temp.append(key.status)
    return status_temp

if __name__ == "__main__":
    status_type = sys.argv[1] if len(sys.argv) > 1 else None
    port = sys.argv[2] if len(sys.argv) > 2 else None
    proc = status_type if status_type == "udp" else "tcp"
    status_info = netstat(port,proc)
	
    if proc == "udp":
        print(len(status_info))
        sys.exit()

    if status_type:
        print(status_info.count(status_type))
    else:
        print(len(status_info))
