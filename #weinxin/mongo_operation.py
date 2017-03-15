import pymongo
import re
import time
import datetime

class MyMongo():
    
    def __init__(self):
        self.addresses = ['223.3.77.26:20000', '223.3.83.196:20000', '223.3.90.150:20000']
        self.client = pymongo.MongoClient(self.addresses)
        self.db = self.client["wechat_data"]

    def disconnect(self):
        self.client.close()

