import jieba
import jieba.analyse
import re
import codecs

def extractKeywords(text):
    stopwords = [line.strip() for line in codecs.open('keywords_extraction/stopwords.txt', 'r', 'utf-8') if len(line.strip()) > 0]
    # 设置停用词
    jieba.analyse.set_stop_words('keywords_extraction/stopwords.txt')
    
    # 抽取关键词,此处是tfidf抽取的关键词,根据这些关键词提取出关键短语,再整合
    words_score = jieba.analyse.extract_tags(text, topK=30, withWeight=True)
    words = [pair[0] for pair in words_score]
    
    keywords2score = {}
    for i in words_score:
        if i not in stopwords:
            keywords2score[i[0]] = i[1]
    
    # 分词
    seg = jieba.cut(text)
    sent = [w for w in seg]
    
    # 候选短语
    s = []
    phrase2count = {}
    phrase2list = {}
    
    # 连续出现的两个关键词加入候选的关键短语
    # 连续的三个词，只要两边都是关键词，加入候选短语
    for i in range(0, len(sent)):
        if sent[i] in words:
            if i+1<len(sent) and sent[i+1] in words:
                phrase = []
                phrase.append(sent[i])
                phrase.append(sent[i+1])
                s.append(phrase)
                phrase_s = ''.join(phrase)
                if len(phrase_s) > 6:
                    continue
                
                if phrase_s not in phrase2list:
                    phrase2list[phrase_s] = phrase
                if phrase_s in phrase2count:
                    phrase2count[phrase_s] = phrase2count[phrase_s] + 1
                else:
                    phrase2count[phrase_s] = 1
            if i+2<len(sent) and sent[i+2] in words:
                phrase = []
                phrase.append(sent[i])
                phrase.append(sent[i+1])
                phrase.append(sent[i+2])
                s.append(phrase)
                phrase_s = ''.join(phrase)
                if len(phrase_s) > 6:
                    continue
                if phrase_s not in phrase2list:
                    phrase2list[phrase_s] = phrase
                if phrase_s in phrase2count:
                    phrase2count[phrase_s] = phrase2count[phrase_s] + 1
                else:
                    phrase2count[phrase_s] = 1
    
    # 去除出现次数少于3次的候选短语
    # 去除同时包含数字字母和汉字的候选短语
    phrases = [i for i in phrase2count.keys() if phrase2count[i] >= 3 and not (re.search('[0-9a-zA-Z]', i) and re.search('[\u4e00-\u9fa5]', i)) or re.match('[0-9a-zA-Z]+-[0-9a-zA-Z]+', i)]
    
    # 去除是其他关键短语子串的关键短语
    tmp = []
    for p1 in phrases:
        flag = True
        for p2 in phrases:
            if p1 != p2 and p1 in p2:
                flag = False
                break
        if flag:
            tmp.append(p1)
    
    phrases = tmp
    
    
    # 关键短语的打分为组成的关键词中打分较大值
    phrase2score = {}
    for phrase in phrases:
        phrase_list = phrase2list[phrase]
        score = 0
        for i in phrase_list:
            if i in keywords2score:
                score = max(keywords2score[i], score)
        phrase2score[phrase] = score
    
    # 关键词与关键短语
    keywords = []
    
    # 去除出现在关键短语中的关键词
    # 去除此时的所有数字串（可能在之前与字母组成关键短语，故不能在前面去除）
    for phrase in phrase2score:
        if not re.match('[0-9]+', phrase):
            keywords.append((phrase, phrase2score[phrase]))
            
    for pair in words_score:
        word = pair[0]
        flag = False
        for phrase in phrases:
            phrase_list = phrase2list[phrase]
            for i in phrase_list:
                if word == i:
                    flag = True
                    break
            if flag:
                break
        if not flag and not re.match('[0-9]+', word):
            keywords.append(pair)
    
    #  按评分排序
    keywords = sorted(keywords, key=lambda t:t[1], reverse=True)
    
    if len(keywords) < 1:
        return ''
    
    # 评分归一化
    base = keywords[0][1]
    for i in range(0, len(keywords)):
        keywords[i] = (keywords[i][0], 1/base*keywords[i][1])

    
    final_keywords = []
    
    count = 0
    i = 0
    while count < 10 and i < len(keywords):
        if keywords[i][0] not in stopwords and len(keywords[i][0]) < 7:
            final_keywords.append(keywords[i][0])
            count += 1
        i += 1

    return '|'.join(final_keywords)



