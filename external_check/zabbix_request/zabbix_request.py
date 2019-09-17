import requests,json
import sys
import re

# code description
# code 0 , request error, forexample request timeout
# code 100 , param error
# code other, server response code



url = sys.argv[1]
request_timeout = 1.5
headers = {'Content-Type':'application/json;charset=UTF-8'}
request_param = {}

pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
if len(sys.argv) % 2 == 1 or len(re.findall(pattern,url)) == 0:
    print "code:100"
    exit(1)

if len(sys.argv) > 2:
    for i in range(2,len(sys.argv),2):
        request_param[sys.argv[i]] = sys.argv[i+1]
try:
    response=requests.post(url,data=json.dumps(request_param), headers=headers, timeout = request_timeout)
    print "code:"+str(response.status_code)
    print "time:"+str(response.elapsed.microseconds//1000)
except Exception as e:
    print e
    print "code:0"
