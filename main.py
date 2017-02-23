'''
Created on Feb 23, 2017

@author: roadd
'''
import sys
v, e, r, c, x = [None] * 5
videos_sizes = []
endpoints_latency = {}
requests = {}

name = "kittens"

with file("inputs/"+name+".in", "r") as f:
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
    requests[re][rv][-1] = 0
    for (cache_id, latency) in endpoints_latency[re].iteritems():
      if cache_id is -1:
        continue
      requests[re][rv][cache_id] = rn * (endpoints_latency[re][-1] - latency)

cache_video_value = {}

for i in range(0, c):
  for (endpoint, videos) in requests.iteritems():
    for (video_id, request_times) in videos.iteritems():
      cache_video_value[video_id] = cache_video_value.get(video_id, False) or {}
      for (cache_id, value) in request_times.iteritems():
        if cache_id is not i:
          cache_video_value[video_id][i] = cache_video_value[video_id].get(i, False) or 0
          cache_video_value[video_id][i] += requests[endpoint][video_id][cache_id]
          continue

cached_videos = {}
for i in range(0, v):
  while any(value > 0 for value in cache_video_value.get(i, {-1: 0}).values()):
    max_index = max(cache_video_value[i], key=cache_video_value[i].get)
    cached_videos[max_index] = cached_videos.get(max_index, False) or []
    if videos_sizes[i] + sum(map(lambda v: videos_sizes[v], cached_videos[max_index])) < x:
      cached_videos[max_index].append(i)
    cache_video_value[i][max_index] = 0
    for j in range(0, e):
      for (key, val) in cache_video_value.iteritems():
        if key is not max_index and cache_video_value[i].get(key, False) and requests.get(j, False):
          if not requests[j].get(i, False):
            continue
          if not requests[j][i].get(key, False):
            continue
          cache_video_value[i][key] -= requests[j][i][key]

target = open("outputs/"+name+".in", 'w')
target.write(str(len(cached_videos)))
target.write("\n")
for key, value in cached_videos.iteritems():
  target.write(str(key))
  for i in value:
    target.write(" "+str(i))
  target.write("\n")