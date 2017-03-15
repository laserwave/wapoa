import re
import mongo_operation
import mysql_operation as mysql
import keywords_extraction.keywords_extraction as keyword
import text_classification.text_classification as text_classify
import sentiment_classification.sentiment_classification as sentiment
import argparse


def processWeiboByDate(date):
    
	
    mymongo = mongo_operation.MyMongo()

    sencl_two = sentiment.SentimentClassification('two')
    sencl_multi = sentiment.SentimentClassification('multi')
    textcl = text_classify.TextClassification()
    
    
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
    


def readParamsFromCmd():
    parser = argparse.ArgumentParser(description = "#processWeiboDataByDate.py")
    parser.add_argument('date', help = 'The date of weibo to be processed, format is yyyy-mm-dd, e.g. 2017-01-05')
    return parser.parse_args()
        
params = readParamsFromCmd().__dict__


print('start processing weibo of ' + params['date'] + '...')

processWeiboByDate(params['date'])

print('processing weibo of ' + params['date'] + ' complete.')





