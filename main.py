'''
Created on Feb 23, 2017

@author: roadd
'''
import sys
from total_size import total_size
v, e, r, c, x = [None] * 5
videos_sizes = []
endpoints_latency = {}
requests = {}



with file("inputs/me_at_the_zoo.in", "r") as f:
  v, e, r, c, x = map(int,f.readline().split(" "))
  videos_sizes = map(int,f.readline().split(" "))
  for i in range(0, e):
    data_server_latency, cache_servers_connected = map(int,f.readline().split(" "))
    endpoints_latency[i] = {}
    endpoints_latency[i][-1] = data_server_latency
    for j in range(0, cache_servers_connected):
      ecache_id, latency = map(int,f.readline().split(" "))
      endpoints_latency[i][ecache_id] = latency
  
  for i in range(0, r):   
    rv, re, rn = map(int,f.readline().split(" "))
    requests[re] = requests.get(re, False) or {}
    requests[re][rv] = {}
    requests[re][rv][-1] = rn * endpoints_latency[re][-1]
    for (cache_id, latency) in endpoints_latency[re].iteritems():
      if cache_id is -1:
        continue
      requests[re][rv][cache_id] = rn * (endpoints_latency[re][-1] - latency)

# def getValue(key, value):
#   return value
# 
# def getServer(key, value):
#   return sorted(value, key=lambda (k,v): getValue(k, v))
# 
# def sortServers(key, value):
#   return dict(map(lambda (k,v): (k, getServer(k, v)), value.iteritems()))
# 
# requests = dict(map(lambda (k,v): (k, sortServers(k, v)), requests.iteritems()))

print requests
cache_video_value = {}

for i in range(0, c):
  cache_video_value[i] = {}
  for (endpoint, videos) in requests.iteritems():
    for (video_id, request_times) in videos.iteritems():
      for (cache_id, value) in request_times.iteritems():
        if cache_id is not i:
          cache_video_value[i][video_id] = cache_video_value[i].get(video_id, False) or 0
          cache_video_value[i][video_id] += requests[endpoint][video_id][cache_id]
          continue

print cache_video_value