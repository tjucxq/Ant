#coding=utf-8
import numpy as np
import cPickle
import math

shop2category = dict()
shop2mall = dict()
shop2location = dict()
shop2price = dict()

shopMap = dict() # 记录shop的特征
mallMap = dict() # 记录mall的相关特征

def LoadShopInfo():
    Infile = file("first_round_shop_info.csv", "r")
    lines = Infile.readlines()
    for line in lines:
        line = line.strip()
        frags = line.split(",")
        if len(frags) < 6:
            continue
        shopId = frags[0]
        categoryId = frags[1]
        location1 = float(frags[2])
        location2 = float(frags[3])
        price = int(frags[4])
        mallId = frags[5]
        shop2category[shopId] = categoryId
        shop2mall[shopId] = mallId
        shop2price[shopId] = price
        shop2location[shopId] = [location1, location2]

def init(shopId,mallId,categoryId):
    if not mallMap.has_key(mallId):
        mallMap[mallId] = dict()
        mallMap[mallId]["mall_tf"] = 0
        mallMap[mallId]["shopTrade"] = dict() #在这个mall中，shop的trade分布
        mallMap[mallId]["categoryTrade"] = dict() #在这个mall中，category的trade分布
        mallMap[mallId]["categoryshopTrade"] = dict()
        mallMap[mallId]["categoryshopTrade"][categoryId] = dict() #在这个mall的这个category中，shop的trade分布

    shopMap[shopId] = dict()
    shopMap[shopId]["shop_tf"] = 0
    shopMap[shopId]["shop_percentInMall"] = 0.0
    shopMap[shopId]["shop_rankInMall"] = 1000
    shopMap[shopId]["shop_percentInCat"] = 0.0
    shopMap[shopId]["shop_rankInCat"] = 1000
    shopMap[shopId]["shop_wifilengthList"] = []
    shopMap[shopId]["shop_avg_wifiLength"] = 0
    shopMap[shopId]["shop_1stSignalList"] = []
    shopMap[shopId]["shop_avg_1stSignal"] = -1000
    shopMap[shopId]["shop_std_1stSignal"] = 0.0
    shopMap[shopId]["1stWifi"] = dict()
    shopMap[shopId]["1stWifi_top3List"] = []
    shopMap[shopId]["shop_wifiTrue"] = 0
    shopMap[shopId]["shop_wifiTruePercent"] = 0.0
    shopMap[shopId]["distanceList"] = []
    shopMap[shopId]["shop_avg_distance"] = 0.0
    shopMap[shopId]["time_trade"] = dict()
    shopMap[shopId]["time_top3List"] = []
    shopMap[shopId]["price"] = 0
    shopMap[shopId]["category"] = 0
    shopMap[shopId]["mall"] = 0

def distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1-x2,2) + math.pow(y1-y2,2))

if __name__ == "__main__":
    LoadShopInfo()
    file = file("first_round_user_shop_behavior.csv", "r")
    startTime = "2017-08-00"
    endTime = "2017-09-01"
    lines = file.readlines()
    for line in lines:
        frags = line.strip().split(",")
        if len(frags) < 6:
            continue
        shopId = frags[1]
        time = frags[2]
        if time <= startTime or time >= endTime:
            continue
        x1 = float(frags[3])
        y1 = float(frags[4])
        wifiList = frags[5].split(";")
        mallId = shop2mall[shopId]
        categoryId = shop2category[shopId]
        x2 = shop2location[shopId][0]
        y2 = shop2location[shopId][1]

        if not shopMap.has_key(shopId):
            init(shopId, mallId, categoryId)
        shopMap[shopId]["shop_tf"] += 1

        ## mall feature
        mallMap[mallId]["mall_tf"] += 1
        if not mallMap[mallId]["shopTrade"].has_key(shopId):
            mallMap[mallId]["shopTrade"][shopId] = 0
        mallMap[mallId]["shopTrade"][shopId] += 1
        if not mallMap[mallId]["categoryTrade"].has_key(categoryId):
            mallMap[mallId]["categoryTrade"][categoryId] = 0
        mallMap[mallId]["categoryTrade"][categoryId] += 1
        if not mallMap[mallId]["categoryshopTrade"].has_key(categoryId):
            mallMap[mallId]["categoryshopTrade"][categoryId] = dict()
        if not mallMap[mallId]["categoryshopTrade"][categoryId].has_key(shopId):
            mallMap[mallId]["categoryshopTrade"][categoryId][shopId] = 0
        mallMap[mallId]["categoryshopTrade"][categoryId][shopId] += 1

        ## shop feature
        wifi_signal = dict()
        wifi_flag = dict()
        for wifi in wifiList:
            wifiInfo = wifi.split("|")
            if len(wifiInfo) < 3:
                continue
            wifiId = wifiInfo[0]
            signal = int(wifiInfo[1])
            flag = wifiInfo[2]
            wifi_signal[wifiId] = signal
            wifi_flag[wifiId] = flag
            if flag == "true":
                shopMap[shopId]["shop_wifiTrue"] += 1
        sortedWifi = sorted(wifi_signal.items(), key=lambda d:d[1], reverse=True)
        if len(sortedWifi) > 0:
            wifi = sortedWifi[0][0]
            signal = sortedWifi[0][1]
            shopMap[shopId]["shop_1stSignalList"].append(signal)
            if not shopMap[shopId]["1stWifi"].has_key(wifi):
                shopMap[shopId]["1stWifi"][wifi] = 0
            shopMap[shopId]["1stWifi"][wifi] += 1

        shopMap[shopId]["shop_wifilengthList"].append(len(wifiList))
        dist = distance(x1, y1, x2, y2)
        shopMap[shopId]["distanceList"].append(dist)
        timeId = time.split(" ")[1].split(":")[0]
        if not shopMap[shopId]["time_trade"].has_key(timeId):
            shopMap[shopId]["time_trade"][timeId] = 0
        shopMap[shopId]["time_trade"][timeId] += 1
        shopMap[shopId]["price"] = shop2price[shopId]
        shopMap[shopId]["category"] = categoryId
        shopMap[shopId]["mall"] = mallId

    for shopId in shopMap.keys():
        mallId = shop2mall[shopId]
        categoryId = shop2category[shopId]
        shopMap[shopId]["shop_percentInMall"] = float(shopMap[shopId]["shop_tf"])/mallMap[mallId]["mall_tf"]
        rank = 1
        for k,v in mallMap[mallId]["shopTrade"].items():
            if k != shopId and v > shopMap[shopId]["shop_tf"]:
                rank += 1
        shopMap[shopId]["shop_rankInMall"] = rank
        shopMap[shopId]["shop_percentInCat"] = float(shopMap[shopId]["shop_tf"])/mallMap[mallId]["categoryTrade"][categoryId]
        rank = 1
        for k,v in mallMap[mallId]["categoryshopTrade"][categoryId].items():
            if k != shopId and v > shopMap[shopId]["shop_tf"]:
                rank += 1
        shopMap[shopId]["shop_rankInCat"] = rank
        shopMap[shopId]["shop_avg_wifiLength"] = np.average(shopMap[shopId]["shop_wifilengthList"])
        shopMap[shopId]["shop_avg_1stSignal"] = np.average(shopMap[shopId]["shop_1stSignalList"])
        shopMap[shopId]["shop_std_1stSignal"] = np.std(shopMap[shopId]["shop_1stSignalList"])

        sortedList = sorted(shopMap[shopId]["1stWifi"].items(),key=lambda d:d[1], reverse=True)
        if len(sortedList) >= 3:
            shopMap[shopId]["1stWifi_top3List"] = [sortedList[0][0], sortedList[1][0], sortedList[2][0]]
        else:
            for ele in sortedList:
                shopMap[shopId]["1stWifi_top3List"].append(ele[0])
        shopMap[shopId]["shop_wifiTruePercent"] = float(shopMap[shopId]["shop_wifiTrue"]) / shopMap[shopId]["shop_tf"]
        shopMap[shopId]["shop_avg_distance"] = np.average(shopMap[shopId]["distanceList"])

        sortedList = sorted(shopMap[shopId]["time_trade"].items(), key=lambda d:d[1], reverse=True)
        if len(sortedList) >= 3:
            shopMap[shopId]["time_top3List"] = [sortedList[0][0], sortedList[1][0], sortedList[2][0]]
        else:
            for ele in sortedList:
                shopMap[shopId]["time_top3List"].append(ele[0])

    output = open("shop_history_feature_0801_0831.pkl", "wb")
    cPickle.dump(shopMap, output)

    #cPickle.dump(mallMap, open("ss.pkl", "wb"))
