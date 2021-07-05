from pathlib import Path
import json, os, time, datetime, pytz

path = 'www/hello.html'
#f = open(path, "r")

'''
local = pytz.timezone("America/Los_Angeles")
dt = os.path.getmtime(path)
print(dt)
local = time.ctime(dt)
print(local)
utc = datetime.datetime.fromtimestamp(dt)
print(utc)
local_dt = local.localize(utc, is_dst=None)
utc_dt = local_dt.astimezone(pytz.utc)
print(utc_dt)
'''

'''
local = pytz.timezone("America/Los_Angeles")
dt = os.path.getmtime('www/hello.html')
local_time_string = time.strftime('%Y-%m-%d %H:%M:%S', time.ctime(dt))
naive = datetime.datetime.strptime(local_time_string, "%Y-%m-%d %H:%M:%S")
local_dt = local.localize(naive, is_dst=None)
utc_dt = local_dt.astimezone(pytz.utc)
print(utc_dt)
'''

modTimesinceEpoc = os.path.getmtime(path)
modificationTime = datetime.datetime.utcfromtimestamp(modTimesinceEpoc).strftime('%Y-%m-%d %H:%M:%S')
print("Last Modified Time : ", modificationTime , ' UTC')