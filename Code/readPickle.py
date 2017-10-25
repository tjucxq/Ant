import cPickle

data = cPickle.load(open("shop_history_feature_0801_0824.pkl","rb"))
print data["s_92802"]
