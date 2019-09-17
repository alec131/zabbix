from pyzabbix import ZabbixAPI
import time


class zabbix_api:
    def __init__(self, zabbix_server, zabbix_user, zabbix_passwd):
        # The hostname at which the Zabbix web interface is available
        self.zapi = ZabbixAPI(zabbix_server)
        # Login to the Zabbix API
        self.zapi.login(zabbix_user, zabbix_passwd)

zabbix_server = 'http://58.215.175.200/zabbix/'
zabbix_user = 'admin'
zabbix_passwd = '*****'
output_file = "./server_info.txt"

zabbix = zabbix_api(zabbix_server, zabbix_user, zabbix_passwd)
current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
count = 0

print("当前时间：{}\n".format(current_time))
sum_size = 0
count = 0
for h in zabbix.zapi.host.get(filter={"status": "0", "available": "1", "flags": "0"}):
    print()
    total_size = 0
    for i in zabbix.zapi.item.get(hostids=h['hostid'],
                              search={'name': 'Total disk space',},
                              output=['itemid','key_',"lastvalue"]):
        total_size += int(i['lastvalue'])
    print("ip:{} ，磁盘总容量{:.1f} G".format(h['name'],total_size/(1024*1024*1024)))
    sum_size += total_size
    count += 1
print("共计{}台服务器，总磁盘空间为:{:.1f}T".format(count, sum_size/(1024*1024*1024*1024)))

