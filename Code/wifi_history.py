#coding=utf-8
import sys
import re
import cPickle
import math
import numpy as np

# features: wifi_tf, wifi_idf, wifi_true, wifi_true_percent, wifi_avg_signal, wifi_signal_std
# wifi_avg_rank, wifi_rank1_percent, wifi_rank2_percent, wifi_rank3_percent,
# wifiFirst_shop1_percent, wifiFirst_shop2_percent, wifiFirst_shop3_percent,
# wifi_shop1_percent, wifi_shop2_percent, wifi_shop3_percent
startTime = "2017-08-00"
endTime = "2017-08-18"
wifi_map = dict()
totalRecord = 0 # num of behavior

def init(wifiId):
    wifi_map[wifiId] = dict()
    wifi_map[wifiId]["wifi_tf"] = 0
    wifi_map[wifiId]["wifi_idf"] = 0.0
    wifi_map[wifiId]["wifi_true"] = 0
    wifi_map[wifiId]["wifi_true_percent"] = 0.0
    wifi_map[wifiId]["wifi_avg_signal"] = -1000
    wifi_map[wifiId]["wifi_signal_std"] = 0
    wifi_map[wifiId]["wifi_signal_list"] = []
    wifi_map[wifiId]["wifi_rank_list"] = []
    wifi_map[wifiId]["wifi_rank"] = dict()
    wifi_map[wifiId]["wifi_avg_rank"] = 30
    wifi_map[wifiId]["wifi_rank1st"] = 0
    wifi_map[wifiId]["wifi_rank2nd"] = 0
    wifi_map[wifiId]["wifi_rank3rd"] = 0
    wifi_map[wifiId]["wifi_rank1st_percent"] = 0.0 #该wifi强度排第一名的percent
    wifi_map[wifiId]["wifi_rank2nd_percent"] = 0.0 #该wifi强度排第二名的percent
    wifi_map[wifiId]["wifi_rank3rd_percent"] = 0.0 #该wifi强度排第三名的percent
    wifi_map[wifiId]["wifi_rank1"] = 30 #该wifi最好的rank排名
    wifi_map[wifiId]["wifi_rank2"] = 30 #该wifi第二好的rank排名
    wifi_map[wifiId]["wifi_rank3"] = 30 #该wifi第三好的rank排名
    wifi_map[wifiId]["wifi_rank1_percent"] = 0.0
    wifi_map[wifiId]["wifi_rank2_percent"] = 0.0
    wifi_map[wifiId]["wifi_rank3_percent"] = 0.0
    wifi_map[wifiId]["wifiFirst_shop"] = dict() #最强wifi对应的shop数量
    wifi_map[wifiId]["wifiFirst_shopTop3"] = [] #最强wifi对应的shop数量， top3
    wifi_map[wifiId]["wifiFirst_totalShop"] = 0 #最强wifi对应的shop总数
    wifi_map[wifiId]["wifiFirst_shopNum"] = 0 #最强wifi对应的shop数量，去重的
    wifi_map[wifiId]["wifi_shop"] = dict() #wifi对应的shop数量
    wifi_map[wifiId]["wifi_shopTop3"] = [] #wifi对应的shop数量， top3
    wifi_map[wifiId]["wifi_totalShop"] = 0 #wifi对应的shop总量
    wifi_map[wifiId]["wifi_shopNum"] = 0


if __name__ == "__main__":
    file = file("../Data/first_round_user_shop_behavior.csv","r")
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        frags = line.split(",")
        if len(frags) < 6:
            continue
        shopId = frags[1]
        time = frags[2]
        if time <= startTime or time >= endTime:
            continue
        wifiList = frags[5].split(";")
        if len(wifiList) < 1:
            continue
        totalRecord += 1
        signal_map = dict()
        flag_map = dict()
        for ele in wifiList:
            wifiInfo = ele.split("|")
            if len(wifiInfo) < 3:
                continue
            wifiId = wifiInfo[0]
            signal = int(wifiInfo[1])
            flag = wifiInfo[2]
            signal_map[wifiId] = signal
            flag_map[wifiId] = flag
        # sort the wifi list based on signal
        signalSorted = sorted(signal_map.items(), key=lambda d:d[1], reverse=True)
        for i in range(len(signalSorted)):
            wifiId = signalSorted[i][0]
            signal = signalSorted[i][1]
            rank = i + 1
            flag = flag_map[wifiId]
            if not wifi_map.has_key(wifiId):
                init(wifiId)
            wifi_map[wifiId]["wifi_tf"] += 1
            if flag == "true":
                wifi_map[wifiId]["wifi_true"] += 1
            wifi_map[wifiId]["wifi_signal_list"].append(signal)
            wifi_map[wifiId]["wifi_rank_list"].append(rank)
            if not wifi_map[wifiId]["wifi_rank"].has_key(rank):
                wifi_map[wifiId]["wifi_rank"][rank] = 0
            wifi_map[wifiId]["wifi_rank"][rank] += 1
            # judge the wifi rank
            if rank == 1:
                wifi_map[wifiId]["wifi_rank1st"] += 1
                if not wifi_map[wifiId]["wifiFirst_shop"].has_key(shopId):
                    wifi_map[wifiId]["wifiFirst_shop"][shopId] = 0
                wifi_map[wifiId]["wifiFirst_shop"][shopId] += 1
                wifi_map[wifiId]["wifiFirst_totalShop"] += 1
            elif rank == 2:
                wifi_map[wifiId]["wifi_rank2nd"] += 1
            elif rank == 3:
                wifi_map[wifiId]["wifi_rank3rd"] += 1

            if not wifi_map[wifiId]["wifi_shop"].has_key(shopId):
                wifi_map[wifiId]["wifi_shop"][shopId] = 0
            wifi_map[wifiId]["wifi_shop"][shopId] += 1
            wifi_map[wifiId]["wifi_totalShop"] += 1

    for wifiId in wifi_map.keys():
        wifi_map[wifiId]["wifi_idf"] = math.log(float(totalRecord)/wifi_map[wifiId]["wifi_tf"])
        wifi_map[wifiId]["wifi_true_percent"] = float(wifi_map[wifiId]["wifi_true"]) / wifi_map[wifiId]["wifi_tf"]
        wifi_map[wifiId]["wifi_avg_signal"] = np.average(wifi_map[wifiId]["wifi_signal_list"])
        wifi_map[wifiId]["wifi_signal_std"] = np.std(wifi_map[wifiId]["wifi_signal_list"])
        wifi_map[wifiId]["wifi_avg_rank"] = np.average(wifi_map[wifiId]["wifi_rank_list"])
        wifi_map[wifiId]["wifi_rank1st_percent"] = float(wifi_map[wifiId]["wifi_rank1st"])/wifi_map[wifiId]["wifi_tf"]  # 该wifi强度排第一名的percent
        wifi_map[wifiId]["wifi_rank2nd_percent"] = float(wifi_map[wifiId]["wifi_rank2nd"])/wifi_map[wifiId]["wifi_tf"]  # 该wifi强度排第二名的percent
        wifi_map[wifiId]["wifi_rank3rd_percent"] = float(wifi_map[wifiId]["wifi_rank3rd"])/wifi_map[wifiId]["wifi_tf"]  #该wifi强度排第三名的percent
        rankSorted = sorted(wifi_map[wifiId]["wifi_rank"].items(), key=lambda d:d[0])
        wifi_map[wifiId]["wifi_rank1"] = rankSorted[0][0]  # 该wifi最好的rank排名
        wifi_map[wifiId]["wifi_rank1_percent"] = float(rankSorted[0][1])/wifi_map[wifiId]["wifi_tf"]
        if len(rankSorted) >= 2:
            wifi_map[wifiId]["wifi_rank2"] = rankSorted[1][0]  # 该wifi第二好的rank排名
            wifi_map[wifiId]["wifi_rank2_percent"] = float(rankSorted[1][1])/wifi_map[wifiId]["wifi_tf"]
        if len(rankSorted) >= 3:
            wifi_map[wifiId]["wifi_rank3"] = rankSorted[2][0]  # 该wifi第三好的rank排名
            wifi_map[wifiId]["wifi_rank3_percent"] = float(rankSorted[2][1])/wifi_map[wifiId]["wifi_tf"]

        wifi_map[wifiId]["wifiFirst_shopNum"] = len(wifi_map[wifiId]["wifiFirst_shop"].keys())
        wifiFirst_shopSorted = sorted(wifi_map[wifiId]["wifiFirst_shop"].items(),key=lambda d:d[1], reverse=True)
        if len(wifiFirst_shopSorted) >=3:
            wifi_map[wifiId]["wifiFirst_shopTop3"] = [wifiFirst_shopSorted[0][0],wifiFirst_shopSorted[1][0],wifiFirst_shopSorted[2][0]]
        else:
            for ele in wifiFirst_shopSorted:
                wifi_map[wifiId]["wifiFirst_shopTop3"].append(ele[0])

        wifi_map[wifiId]["wifi_shopNum"] = len(wifi_map[wifiId]["wifi_shop"].keys())
        wifi_shopSorted = sorted(wifi_map[wifiId]["wifi_shop"].items(), key=lambda d:d[1], reverse=True)
        if len(wifi_shopSorted) >= 3:
            wifi_map[wifiId]["wifi_shopTop3"] = [wifi_shopSorted[0][0], wifi_shopSorted[1][0], wifi_shopSorted[2][0]]
        else:
            for ele in wifi_shopSorted:
                wifi_map[wifiId]["wifi_shopTop3"].append(ele[0])

    output = open("../Feature/wifi_history_feature_0801_0817.pkl", "wb")
    cPickle.dump(wifi_map, output)