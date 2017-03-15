import pymongo
import re
import datetime

class MyMongo():
    
    def __init__(self):
        self.addresses = ['223.3.77.26:20000', '223.3.83.196:20000', '223.3.90.150:20000']
        self.client = pymongo.MongoClient(self.addresses)

    def disconnect(self):
        self.client.close()
    
    ### date:yyyy-mm-dd
    ### 获取某天的全部微博,从三天内的集合中查找
    def getWeiboListByDate(self, d1):
        d1 = datetime.datetime.strptime(d1, "%Y-%m-%d").date()
        d2 = d1 + datetime.timedelta(days=1)
        d3 = d1 + datetime.timedelta(days=2)
        ##########################################################################
#        dates = [d1, d2, d3]
        dates = [d1]
        weiboList = []
        db = self.client["Sina_test"]
    
        for d in dates:
            
            collectionName = 'Tweets-' + str(d)
            
            if collectionName not in db.collection_names():
                continue
            
            weiboCollection = db[collectionName]
        
            for weibo in weiboCollection.find():
                if 'PubTime' not in weibo.keys():
                    continue
                pubTime = weibo['PubTime']
                if len(pubTime) < 1:
                    continue
                if re.match('[0-9]{1,2}分钟前', pubTime):
                    pubTime = str(weibo['ColTime'])
                    pubTime = pubTime.replace('/', '-')
                
                
                t = ((pubTime.split())[0]).strip()
                if not re.match('[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}', t):
                    print(t)
                    continue
                tmp = datetime.datetime.strptime(t, "%Y-%m-%d").date()
                if tmp != d1:
                    continue
                weiboList.append(weibo)
                
        return weiboList
        
        
        
    def getCollectionNamesWithPrefix(self, prefix):
        db = self.client["Sina_test"]
    
        res = []
    
        coll = db.collection_names()
        for c in coll:
            if c[0:len(prefix)] == prefix:
                res.append(c)
        res = sorted(res)
        return res
    
    def getUserListByDate(self, date):
        return self.getUserListByDates([date])
    
    def getUserListByDates(self, dateList):
        db = self.client["Sina_test"]
        
        userList = [] 
    
        for dateString in dateList:
            collectionName = 'Information-' + dateString
            userCollection = db[collectionName]
            for user in userCollection.find():
                userList.append(user)
        return userList
                    
        
    def findWeiboByDateAndUserid(self, date, userId):
        
        res = []
        
        db = self.client["Sina_test"]
    
    
        collectionName = 'Tweets-' + date
        weiboCollection = db[collectionName]
    
    
        for weibo in weiboCollection.find({"ID": userId}):
            res.append(weibo)
            
        return res
        
    def getWeiboCollectionsBydates(self, dateList):
        db = self.client["Sina_test"]
    
        weiboCollections = []
    
        for d in dateList:
            collectionName = 'Tweets-' + str(d)
            weiboCollection = db[collectionName]
            weiboCollections.append(weiboCollection)
        return weiboCollections