import mongo_operation
import mysql_operation as mysql
import text_classification.text_classification as text_classify
import sentiment_classification.sentiment_classification as sentiment
import user.user_desc as user_desc

mymongo = mongo_operation.MyMongo()


dateList = []
collectionNames = mymongo.getCollectionNamesWithPrefix('Tweets')
for colName in collectionNames:
    dateList.append(colName[7:])

dateList2 = ['2016-12-29', '2017-03-07']


sencl_two = sentiment.SentimentClassification('two')
sencl_multi = sentiment.SentimentClassification('multi')
textcl = text_classify.TextClassification()


print('processing user info...')


userDesc = user_desc.UserDesc()

newUsers = []

oldUsers = []

userList = mymongo.getUserListByDates(dateList2)

for user in userList:
        
    if '_id' not in user.keys():
        continue
    
    
    
    userId = user['_id']

    city = user['City'] if 'City' in user.keys() else ''
    gender = user['Gender'] if 'Gender' in user.keys() else ''
    nickname = user['NickName'] if 'NickName' in user.keys() else ''
    num_fans = user['Num_Fans'] if 'Num_Fans' in user.keys() else 0
    province = user['Province'] if 'Province' in user.keys() else ''
    signature = user['Signature'] if 'Signature' in user.keys() else ''
    url = user['URL'] if 'URL' in user.keys() else ''
    num_follows = user['Num_Follows'] if 'Num_Follows' in user.keys() else 0
    num_tweets = user['Num_Tweets'] if 'Num_Tweets' in user.keys() else 0
    
    tags = user['Tags'] if 'Tags' in user.keys() else ''
    
    credentials = user['Credentials'] if 'Credentials' in user.keys() else ''
    
    influence = num_fans + num_tweets
    keywords = ''
    
    userWeiboList = []

    
    for date in dateList:
        res = mymongo.findWeiboByDateAndUserid(date, userId)
        for weibo in res:
            userWeiboList.append(weibo)

    
    if len(userWeiboList) > 0:
        doc = ''
        for weibo in userWeiboList:
            doc += weibo['Content'] + ' ' if 'Content' in weibo.keys() else ''
        if len(doc) > 0:
            keywords = userDesc.getRes(doc)

            
    if not mysql.isUserExist(userId):
        newUsers.append((userId, city, gender, nickname, num_fans, province, signature, url, num_follows, num_tweets, influence, tags, keywords, credentials))
    else:
        oldUsers.append((city, gender, nickname, num_fans, province, signature, url, num_follows, num_tweets, influence, tags, keywords, credentials, userId))

    
    if len(newUsers) > 50:
        mysql.insertUsers(newUsers)
        newUsers = []
    if len(oldUsers) > 50:
        mysql.updateUsers(oldUsers)
        oldUsers = []
        
        
        

mysql.insertUsers(newUsers)
mysql.updateUsers(oldUsers)



