import cPickle

data = cPickle.load(open("../Feature/shop_history_feature_0801_0824.pkl","rb"))
print data["s_92802"]
