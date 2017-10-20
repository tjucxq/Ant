import sys
import re

import cPickle

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
output = file("submition10.18_hottestShop.csv","w")
for line in lines:
    line = line.strip()
    frags = line.split(",")
    rowid = frags[0]
    mallId = frags[2]
    print mallId
    output.write(rowid+","+resultMap[mallId]+"\n")
output.close()