import codecs
import jieba

import os
import os.path


class TextClassification():
    
    def __init__(self):
        
        
        self.types = set()
        
        self.word_type = {}
        
        for parent,dirnames,filenames in os.walk('text_classification/lexicons/'):
            for filename in filenames:
                typename = (filename.split('.'))[0]
                self.types.add(typename)
                
                fullname = 'text_classification/lexicons/' + filename
                for line in codecs.open(fullname, 'r', 'utf-8'):
                    if len(line.strip()) > 0:
                        self.word_type[line.strip()] = typename
                
    def getTypeDist(self, text):
    
        scores = {}

        for typename in self.types:
            scores[typename] = 0.0

        words = doc2words(text).split()
        
        tmp = set()
                
        for word in words:
            if word in self.word_type.keys():
                scores[self.word_type[word]] = scores[self.word_type[word]] + 1
                tmp.add(word)
        
        scores = normalize(scores)
        
        return scores, tmp
        
    def getType(self, text):
        
        scores, words = self.getTypeDist(text)
        
        self.t = ''
        tmp = -1
        for e in scores.keys():
            if scores[e] > tmp:
                self.t = e
                tmp = scores[e]

        if len(words) < 10:
            self.t = '非突发安全事件'

        return self.t, words



# 中文分词
def doc2words(doc):
    seg = jieba.cut(doc)
    seg = [i.strip() for i in seg if len(i.strip()) > 0]
    return ' '.join(seg)


# 百分数
def normalize(scores):
    
    s = 0.0
    for i in scores.keys():
        s += scores[i]
    if s == 0:
        scores['no'] = 100.0
    else:
        for i in scores.keys():
            scores[i] = scores[i] / s * 100
    
    return scores
    
