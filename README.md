# zabbix 自定义监控项

## 1.zabbix_request:post请求
### shell脚本运行测试：
````
获取返回码：
./zabbix_request_code.sh http://baidu.com param1 param1_value param2 param2_value param3 param3_value

获取响应时间（毫秒）：
./zabbix_request_time.sh http://baidu.com param1 param1_value param2 param2_value param3 param3_value
````


### zabbix_get 测试
    zabbix_get -s localhost -p 10050 -k "post.code[http://baidu.com/,param1,param1_value,param2,param2_value,param3,param3_value]"
    