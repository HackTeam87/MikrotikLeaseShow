#!usr/bin/python3
import re
import sys
from pprint import pprint
import routeros_api
from datetime import datetime, timedelta
now = datetime.now()

try:
  host=sys.argv[1]
except:
  pass

try:
  uname=sys.argv[2]
except:
  pass

try:
  passwd=sys.argv[3]
except:
  pass

try:
  port=int(sys.argv[4])
except:
  pass


class Mapi:
    
    def getlease(self, host,uname,passwd,port, command):
        
        connection = routeros_api.RouterOsApiPool(host, port=port,
                                                  username=uname,
                                                  password=passwd,
                                                  plaintext_login=True
                                                  )
        api = connection.get_api()
        list = api.get_resource(command)
        result = list.get()
        return(result)
    
    
    def format_time(self,ftime): #17w3d6h55m36s 
        if 'w' in ftime:
            weeks = re.search(r'(\d+)w', ftime).group(1)
        else: weeks = 0

        if 'd' in ftime:
            days = re.search(r'(\d+)d', ftime).group(1)
        else: days = 0

        if 'h' in ftime:
            hours = re.search(r'(\d+)h', ftime).group(1)
        else: hours = 0

        if 'm' in ftime:
            minutes = re.search(r'(\d+)m', ftime).group(1)
        else: minutes = 0

        if 's' in ftime:
            seconds = re.search(r'(\d+)s', ftime).group(1)
        else: seconds = 0   

        total_seconds = int(weeks) * 7 * 24 * 60 * 60 + int(days) * 24 * 60 * 60 + int(hours) * 60 * 60 + int(minutes) * 60 + int(seconds) 

        return total_seconds


# Достаем лиз с микротика
lease = Mapi().getlease(host, uname, passwd, port, '/ip/dhcp-server/lease')


arr = []
for l in lease:
   
    try:
        format_last_seen_time =  now - timedelta(seconds=Mapi().format_time(l['last-seen'])) 
        format_expires_after = now + timedelta(seconds=Mapi().format_time(l['expires-after'])) 
        format_lease_time = (Mapi().format_time(l['last-seen']) + Mapi().format_time(l['expires-after'])) / 60

        arr.append(
            {'id': l['id'], 
             'address': l['address'],
             'mac-address': l['mac-address'],
             'server': l['server'],
             'время аренды': f'{"%.0f" % format_lease_time} минут',
             'истекает в: ': format_expires_after.strftime("%Y-%m-%d %H:%M"),
             'последняя авторизация:' : format_last_seen_time.strftime("%Y-%m-%d %H:%M"),
            #  'host-name': l['host-name'],
             'status' : l['status']
             })    
    except:
        format_last_seen_time =  now - timedelta(seconds=Mapi().format_time(l['last-seen'])) 
        arr.append(
            {'id': l['id'], 
             'address': l['address'],
             'mac-address': l['mac-address'],
             'server': l['server'],
             'время аренды': '',
             'истекает в: ': '',
             'последняя авторизация:' : format_last_seen_time.strftime("%Y-%m-%d %H:%M"),
             'status' : l['status']
             }) 


for test in arr:
    pprint(test)





# id
# address
# mac-address
# client-id
# address-lists
# server
# dhcp-option
# status
# expires-after
# last-seen
# active-address
# active-mac-address
# active-client-id
# active-server
# host-name
# agent-circuit-id
# agent-remote-id
# radius
# dynamic
# blocked
# disabled
