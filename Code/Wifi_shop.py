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

inFile = file("first_round_shop_info.csv","r")
lines = inFile.readlines()
mallMap = dict()
for line in lines:
    frags = line.strip().split(",")
    shopId = frags[0]
    mallId = frags[5]
    if not mallMap.has_key(mallId):
        mallMap[mallId] = dict()
    mallMap[mallId][shopId] = 0

user_shop = file("first_round_user_shop_behavior.csv","r")
lines = user_shop.readlines()
shopMap = dict()
for line in lines:
    frags = line.strip().split(",")
    shopId = frags[1]
    if not shopMap.has_key(shopId):
        shopMap[shopId] = 0
    shopMap[shopId] += 1

for mallId, value in mallMap.items():
    for shopId in value.keys():
        mallMap[mallId][shopId] = shopMap[shopId]
resultMap = dict()
for mallId, value in mallMap.items():
    list = sorted(value.items(), key=lambda d:d[1], reverse=True)
    for i in range(len(list)):
        mallMap[mallId][list[i][0]] = 0
    resultMap[mallId] = list[0][0]

evalFile = file("evaluation_public.csv","r")
lines = evalFile.readlines()
output = file("submition10.19_wifi_hottestShop.csv","w")
pre = "1"
for line in lines:
    line = line.strip()
    frags = line.split(",")
    rowid = frags[0]
    mallid = frags[2]
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
            pre = wifi_shop[wifi]
        # else:
        #     output.write(rowid+","+resultMap[mallid]+"\n")

output.close()