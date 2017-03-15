import codecs
import jieba

class SentimentClassification():
    
    def __init__(self, multiOrTwo):
        v = []
        self.multiOrTwo = multiOrTwo
        filename = 'sentiment_classification/lexicons_' + multiOrTwo + '.txt' 
        for line in codecs.open(filename, 'r', 'utf-8'):
            v.append(line.strip().split())
        self.emotion_type ={}
        for i in v:
            self.emotion_type[i[0]] = i[1]


        


    def init_scores(self):
        scores = {}
    
        if self.multiOrTwo == 'multi':
            scores['happy'] = 0.0
            scores['good'] = 0.0
            scores['angry'] = 0.0
            scores['sad'] = 0.0
            scores['fear'] = 0.0
            scores['hate'] = 0.0
            scores['surprised'] = 0.0
            scores['neutral'] = 0.0
        elif self.multiOrTwo == 'two':
            scores['pos'] = 0.0
            scores['neg'] = 0.0
            scores['neutral'] = 0.0
        return scores
        
        
    def getEmotionDist(self, text):
    
    
        words = doc2words(text).split()
        
        scores = self.init_scores()
                
        degree = 0 
        
        for word in words:
            if word in self.emotion_type.keys():
                scores[self.emotion_type[word]] = scores[self.emotion_type[word]] + 1
                if scores[self.emotion_type[word]] > degree:
                    degree = scores[self.emotion_type[word]]
        
        scores = normalize(scores)
        
        return scores, degree
        
    def getEmotion(self, text):
        
        scores, degree = self.getEmotionDist(text)
        
        self.emotion = ''
        tmp = -1
        for e in scores.keys():
            if scores[e] > tmp:
                self.emotion = e
                tmp = scores[e]

        return self.emotion, degree


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
        scores['neutral'] = 100.0
    else:
        for i in scores.keys():
            scores[i] = scores[i] / s * 100
    
    return scores
    
