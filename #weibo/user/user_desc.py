import jieba
import jieba.analyse
import codecs

class UserDesc():
    def __init__(self):
        self.word2type = {}
        self.words = set()
        
        for line in codecs.open('user/dict.txt', 'r', 'utf-8'):
            c = line.split()
            typename = c[0]
            wordList = c[1:len(c)]
            for word in wordList:
                self.word2type[word] = typename
                self.words.add(word)        
                

    def getRes(self, text):
        word2count = {}

        wordList = [word.strip() for word in jieba.cut(text)]
        
        
        for w in wordList:
            if w in self.words:
                if w in word2count.keys():
                    word2count[w] += 1
                else:
                    word2count[w] = 1
        
        type2words = {}
        
        
        for w in word2count.keys():
            t = self.word2type[w]
            if t in type2words.keys():
                type2words[t].append(w)
            else:
                type2words[t] = [w]

        res = ''
        index = -1
        for typename in type2words.keys():
            index += 1
            if index != 0:
                res += '|'
            res += typename + ':'
            for i in range(0, len(type2words[typename])):
                word =type2words[typename][i]
                if i == 0:
                    res += word
                else:
                    res += ','+word
        return res






