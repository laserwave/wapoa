import mongo_operation
import mysql_operation as mysql
import text_classification.text_classification as text_classify
import sentiment_classification.sentiment_classification as sentiment
import math



mymongo = mongo_operation.MyMongo()

# 微信公众号的id列表
col_names = mymongo.db.collection_names()

sencl_two = sentiment.SentimentClassification('two')
sencl_multi = sentiment.SentimentClassification('multi')
textcl = text_classify.TextClassification()




for col_name in col_names:
    
    if col_name == 'wechat_info':
        continue
    
    collection = mymongo.db[col_name]

    # 所有文章阅读总数
    R = 0
    # 所有文章点赞总数
    Z = 0
    # 日期
    dates = set()
    # 文章数
    n = 0
    # 最高阅读数
    Rmax = 0
    # 最高点赞数
    Zmax = 0
    
    
    publicsExist = []
    publicsNotExist = []
    emotions_two = []
    emotions_multi = []
    acticlesExist = []
    acticlesNotExist = []

    name = ''
    for article in collection.find():
        
        # 缺少字段
        if 'col_time' not in article.keys():
            continue
        
        if 'name' not in article.keys():
            continue
        
        if '_id' not in article.keys():
            continue
        
        if 'title' not in article.keys():
            continue
        
        if 'content' not in article.keys():
            continue
        
        if 'readNum' not in article.keys():
            continue
        
        if 'praise_num' not in article.keys():
            continue
        
        if 'date' not in article.keys():
            continue
        
        name = article['name']
        _id = str(article['_id'])
        title = article['title']
        content = article['content']
        read_num = article['readNum']
        praise_num = article['praise_num']
        date = article['date']
        col_time = article['col_time']

        dates.add(date)
        
        n += 1
        
        
        if type(read_num) is str:
            if len(read_num) < 1:
                continue
            if read_num == '100000+':
                read_num = '100000'
                Rmax = 100000
                R += 100000
            else:
                R += (int)(read_num)
                if (int)(read_num) > Rmax:
                    Rmax = (int)(read_num)
                    
            
        elif type(read_num) is list:
            q = 0
            for i in range(0, len(read_num)):
                if len(read_num[i]) < 1:
                    q = 1
                    break
                if read_num[i] == '100000+':
                    read_num[i] = '100000'
                    Rmax = 100000
                else:
                    if (int)(read_num[i]) > Rmax:
                        Rmax = (int)(read_num[i])
                    if i == len(read_num) - 1:
                        R += (int)(read_num[i])
            if q == 1:
                continue
            
            read_num = '|'.join(read_num)
            
            
            
        if type(praise_num) is str:
            if len(praise_num) < 1:
                continue
            if praise_num == '100000+':
                praise_num = '100000'
                Zmax = 100000
                Z += 100000
            else:
                Z += (int)(praise_num)
                if (int)(praise_num) > Zmax:
                    Zmax = (int)(praise_num)
            
        elif type(praise_num) is list:
            q = 0
            for i in range(0, len(praise_num)):
                if len(praise_num[i]) < 1:
                    q = 1
                    break
                if praise_num[i] == '100000+':
                    praise_num[i] = '100000'
                    Zmax = 100000
                else:
                    if (int)(praise_num[i]) > Zmax:
                        Zmax = (int)(praise_num[i])
                    if i == len(praise_num) -1:
                        Z += (int)(praise_num[i])
            if q == 1:
                continue
            praise_num = '|'.join(praise_num)      
            
            
            
        if type(col_time) is str:
            if len(col_time) < 1:
                continue
        elif type(col_time) is list:
            q = 0
            for i in range(0, len(col_time)):
                if len(col_time[i]) < 1:
                    q = 1
                    break
            if q == 1:
                continue
            col_time = '|'.join(col_time)
            
            
        t1, keywords = textcl.getType(content)
            
        if mysql.isArticleExist(_id):
            acticlesExist.append((read_num, praise_num, date,  col_time, t1, _id))
        else:
            acticlesNotExist.append((_id, col_name, title, content, read_num, praise_num, date, col_time, t1))
        
        if 'comment' in article.keys() and len(article['comment']) > 0:
            comments = []
            emotion2comments_two = {}
            emotion2comments_multi = {}

            for i in range(0, len(article['comment'])):
                comment = article['comment'][i]
                content = ''
                for key in comment.keys():
                    if 'content' in key:
                        content = comment[key]
                comments.append(content)
            total_number = len(comments)
            
            for i in range(0, total_number):
                comment = comments[i]
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
                if mysql.isEmotionExist_two(_id, e):
                    continue
                proportion = len(emotion2comments_two[e]) / total_number
                the_comments = emotion2comments_two[e]
                the_comments = sorted(the_comments , key=lambda t:t[1], reverse=1)
                comment1 = the_comments[0][0] if len(the_comments) > 0 else ''
                comment2 = the_comments[1][0] if len(the_comments) > 1 else ''
                comment3 = the_comments[2][0] if len(the_comments) > 2 else ''
                article_id = _id
                emotion_type = e
                emotions_two.append((article_id, emotion_type, proportion, comment1, comment2, comment3))

            for e in emotion2comments_multi.keys():
                if mysql.isEmotionExist_multi(_id, e):
                    continue
                proportion = len(emotion2comments_multi[e]) / total_number
                the_comments = emotion2comments_multi[e]
                the_comments = sorted(the_comments , key=lambda t:t[1], reverse=1)
                comment1 = the_comments[0][0] if len(the_comments) > 0 else ''
                comment2 = the_comments[1][0] if len(the_comments) > 1 else ''
                comment3 = the_comments[2][0] if len(the_comments) > 2 else ''  
                article_id = _id
                emotion_type = e
                emotions_multi.append((article_id, emotion_type, proportion, comment1, comment2, comment3))
                             


    mysql.insertEmotionsTwo(emotions_two)
    mysql.insertEmotionsMulti(emotions_multi)   

            
    
            
    mysql.insertArticles(acticlesNotExist)
    mysql.updateArticles(acticlesExist)
        
    d = len(dates)
    
    if d==0 or n==0:
        WCI = 0.0
    else:
        WCI = 0.8 * (math.log(R/d+1) * 0.4 + math.log(R/n+1) * 0.45 + math.log(Rmax+1) * 0.15)
        WCI += 0.2 * (math.log(10*Z/d+1) * 0.4 + math.log(10*Z/n+1) * 0.45 + math.log(10*Zmax+1) * 0.15)
        WCI = WCI * WCI * 10
    
    
    if mysql.isPublicExist(col_name):
        publicsExist.append((WCI, col_name))
    else:
        publicsNotExist.append((col_name, WCI))

    mysql.insertPublics_WCI(publicsNotExist)
    mysql.updatePublics_WCI(publicsExist)

publics = []  

collection = mymongo.db['wechat_info']

for info in collection.find():

    if '_id' not in info.keys():
            continue

    _id = info['_id']

    function = info['fuction'] if 'fuction' in info.keys() else ''
    
    identify = info['identify'] if 'identify' in info.keys() else ''

    name = info['account_name'] if 'account_name' in info.keys() else ''

    col_time = ''

    if 'col_time' in info.keys():
        
        if type(info['col_time']) is str:
            col_time = info['col_time']
        elif type(info['col_time']) is list:
            col_time = '|'.join(info['col_time'])
    
    articles_ave_month = ''
    if 'articles_ave_month' in info.keys():
        
        if type(info['articles_ave_month']) is str:
            articles_ave_month = info['articles_ave_month']
        elif type(info['articles_ave_month']) is list:
            articles_ave_month = '|'.join(info['articles_ave_month'])
        
        
    readnum_ave = ''
    if 'readnum_ave' in info.keys():
        if type(info['readnum_ave']) is str:
            readnum_ave = info['readnum_ave']
        elif type(info['readnum_ave']) is list:
            readnum_ave = '|'.join(info['readnum_ave'])
            
    sina_id = info['sina_id'] if 'sina_id' in info.keys() else ''
    
        
    publics.append((name, function, identify, col_time, articles_ave_month, readnum_ave, sina_id,  _id))
        
mysql.updatePublics(publics)
        
        
        
        
        

