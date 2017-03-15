import mongo_operation
import mysql_operation as mysql
import user.user_desc as user_desc
import argparse


def processUserByDate(date):
    
    dateList = []
    collectionNames = mongo_operation.getCollectionNamesWithPrefix('Tweets')
    for colName in collectionNames:
        dateList.append(colName[7:])
    
                
    userDesc = user_desc.UserDesc()






    newUsers = []
    
    oldUsers = []
    
    userList = mongo_operation.getUserListByDates(dateList)
    
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
        res = mongo_operation.findWeiboByDateAndUserid(date, userId)
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



    print('insert new users...')
    mysql.insertUsers(newUsers)
    print('update old users...')
    mysql.updateUsers(oldUsers)


def readParamsFromCmd():
    parser = argparse.ArgumentParser(description = "#processUserDataByDate.py")
    parser.add_argument('date', help = 'The date of user to be processed, format is yyyy-mm-dd, e.g. 2017-01-05')
    return parser.parse_args()
        
params = readParamsFromCmd().__dict__


print('start processing user of ' + params['date'] + '...')

processUserByDate(params['date'])

print('processing user of ' + params['date'] + ' complete.')






