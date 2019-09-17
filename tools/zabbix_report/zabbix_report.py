"""
Retrieves
history
data
for a given numeric (either int or float) item_id
"""

from pyzabbix import ZabbixAPI
from datetime import datetime
import time
import my_sort


class zabbix_api:
    def __init__(self, zabbix_server, zabbix_user, zabbix_passwd):
        # The hostname at which the Zabbix web interface is available
        self.zapi = ZabbixAPI(zabbix_server)
        # Login to the Zabbix API
        self.zapi.login(zabbix_user, zabbix_passwd)

    def trend_get(self, itemID='', time_from='', time_till=''):
        '''
        内部函数
        输出一段时间内的某个item的最大值、平均值、最小值
        '''
        trend_min_data = []
        trend_max_data = []
        trend_avg_data = []
        trend_min_data[:] = []
        trend_max_data[:] = []
        trend_avg_data[:] = []
        response = self.zapi.trend.get(
            time_from=time_from,
            time_till=time_till,
            output=[
                "itemid",
                "clock",
                "num",
                "value_min",
                "value_avg",
                "value_max"
            ],
            itemids=itemID,
            limit="8760"
        )
        if len(response) == 0:
            return 0.0, 0.0, 0.0
        for result_info in response:
            trend_min_data.append(result_info['value_min'])
            trend_max_data.append(result_info['value_max'])
            trend_avg_data.append(result_info['value_avg'])
        trend_min_data_all = my_sort.Stats(trend_min_data)
        trend_max_data_all = my_sort.Stats(trend_max_data)
        trend_avg_data_all = my_sort.Stats(trend_avg_data)
        trend_min = trend_min_data_all.min()
        trend_max = trend_max_data_all.max()
        trend_avg = float('%0.4f' % trend_avg_data_all.avg())

        return (trend_min, trend_max, trend_avg)


zabbix_server = 'http://58.215.175.200/zabbix/'
zabbix_user = 'admin'
zabbix_passwd = '*********'
output_file = "./server_info.txt"

# Create a time range
time_till = time.mktime(datetime.now().timetuple())
time_from = time_till - 60 * 60 * 24 * 7  # last 4 hours
zabbix = zabbix_api(zabbix_server, zabbix_user, zabbix_passwd)
current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
count = 0

net_if_in_keylist = ['net.if.in[eth0]', 'net.if.in[eth1]', 'net.if.in[eth2]', 'net.if.in[eth3]',
                  'net.if.in[em1]', 'net.if.in[em2]', 'net.if.in[em3]', 'net.if.in[em4]',
                  'net.if.in[vnet1]', 'net.if.in[em2]', 'net.if.in[em3]', 'net.if.in[em4]',
                  'net.if.in[Broadcom BCM5716C NetXtreme II GigE (NDIS VBD Client) #1]',
                  'net.if.in[Broadcom BCM5716C NetXtreme II GigE (NDIS VBD Client) #2]',
                  'net.if.in[Broadcom BCM5716C NetXtreme II GigE (NDIS VBD Client) #3]',
                  'net.if.in[Broadcom BCM5716C NetXtreme II GigE (NDIS VBD Client) #4]',
                  'net.if.in[Broadcom NetXtreme Gigabit Ethernet]',
                  'net.if.in[Broadcom NetXtreme Gigabit Ethernet #2]',
                  'net.if.in[Broadcom NetXtreme Gigabit Ethernet #3]'
                  'net.if.in[Broadcom NetXtreme Gigabit Ethernet #4]']

net_if_out_keylist = ['net.if.out[eth0]', 'net.if.out[eth1]', 'net.if.out[eth2]', 'net.if.out[eth3]',
                   'net.if.out[em1]', 'net.if.out[em2]', 'net.if.out[em3]', 'net.if.out[em4]',
                   'net.if.out[vnet1]', 'net.if.out[em2]', 'net.if.out[em3]', 'net.if.out[em4]',
                   'net.if.out[Broadcom BCM5716C NetXtreme II GigE (NDIS VBD Client) #1]',
                   'net.if.out[Broadcom BCM5716C NetXtreme II GigE (NDIS VBD Client) #2]',
                   'net.if.out[Broadcom BCM5716C NetXtreme II GigE (NDIS VBD Client) #3]',
                   'net.if.out[Broadcom BCM5716C NetXtreme II GigE (NDIS VBD Client) #4]',
                   'net.if.out[Broadcom NetXtreme Gigabit Ethernet]',
                   'net.if.out[Broadcom NetXtreme Gigabit Ethernet #2]',
                   'net.if.out[Broadcom NetXtreme Gigabit Ethernet #3]'
                   'net.if.out[Broadcom NetXtreme Gigabit Ethernet #4]']

disk_total_key_list = ['vfs.fs.size[C:,total]','vfs.fs.size[D:,total]','vfs.fs.size[E:,total]','vfs.fs.size[F:,total]',
                        'vfs.fs.size[/qingkedata1,total]','vfs.fs.size[/qingkedata2,total]','vfs.fs.size[/qingkedata3,total]',
                       'vfs.fs.size[/qingke,total]','vfs.fs.size[/,total]']

disk_free_key_list = ['vfs.fs.size[C:,free]','vfs.fs.size[D:,free]','vfs.fs.size[E:,free]','vfs.fs.size[F:,free]',
                        'vfs.fs.size[/qingkedata1,free]','vfs.fs.size[/qingkedata2,free]','vfs.fs.size[/qingkedata3,free]',
                       'vfs.fs.size[/qingke,free]','vfs.fs.size[/,free]']

with open(output_file, 'w+') as f:
    f.write("当前时间：{}\n".format(current_time))
    for h in zabbix.zapi.host.get(filter={"status": "0", "available": "1", "flags": "0"}):

        os = ""
        mem_total, mem_free = 0,0
        cpu_num, cpu_load = 0,0
        net_in_map, net_out_map = {}, {}
        disk_total, disk_free = 0,0

        for i in zabbix.zapi.item.get(hostids=h['hostid'],
                                      filter={'key_': ['system.uname']},
                                      output=["lastvalue", ""]):
            os = i["lastvalue"]
        # memory total
        for i in zabbix.zapi.item.get(hostids=h['hostid'], filter={'key_': ['vm.memory.size[total]', ]},
                                      output=["lastvalue", ""]):
            mem_total = int(i["lastvalue"])


        # memory free
        for i in zabbix.zapi.item.get(hostids=h['hostid'],
                                      filter={'key_': ['vm.memory.size[free]', 'vm.memory.size[available]']},
                                      output=["itemid", ""]):
            tmp = zabbix.trend_get(itemID=i["itemid"], time_from=time_from, time_till=time_till)
            mem_free = int(tmp[0])

        # cpu number
        for i in zabbix.zapi.item.get(hostids=h['hostid'],
                                      filter={'key_': ['system.cpu.num']},
                                      output=["lastvalue", ""]):
            cpu_num = int(i["lastvalue"])

        # cpu load
        cpu_load_key = ['system.cpu.load[percpu,avg1]'] if os.find("Linux") != -1 else ['perf_counter[\Processor(_Total)\% Processor Time]']
        for i in zabbix.zapi.item.get(hostids=h['hostid'],
                                      filter={'key_': cpu_load_key},
                                      output=["itemid", ""]):
            tmp = zabbix.trend_get(itemID=i["itemid"], time_from=time_from, time_till=time_till)
            cpu_load = float(tmp[1])
        # disk total
        for i in zabbix.zapi.item.get(hostids=h['hostid'],
                                      filter={'key_': disk_total_key_list},
                                      output=["lastvalue", ""]):
            disk_total += int(i["lastvalue"])

        # disk free
        for i in zabbix.zapi.item.get(hostids=h['hostid'],
                                      filter={'key_': disk_free_key_list},
                                      output=["lastvalue", ""]):
            disk_free += int(i['lastvalue'])

        # net_inf in
        for i in zabbix.zapi.item.get(hostids=h['hostid'],
                                      filter={'key_': net_if_in_keylist},
                                      output=["itemid", ""]):
            tmp = zabbix.trend_get(itemID=i["itemid"], time_from=time_from, time_till=time_till)
            if net_in_map:
                if tmp[1] > net_in_map['max']:
                    net_in_map['max'] = int(tmp[1])
                    net_in_map['min'] = int(tmp[0])
                    net_in_map['avg'] = int(tmp[2])
            else:
                net_in_map['max'] = int(tmp[1])
                net_in_map['min'] = int(tmp[0])
                net_in_map['avg'] = int(tmp[2])

        # net_if out
        for i in zabbix.zapi.item.get(hostids=h['hostid'],
                                      filter={'key_': net_if_out_keylist},
                                      output=["itemid", ""]):
            tmp = zabbix.trend_get(itemID=i["itemid"], time_from=time_from, time_till=time_till)
            if net_out_map:
                if tmp[1] > net_out_map['max']:
                    net_out_map['max'] = int(tmp[1])
                    net_out_map['min'] = int(tmp[0])
                    net_out_map['avg'] = int(tmp[2])
            else:
                net_out_map['max'] = int(tmp[1])
                net_out_map['min'] = int(tmp[0])
                net_out_map['avg'] = int(tmp[2])

        disk_total = int(disk_total) // (1024 * 1024 * 1024)
        disk_free = int(disk_free) // (1024 * 1024 * 1024)

        mem_total //= (1024 * 1024* 1024)
        mem_free //= (1024 * 1024* 1024)

        cpu_load = "{:.2f}".format(cpu_load*cpu_num) if os.find("Linux") != -1 else "{:.2f}%".format(cpu_load)

        net_in_max = net_in_map['max'] / (1024 * 1024) if net_in_map else 0
        net_in_min = net_in_map['min'] / (1024 * 1024) if net_in_map else 0
        net_in_avg = net_in_map['avg'] / (1024 * 1024) if net_in_map else 0

        net_out_max = net_out_map['max'] / (1024 * 1024) if net_out_map else 0
        net_out_min = net_out_map['min'] / (1024 * 1024) if net_out_map else 0
        net_out_avg = net_out_map['avg'] / (1024 * 1024) if net_out_map else 0

        count += 1

        print("{}服务器信息：".format(h['name']))
        print("磁盘：共{}G、用{}G、剩余{}G".format(disk_total, disk_total - disk_free, disk_free))
        print("内存：共{}G、使用峰值{}G".format(mem_total, mem_total - mem_free, mem_free))
        print("cpu_load_list：{}核，负载峰值{}".format(cpu_num,cpu_load))
        print("in-network:最高{:.2f}Mbps、最低{:.2f}Mbs、平均{:.2f}Mbs".format(net_in_max, net_in_min, net_in_avg))
        print("out-network:最高{:.2f}Mbps、最低{:.2f}Mbs、平均{:.2f}Mbs".format(net_out_max, net_out_min, net_out_avg))
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        f.write("{}服务器信息：\n".format(h['name']))
        f.write("磁盘：共{}G、用{}G、剩余{}G\n".format(disk_total, disk_total - disk_free, disk_free))
        f.write("内存：共{}G、使用峰值{}G\n".format(mem_total, mem_total - mem_free, mem_free))
        f.write("cpu_load_list：{}核，负载峰值{}\n".format(cpu_num,cpu_load))
        f.write("in-network:最高{:.2f}Mbps、最低{:.2f}Mbs、平均{:.2f}Mbs\n".format(net_in_max, net_in_min, net_in_avg))
        f.write("out-network:最高{:.2f}Mbps、最低{:.2f}Mbs、平均{:.2f}Mbs\n".format(net_out_max, net_out_min, net_out_avg))
        f.write("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    print("共{}服务器".format(count))
    f.write("共{}服务器".format(count))
