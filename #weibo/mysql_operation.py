import pymysql.cursors


def getConnection():
    connection = pymysql.connect(host='223.3.77.26',
                             user='root',
                             password='hadoopmysql',
                             db='weibo',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    return connection

#def getConnection():
#    connection = pymysql.connect(host='localhost',
#                             user='root',
#                             password='118174',
#                             db='weibodb',
#                             charset='utf8mb4',
#                             cursorclass=pymysql.cursors.DictCursor)
#    return connection

def getEvent(name):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `weibo_event` where name = %s"
            cursor.execute(sql, name)
            event = cursor.fetchone()
            return event
    finally:
        connection.close()

def isWeiboExist(_id):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT count(*) FROM `weibo_content` where _id = %s"
            cursor.execute(sql, _id)
            result = cursor.fetchone()
            if result['count(*)'] > 0:
                return True
            else:
                return False
    finally:
        connection.close()
        
def isEventExist(name):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT count(*) FROM `weibo_event` where name = %s"
            cursor.execute(sql, name)
            result = cursor.fetchone()
            if result['count(*)'] > 0:
                return True
            else:
                return False
    finally:
        connection.close()
    
def updateEvents(events):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "update weibo_event set recent_time = %s, hot = %s, max_hot = %s where name = %s"
            cursor.executemany(sql, events)
        connection.commit()

    finally:
        connection.close()
        

            
def insertEvents(events):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO `weibo_event` (`name`, `tag`, `start_time`, `hot`, `keywords`, `recent_time`, `max_hot`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, events)
    
        connection.commit()
    finally:
        connection.close()
        
def insertWeibos(contents):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO `weibo_content` (`comment`, `transfer`, `ID`, `praise`, `pubtime`, `tools`, `content`, `_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, contents)
        connection.commit()
    
    finally:
        connection.close()
        
def insertContentEvent(contentEvents):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO `content_event` (`content_id`, `event_id`) VALUES (%s, %s)"
            cursor.executemany(sql, contentEvents)
        connection.commit()
    
    finally:
        connection.close()
      
        
def insertWeiboEmotionsTwo(emotions):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO `emotion_two` (`weibo_id`, `emotion_type`, `proportion`, `comment1`, `comment2`, `comment3`, `_date`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, emotions)
        connection.commit()
    
    finally:
        connection.close()   
        
def insertWeiboEmotionsMulti(emotions):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO `emotion_multi` (`weibo_id`, `emotion_type`, `proportion`, `comment1`, `comment2`, `comment3`, `_date`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, emotions)
        connection.commit()
    finally:
        connection.close()
        
        
def insertEventEmotionsTwo(emotions):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO `emotion_two` (`event_id`, `emotion_type`, `proportion`, `comment1`, `comment2`, `comment3`, `_date`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, emotions)
        connection.commit()
    
    finally:
        connection.close()  
     
        
def insertEventEmotionsMulti(emotions):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO `emotion_multi` (`event_id`, `emotion_type`, `proportion`, `comment1`, `comment2`, `comment3`, `_date`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, emotions)
        connection.commit()
    finally:
        connection.close()  
        
        
def insertUsers(users):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO `weibo_user` (`_id`, `city`, `gender`, `nickname`, `num_fans`, `province`, `signature`, `url`, `num_follows`, `num_tweets`, `influence`, `tags`, `keywords`, `credentials`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, users)
        connection.commit()
    
    finally:
        connection.close()   
    


def isUserExist(_id):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT count(*) FROM `weibo_user` where _id = %s"
            cursor.execute(sql, _id)
            result = cursor.fetchone()
            if result['count(*)'] > 0:
                return True
            else:
                return False
    finally:
        connection.close()
        
        
def updateUsers(users):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "update weibo_user set city = %s, gender = %s, nickname = %s, num_fans = %s, province = %s, signature = %s, url = %s, num_follows = %s, num_tweets = %s, influence = %s, tags = %s, keywords = %s,  credentials = %s where _id = %s"
            cursor.executemany(sql, users)
        connection.commit()
    finally:
        connection.close()

        
# 某个微博某种情感是否存在（两类）
def isEmotionExist_two_weibo(weibo_id, emotion):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT count(*) FROM `emotion_two` where weibo_id = %s and emotion_type = %s"
            cursor.execute(sql, (weibo_id, emotion))
            result = cursor.fetchone()
            if result['count(*)'] > 0:
                return True
            else:
                return False
    finally:
        connection.close()

# 某个微博某种情感是否存在（多类）
def isEmotionExist_multi_weibo(weibo_id, emotion):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT count(*) FROM `emotion_multi` where weibo_id = %s and emotion_type = %s"
            cursor.execute(sql, (weibo_id, emotion))
            result = cursor.fetchone()
            if result['count(*)'] > 0:
                return True
            else:
                return False
    finally:
        connection.close()        

# 某个事件某种情感是否存在（两类）
def isEmotionExist_two_event(event_id, emotion):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT count(*) FROM `emotion_two` where event_id = %s and emotion_type = %s"
            cursor.execute(sql, (event_id, emotion))
            result = cursor.fetchone()
            if result['count(*)'] > 0:
                return True
            else:
                return False
    finally:
        connection.close()

# 某个事件某种情感是否存在（多类）
def isEmotionExist_multi_event(event_id, emotion):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT count(*) FROM `emotion_multi` where event_id = %s and emotion_type = %s"
            cursor.execute(sql, (event_id, emotion))
            result = cursor.fetchone()
            if result['count(*)'] > 0:
                return True
            else:
                return False
    finally:
        connection.close()