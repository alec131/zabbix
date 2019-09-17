# zabbix 导出所有服务器负载信息

主要配置：

zabbix_server = 'http://58.215.175.200/zabbix/'
zabbix_user = 'admin'
zabbix_passwd = '*********'
output_file = "./server_info.txt"




导出格式如下：
````
当前时间：2019-04-22 16:36:42
ZabbixServer1150服务器信息：
磁盘：共1083G、用599G、剩余484G
内存：共62G、使用峰值46G
cpu_load_list：20核，负载峰值8.34
in-network:最高179.67Mbps、最低0.96Mbs、平均10.10Mbs
out-network:最高150.82Mbps、最低0.91Mbs、平均5.48Mbs
+++++++++++++++++++++++++++++++++++++++++++++++++++++++
10.10.10.65服务器信息：
磁盘：共540G、用103G、剩余437G
内存：共62G、使用峰值47G
cpu_load_list：32核，负载峰值3.03
in-network:最高2.34Mbps、最低0.07Mbs、平均0.15Mbs
out-network:最高54.95Mbps、最低0.06Mbs、平均0.19Mbs
+++++++++++++++++++++++++++++++++++++++++++++++++++++++
````