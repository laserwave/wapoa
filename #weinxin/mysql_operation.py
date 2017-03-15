import pymysql.cursors


def getConnection():
    connection = pymysql.connect(host='223.3.77.26',
                             user='root',
                             password='hadoopmysql',
                             db='weixin',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    return connection

def isPublicExist(_id):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT count(*) FROM `weixin_public` where _id = %s"
            cursor.execute(sql, _id)
            result = cursor.fetchone()
            if result['count(*)'] > 0:
                return True
            else:
                return False
    finally:
        connection.close()

def insertPublics_WCI(publics):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO `weixin_public` (`_id`, `WCI`) VALUES (%s, %s)"
            cursor.executemany(sql, publics)
        connection.commit()
    finally:
        connection.close()

def updatePublics_WCI(publics):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "update weixin_public set WCI = %s where _id = %s"
            cursor.executemany(sql, publics)
        connection.commit()
    finally:
        connection.close()
        

def updatePublics(publics):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "update weixin_public set public_name = %s, function = %s, identify = %s, col_time = %s, articles_ave_month = %s, readnum_ave = %s, sina_id = %s  where _id = %s"
            cursor.executemany(sql, publics)
        connection.commit()
    finally:
        connection.close()


def isArticleExist(_id):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT count(*) FROM `article` where _id = %s"
            cursor.execute(sql, _id)
            result = cursor.fetchone()
            if result['count(*)'] > 0:
                return True
            else:
                return False
    finally:
        connection.close()
		
		
def insertArticles(articles):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO `article` (`_id`, `public_id`, `title`, `content`, `read_num`, `praise_num`, `date`, `col_time`, `tag`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, articles)
        connection.commit()
    finally:
        connection.close()
		
def updateArticles(articles):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "update article set read_num = %s, praise_num = %s, date = %s, col_time = %s, tag = %s where _id = %s"
            cursor.executemany(sql, articles)
        connection.commit()
    finally:
        connection.close()

def isEmotionExist_two(article_id, emotion):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT count(*) FROM `emotion_two` where article_id = %s and emotion_type = %s"
            cursor.execute(sql, (article_id, emotion))
            result = cursor.fetchone()
            if result['count(*)'] > 0:
                return True
            else:
                return False
    finally:
        connection.close()
        
def isEmotionExist_multi(article_id, emotion):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT count(*) FROM `emotion_multi` where article_id = %s and emotion_type = %s"
            cursor.execute(sql, (article_id, emotion))
            result = cursor.fetchone()
            if result['count(*)'] > 0:
                return True
            else:
                return False
    finally:
        connection.close()

        
def insertEmotionsTwo(emotions):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `emotion_two` (`article_id`, `emotion_type`, `proportion`, `comment1`, `comment2`, `comment3`) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, emotions)
        connection.commit()
    finally:
        connection.close()
        
def insertEmotionsMulti(emotions):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `emotion_multi` (`article_id`, `emotion_type`, `proportion`, `comment1`, `comment2`, `comment3`) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, emotions)
        connection.commit()
    finally:
        connection.close()

		
		
		

