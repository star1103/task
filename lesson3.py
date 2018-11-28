# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 10:37:40 2018

@author: ywm
"""

coordination_source = """
{name:'兰州', geoCoord:[103.73, 36.03]},
{name:'嘉峪关', geoCoord:[98.17, 39.47]},
{name:'西宁', geoCoord:[101.74, 36.56]},
{name:'成都', geoCoord:[104.06, 30.67]},
{name:'石家庄', geoCoord:[114.48, 38.03]},
{name:'拉萨', geoCoord:[102.73, 25.04]},
{name:'贵阳', geoCoord:[106.71, 26.57]},
{name:'武汉', geoCoord:[114.31, 30.52]},
{name:'郑州', geoCoord:[113.65, 34.76]},
{name:'济南', geoCoord:[117, 36.65]},
{name:'南京', geoCoord:[118.78, 32.04]},
{name:'合肥', geoCoord:[117.27, 31.86]},
{name:'杭州', geoCoord:[120.19, 30.26]},
{name:'南昌', geoCoord:[115.89, 28.68]},
{name:'福州', geoCoord:[119.3, 26.08]},
{name:'广州', geoCoord:[113.23, 23.16]},
{name:'长沙', geoCoord:[113, 28.21]},
//{name:'海口', geoCoord:[110.35, 20.02]},
{name:'沈阳', geoCoord:[123.38, 41.8]},
{name:'长春', geoCoord:[125.35, 43.88]},
{name:'哈尔滨', geoCoord:[126.63, 45.75]},
{name:'太原', geoCoord:[112.53, 37.87]},
{name:'西安', geoCoord:[108.95, 34.27]},
//{name:'台湾', geoCoord:[121.30, 25.03]},
{name:'北京', geoCoord:[116.46, 39.92]},
{name:'上海', geoCoord:[121.48, 31.22]},
{name:'重庆', geoCoord:[106.54, 29.59]},
{name:'天津', geoCoord:[117.2, 39.13]},
{name:'呼和浩特', geoCoord:[111.65, 40.82]},
{name:'南宁', geoCoord:[108.33, 22.84]},
//{name:'西藏', geoCoord:[91.11, 29.97]},
{name:'银川', geoCoord:[106.27, 38.47]},
{name:'乌鲁木齐', geoCoord:[87.68, 43.77]},
{name:'香港', geoCoord:[114.17, 22.28]},
{name:'澳门', geoCoord:[113.54, 22.19]}
"""

import re 
city_information = {}

for line in coordination_source.split('\n'):
    if not line.strip() or line.startswith('//'):
        continue
    
    city=re.findall("name:'(\w+)'", line)
    x_y = re.findall("Coord:\[(\d+.\d+),\s(\d+.\d+)\]",line)[0]
    x_y = tuple(map(float, x_y))
    city_information[city[0]] = x_y
    print('\t', city)    
    print('\t', x_y)
city_information

#将经纬度坐标转化为千米
import math
def distance(orgin,destination):
    lat1,lon1 = orgin
    lat2,lon2 = destination
    radius = 6371 #km
    
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d

#计算两个城市之间的距离
def get_city_distance(city1, city2):
    return distance(city_information[city1], city_information[city2])
get_city_distance('广州','上海')

import networkx as nx
cities = city_information.keys()
city_graph = nx.Graph()
city_graph.add_nodes_from (cities)

from collections import defaultdict
threhold = 700

cities_connection = defaultdict(list)

for c in cities:
    for c2 in cities:
        if c == c2 : continue
    if get_city_distance(c,c2) < threhold:
        cities_connection[c].append(c2)
        
cities_connection
cities_connection_graph = nx.Graph(cities_connection)
nx.draw(cities_connection_graph,city_information,with_labels=True,node_size=2)

def get_succssors(froninter,graph):
    return graph[froninter]

def is_goal(node,destination):
    return node == destination

def search_destination(graph,start,get_succssors,is_goal_predicate,strategy_func):
    pathes = [[start]]
    seen = set()
    chosen_pathes = []
    while pathes:
        path = pathes.pop(0)
        frontier = path[-1]
        if frontier in seen : continue
    
        for city in get_succssors(frontier,graph):
            if city in path : continue
            new_path = path + [city]
            pathes.append(new_path)
            if is_goal_predicate(city) : return new_path
    
        pathes = strategy_func(pathes)
        seen.add(frontier)
    return chosen_pathes

pathes = [['杭州', '济南'], ['杭州', '南京'], ['杭州', '合肥'], ['杭州', '南昌'], ['杭州', '福州'], ['杭州', '北京'], ['杭州', '上海'], ['杭州', '天津']]
def sort_pathes(pathes,func):
    return sorted(pathes,key=func)[:beam]

def comprehensive_sort(pathes):
    return sort_pathes(pathes, lambda p: (len(p) + get_path_distance(p)), beam=30)

def mini_change_station(pathes):
    return sort_pathes(pathes, lambda p: len(p), beam=-1)

def min_distance(pathes):
    return sort_pathes(pathes, lambda p:get_path_distance(p), beam=-1)

def most_view(pathes):
    return sor