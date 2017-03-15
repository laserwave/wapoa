# 自媒体舆情分析系统架构

## 算法模块
1.keywords_extraction文件夹 - 关键词、短语的抽取
2.sentiment_classification文件夹下 - 情感分类
3.text_classification文件夹下 - 文本分类
4.user文件夹下 - 用户画像

## 数据库访问模块
1.mongo_operation.py 访问mongo数据库
2.mysql_operation.py 访问mysql数据库

## 主程序样例
1.processAllPastData.py 处理全部现有微博collection（自动检测）以及Information-2016-12-29中的用户
2.processWeiboDataByDate.py 处理微博
example：
python processWeiboDataByDate.py 2017-01-05

3.processUserDataByDate.py 处理用户
example：
python processUserDataByDate.py 2017-01-05

