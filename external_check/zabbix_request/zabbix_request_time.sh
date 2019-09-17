#!/bin/bash

basename=$( dirname $( readlink -f $0 ))

res=$( python $basename/zabbix_request.py $@ )

for i in $( echo $res|awk '{ print $0 }' )
do
	echo $i|grep 'time'|awk -F: '{ print $2 }'
done
