import sys
import re

behavior = file("first_round_user_shop_behavior.csv","r")
wifiMap = dict()
lines = behavior.readlines()
for line in lines:
    line = line.strip()
    frags = line.split(",")
    shopId = frags[1]
    wifiList = frags[5].split(";")
    map = dict()
    for wifi in wifiList:
        list = wifi.split("|")
        if len(list) > 2:
            wifi = list[0]
            rank = int(list[1])
            map[wifi] = rank
    if len(map) > 0:
        sortList = sorted(map.items(), key=lambda d:d[1], reverse=True)
        wifi = sortList[0][0]
        if not wifiMap.has_key(wifi):
            wifiMap[wifi] =  dict()
        if not wifiMap[wifi].has_key(shopId):
            wifiMap[wifi][shopId] = 0
        wifiMap[wifi][shopId] += 1
wifi_shop = dict()
for wifi, shopMap in wifiMap.items():
    sortList = sorted(shopMap.items(), key=lambda d:d[1], reverse=True)
    wifi_shop[wifi] = sortList[0][0]
print wifi_shop
evalFile = file("evaluation_public.csv","r")
lines = evalFile.readlines()
output = file("submition10.19_wifi_hottestShop.csv","w")
for line in lines:
    line = line.strip()
    frags = line.split(",")
    rowid = frags[0]
    wifiList = frags[6].split(";")
    map = dict()
    for wifi in wifiList:
        list = wifi.split("|")
        if len(list) > 2:
            wifi = list[0]
            rank = int(list[1])
            map[wifi] = rank
    if len(map) > 0:
        sortList = sorted(map.items(), key=lambda d: d[1], reverse=True)
        wifi = sortList[0][0]
        if wifi_shop.has_key(wifi):
            output.write(rowid+","+wifi_shop[wifi]+"\n")

output.close()