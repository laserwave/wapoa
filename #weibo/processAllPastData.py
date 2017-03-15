import re
import mongo_operation
import mysql_operation as mysql
import keywords_extraction.keywords_extraction as keyword
import text_classification.text_classification as text_classify
import sentiment_classification.sentiment_classification as sentiment
import time
import user.user_desc as user_desc

mymongo = mongo_operation.MyMongo()


dateList = ['2016-11-22']
#dateList = ['2017-01-07', '2017-01-08', '2017-01-09', '2017-01-10']
#dateList = []
#collectionNames = mongo_operation.getCollectionNamesWithPrefix('Tweets')
#for colName in collectionNames:
#    dateList.append(colName[7:])

dateList2 = ['2016-12-29']


sencl_two = sentiment.SentimentClassification('two')
sencl_multi = sentiment.SentimentClassification('multi')
textcl = text_classify.TextClassification()


t1 = time.time()

for date in dateList:
    
    print('processing weibo of ' + date + '...')
    
    weiboThisDay = mymongo.getWeiboListByDate(date)

    oldEvents = []
    newEvents = []
    
    ### 统计每个话题出现次数并排序
    # 每个话题计数
    hashtag2score = {}
    # 包含hashtag的微博
    hashtag2weibo = {}

    hashtag2eventid = {}

    weiboid2hashtag = {}

    for i in range(0, len(weiboThisDay)):
        
        weibo = weiboThisDay[i]
        pattern = re.compile('#.+?#')
        res = pattern.findall(weiboThisDay[i]['Content'])
        for j in range(0, len(res)):
            res[j] = res[j][1:len(res[j])-1]

            score = weibo['CommentNum'] + weibo['TransferNum'] + weibo['Like']
            if score < 100:
                continue

            if res[j] not in hashtag2score.keys():
                hashtag2score[res[j]] = 0
            hashtag2score[res[j]] += score
    
            

            _id = weibo['_id']

            weiboid2hashtag[_id] = res[j]

            if res[j] in hashtag2weibo.keys():
                hashtag2weibo[res[j]].append(weibo)
            else:
                hashtag2weibo[res[j]] = [weibo]
  
    


    hashtag2keywords = {}
    hashtag2tag = {}

    for hashtag in hashtag2score.keys():
        score = hashtag2score[hashtag]

        if score < 1000:
            continue
        
        relatedWeiboList = hashtag2weibo[hashtag]



        if not mysql.isEventExist(hashtag):
            text = ''
            for weibo in relatedWeiboList:
                text += weibo['Content'] + ' '
            text = text.replace('#', ' ')
            hashtag2keywords[hashtag] = keyword.extractKeywords(text)
            hashtag2tag[hashtag], keywordsList = textcl.getType(text)
            hot = date + ':' + str(score)
            newEvents.append((hashtag, hashtag2tag[hashtag], date, hot, hashtag2keywords[hashtag], date, score))
            
        else:
            event = mysql.getEvent(hashtag)
            hot = event['hot']
            hot += '|' + date + ':' + str(score)
            tmp = [(a.split(':'))[1] for a in hot.split('|')]
            max_hot = 0.0
            for i in tmp:
                max_hot = max(max_hot, float(i))
            oldEvents.append((date, hot, max_hot, hashtag))

    print('insert new events...')
    print(len(newEvents))
    mysql.insertEvents(newEvents)
    print('update old events...')
    print(len(oldEvents))
    mysql.updateEvents(oldEvents)
    
    ### 存weibo_content,content_event
    contents = []
    

    for hashtag in hashtag2score.keys():
        
        score = hashtag2score[hashtag]
        if score < 1000:
            continue
                
        relatedWeiboList = hashtag2weibo[hashtag]
    
        for weibo in relatedWeiboList:
            comment = weibo['CommentNum'] if 'CommentNum' in weibo.keys() else 0
            transfer = weibo['TransferNum'] if 'TransferNum' in weibo.keys() else 0
            ID = weibo['ID']
            praise = weibo['Like'] if 'Like' in weibo.keys() else 0
            pubtime = weibo['PubTime'] if 'PubTime' in weibo.keys() else ''
            tools = weibo['Tools'] if 'Tools' in weibo.keys() else ''
            content = weibo['Content'] if 'Content' in weibo.keys() else ''
            _id = weibo['_id']
            contents.append((comment, transfer, ID, praise, pubtime, tools, content, _id))
    print('insert weibos...')
    mysql.insertWeibos(contents)

    
    content_events = []
    
    for hashtag in hashtag2score.keys():
        event = mysql.getEvent(hashtag)
        
        if event is None:
            continue
        
        eventId = event['_id']
        hashtag2eventid[hashtag] = eventId

    for weiboId in weiboid2hashtag.keys():
        if weiboid2hashtag[weiboId] in hashtag2eventid.keys():
            
            event = mysql.getEvent(weiboid2hashtag[weiboId])
        
            if event is None:
                continue
            if not mysql.isWeiboExist(weiboId):
                continue
            content_events.append((weiboId, hashtag2eventid[weiboid2hashtag[weiboId]]))
            
            
    mysql.insertContentEvent(content_events)
    
    
    
    ### 微博情感
    emotions_two_weibo = []
    emotions_multi_weibo = []

    emotions_two_event = []
    emotions_multi_event = []

    
    for hashtag in hashtag2score.keys():
        
        score = hashtag2score[hashtag]
        if score < 1000:
            continue
                
        relatedWeiboList = hashtag2weibo[hashtag]
    
    
        for weibo in relatedWeiboList:
            if 'Comments' not in weibo.keys() or len(weibo['Comments']) < 1:
                continue
            comments = weibo['Comments']
            
            emotion2comments_two = {}
            emotion2comments_multi = {}
            # 一条微博的评论数
            total_number = len(comments)
            
            for i in range(0, total_number):
                comment = comments[i]['Content']
                e, d = sencl_two.getEmotion(comment)
                if e in emotion2comments_two.keys():
                    emotion2comments_two[e].append((comment, d))
                else:
                    tmp = []
                    tmp.append((comment, d))
                    emotion2comments_two[e] = tmp

                e, d = sencl_multi.getEmotion(comment)
                if e in emotion2comments_multi.keys():
                    emotion2comments_multi[e].append((comment, d))
                else:
                    tmp = []
                    tmp.append((comment, d))
                    emotion2comments_multi[e] = tmp


            for e in emotion2comments_two.keys():
                if mysql.isEmotionExist_two_weibo(weibo['_id'], e):
                    continue
                weibo_id = weibo['_id']
                proportion = len(emotion2comments_two[e]) / total_number
                the_comments = emotion2comments_two[e]
                the_comments = sorted(the_comments , key=lambda t:t[1], reverse=1)
                comment1 = the_comments[0][0] if len(the_comments) > 0 else ''
                comment2 = the_comments[1][0] if len(the_comments) > 1 else ''
                comment3 = the_comments[2][0] if len(the_comments) > 2 else ''
                emotion_type = e
                emotions_two_weibo.append((weibo_id, emotion_type, proportion, comment1, comment2, comment3, date))

            for e in emotion2comments_multi.keys():
                if mysql.isEmotionExist_multi_weibo(weibo['_id'], e):
                    continue
                weibo_id = weibo['_id']
                proportion = len(emotion2comments_multi[e]) / total_number
                the_comments = emotion2comments_multi[e]
                the_comments = sorted(the_comments , key=lambda t:t[1], reverse=1)
                comment1 = the_comments[0][0] if len(the_comments) > 0 else ''
                comment2 = the_comments[1][0] if len(the_comments) > 1 else ''
                comment3 = the_comments[2][0] if len(the_comments) > 2 else ''  
                emotion_type = e
                emotions_multi_weibo.append((weibo_id, emotion_type, proportion, comment1, comment2, comment3, date))
                
                
                
                
                
    
        
                
    ### 事件情感
    for hashtag in hashtag2score.keys():
        
        
        score = hashtag2score[hashtag]
        if score < 1000:
            continue
        
        event = mysql.getEvent(hashtag)
        if event is None:
            continue
        eventId = event['_id']
                
        relatedWeiboList = hashtag2weibo[hashtag]
    
        commentsList = []
    
        for weibo in relatedWeiboList:
            if 'Comments' not in weibo.keys() or len(weibo['Comments']) < 1:
                continue
            comments = weibo['Comments']
            for comment in comments:
                commentsList.append(comment)
                
        emotion2comments_two = {}
        emotion2comments_multi = {}
        # 所有微博总评论数
        total_number = len(commentsList)
        
        for i in range(0, total_number):
            comment = commentsList[i]['Content']
            e, d = sencl_two.getEmotion(comment)
            if e in emotion2comments_two.keys():
                emotion2comments_two[e].append((comment, d))
            else:
                tmp = []
                tmp.append((comment, d))
                emotion2comments_two[e] = tmp

            e, d = sencl_multi.getEmotion(comment)
            if e in emotion2comments_multi.keys():
                emotion2comments_multi[e].append((comment, d))
            else:
                tmp = []
                tmp.append((comment, d))
                emotion2comments_multi[e] = tmp


        for e in emotion2comments_two.keys():
            if mysql.isEmotionExist_two_event(eventId, e):
                continue
            proportion = len(emotion2comments_two[e]) / total_number
            the_comments = emotion2comments_two[e]
            the_comments = sorted(the_comments , key=lambda t:t[1], reverse=1)
            comment1 = the_comments[0][0] if len(the_comments) > 0 else ''
            comment2 = the_comments[1][0] if len(the_comments) > 1 else ''
            comment3 = the_comments[2][0] if len(the_comments) > 2 else ''
            emotion_type = e
            emotions_two_event.append((eventId, emotion_type, proportion, comment1, comment2, comment3, date))

        for e in emotion2comments_multi.keys():
            if mysql.isEmotionExist_multi_weibo(weibo['_id'], e):
                continue
            proportion = len(emotion2comments_multi[e]) / total_number
            the_comments = emotion2comments_multi[e]
            the_comments = sorted(the_comments , key=lambda t:t[1], reverse=1)
            comment1 = the_comments[0][0] if len(the_comments) > 0 else ''
            comment2 = the_comments[1][0] if len(the_comments) > 1 else ''
            comment3 = the_comments[2][0] if len(the_comments) > 2 else ''  
            emotion_type = e
            emotions_multi_event.append((eventId, emotion_type, proportion, comment1, comment2, comment3, date))      
          
                
    print('insert weibo emotions...')
    mysql.insertWeiboEmotionsTwo(emotions_two_weibo)
    mysql.insertWeiboEmotionsMulti(emotions_multi_weibo)
    print('insert event emotions...')
    mysql.insertEventEmotionsTwo(emotions_two_event)
    mysql.insertEventEmotionsMulti(emotions_multi_event)
    


t2 = time.time()
print('processing weibo cost ' + str(t2-t1) + ' seconds.')



#
#print('processing user info...')
#
#
#userDesc = user_desc.UserDesc()
#
#newUsers = []
#
#oldUsers = []
#
#userList = mymongo.getUserListByDates(dateList2)
#
#for user in userList:
#        
#    if '_id' not in user.keys():
#        continue
#    
#    
#    
#    userId = user['_id']
#
#    city = user['City'] if 'City' in user.keys() else ''
#    gender = user['Gender'] if 'Gender' in user.keys() else ''
#    nickname = user['NickName'] if 'NickName' in user.keys() else ''
#    num_fans = user['Num_Fans'] if 'Num_Fans' in user.keys() else 0
#    province = user['Province'] if 'Province' in user.keys() else ''
#    signature = user['Signature'] if 'Signature' in user.keys() else ''
#    url = user['URL'] if 'URL' in user.keys() else ''
#    num_follows = user['Num_Follows'] if 'Num_Follows' in user.keys() else 0
#    num_tweets = user['Num_Tweets'] if 'Num_Tweets' in user.keys() else 0
#    
#    tags = user['Tags'] if 'Tags' in user.keys() else ''
#    
#    credentials = user['Credentials'] if 'Credentials' in user.keys() else ''
#    
#    influence = num_fans + num_tweets
#    keywords = ''
#    
#    userWeiboList = []
#
#    
#    for date in dateList:
#        res = mymongo.findWeiboByDateAndUserid(date, userId)
#        for weibo in res:
#            userWeiboList.append(weibo)
#
#    
#    if len(userWeiboList) > 0:
#        doc = ''
#        for weibo in userWeiboList:
#            doc += weibo['Content'] + ' ' if 'Content' in weibo.keys() else ''
#        if len(doc) > 0:
#            keywords = userDesc.getRes(doc)
#
#            
#    if not mysql.isUserExist(userId):
#        newUsers.append((userId, city, gender, nickname, num_fans, province, signature, url, num_follows, num_tweets, influence, tags, keywords, credentials))
#    else:
#        oldUsers.append((city, gender, nickname, num_fans, province, signature, url, num_follows, num_tweets, influence, tags, keywords, credentials, userId))
#
#
#
#print('insert new users...')
#mysql.insertUsers(newUsers)
#print('update old users...')
#mysql.updateUsers(oldUsers)
#
#
#t3 = time.time()
#print('processing users cost ' + str(t3-t2) + ' seconds.')

