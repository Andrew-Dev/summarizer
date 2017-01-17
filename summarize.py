#summarize.py
#
#Text summarization functionality for the English language
#
#Written by Andrew Arpasi

import re
from stemming.porter2 import stem

class Summarize(object):

    # Splits everything into sentences. Works with english language.
    # Credit: https://stackoverflow.com/questions/4576077/python-split-text-on-sentences
    def split_into_sentences(self,text):
        caps = "([A-Z])"
        prefixes = "(Mr|St|Mrs|Ms|Dr|Sen|Rep|Pres|Prof)[.]"
        suffixes = "(Inc|Ltd|Llc|Jr|Sr|Co)"
        starters = "(Mr|Mrs|Ms|Dr|Sen|Rep|Pres|Prof|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
        months = "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Nov|Dec)"
        acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
        websites = "[.](com|net|org|io|gov)"
        digits = "([0-9])"
        text = " " + text + "  "
        text = text.replace("\n", " ")
        text = re.sub(prefixes, "\\1<prd>", text)
        text = re.sub(websites, "<prd>\\1", text)
        if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
        if "Sen." in text: text = text.replace("Sen.", "Sen")
        if "Rep." in text: text = text.replace("Rep.", "Rep")
        if "a.m." in text: text = text.replace("a.m.", "am")
        if "p.m." in text: text = text.replace("p.m.", "pm")
        text = re.sub("\s" + caps + "[.] ", " \\1<prd> ", text)
        text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
        text = re.sub(acronyms + " " + months, "\\1<stop> \\2", text)
        text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
        text = re.sub(caps + "[.]" + caps + "[.]", "\\1<prd>\\2<prd>", text)
        text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
        text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
        text = re.sub(" " + caps + "[.]", " \\1<prd>", text)
        text = re.sub(" " + months + "[.]", " \\1<prd>", text)
        text = re.sub(r'\([^)]*\)', '', text)
        text = re.sub(digits + "[.]" + digits, "\\1<prd>\\2", text)
        if "”" in text: text = text.replace(".”", "”.")
        if "\"" in text: text = text.replace(".\"", "\".")
        if "!" in text: text = text.replace("!\"", "\"!")
        if "?" in text: text = text.replace("?\"", "\"?")
        text = text.replace(".", ".<stop>")
        text = text.replace("?", "?<stop>")
        text = text.replace("!", "!<stop>")
        text = text.replace("<prd>", ".")
        sentences = text.split("<stop>")
        sentences = sentences[:-1]
        sentences = [s.strip() for s in sentences]
        return sentences

    #determines if the word should be ignored
    def is_noise_word(self,word):
        noiseWordsStr = "about,after,all,also,an,and,another,any,are,as,at,be,because,been,before,being,between,both,but,by,came,can,come,could,did,do,each,for,from,get,got,has,had,he,have,her,here,him,himself,his,how,if,in,into,is,it,like,make,many,me,might,more,most,much,must,my,never,now,of,on,only,or,other,our,out,over,said,same,see,should,since,some,still,such,take,than,that,the,their,them,then,there,these,they,this,those,through,to,too,under,up,very,was,way,we,well,were,what,where,which,while,who,with,would,you,your,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,$,1,2,3,4,5,6,7,8,9,0,_"
        noiseWords = noiseWordsStr.split(",")
        for noise in noiseWords:
            if word.lower() == noise:
                return True
        return False

    #splits words into "tokens" that will have scores
    def split_into_word_tokens(self,text):
        unstemmedWords = text.split(" ")
        words = []
        for unstemmedWord in unstemmedWords:
            if self.is_noise_word(unstemmedWord) != True:
                words.append(stem(re.sub(r'\W+', '', unstemmedWord)))
        return words

    #counts the number of each occurrence in the text
    def score_words(self, words):
        scores = {}
        for word in words:
            scores[word] = 0
        for word in words:
            if (word != '') & self.is_noise_word(word) != True:
                scores[word] += 1
        return scores

    #gets an overall score for a sentence based on it's word scores
    def sentence_score(self, sentence, scores):
        sentenceWords = self.split_into_word_tokens(sentence)
        score = 0
        for word in sentenceWords:
            if self.is_noise_word(word) != True:
                try:
                    score += scores[word]
                except KeyError as e:
                    e
        if sentence.count(',') > 5:
            score *= 0.85
        if len(sentenceWords) <= 6:
            return score / 6
        if "skip ad" in sentence.lower():
            score *= 0.25
        return score

    #applies a different method of scoring along with word frequency
    #https://thetokenizer.com/2013/04/28/build-your-own-summary-tool/
    def apply_intersection_scores(self, sentences, scores, combine):
        intScores = {}
        for s1 in sentences:
            score = 0
            for s2 in sentences:
                if s1 == s2:
                    continue
                set1 = set(s1.split(" "))
                set2 = set(s2.split(" "))
                if(len(set1) + len(set2) == 0):
                    continue
                score += len(set1.intersection(set2)) / ((len(set1) + len(set2)) / 2)
            if combine == True:
                intScores[s1] = score
            else:
                scores[s1] = score
        if combine == True:
            maxScore = intScores[max(intScores, key=intScores.get)]
            for sentence in sentences:
                scores[sentence] *= .65
                scores[sentence] += (intScores[sentence]/maxScore/2)
        return scores


    #creates a dictionary with the scores for all the sentences
    def score_sentences(self, text, wordScores):
        sentences = self.split_into_sentences(text)
        sentenceScores = {}
        for sentence in sentences:
            sentenceScores[sentence] = 0
        for sentence in sentences:
            sentenceScores[sentence] += self.sentence_score(sentence,wordScores)
        maxScore = sentenceScores[max(sentenceScores, key=sentenceScores.get)]
        for sentence in sentences:
            sentenceScores[sentence] /= maxScore
        return sentenceScores

    #summarizes the text into a number of sentences using a certain algorithm
    #Algorithms: 0 - Intersection, 1 - Simple Word Frequency, 2 - Combine Both
    def summarize_text(self, text, numSentences, algorithm):
        wordScores = self.score_words(self.split_into_word_tokens(text))
        scores = {}
        if algorithm > 0:
            scores = self.score_sentences(text, wordScores)
        chronSentences = self.split_into_sentences(text)
        if len(chronSentences) < 3:
            return "Could not summarize. Minimum 3 sentences."
        if algorithm != 1:
            scores = self.apply_intersection_scores(chronSentences, scores, (algorithm != 0))
        else:
            scores[chronSentences[0]] *= 1.2 #slight bias towards 1st sentence for word frequency method
        sortedSentences = sorted(scores, key=scores.get, reverse=True)[0:numSentences]
        for sentence in sortedSentences:
            print("SCORE: %.5f SENTENCE: %s" % (scores[sentence], sentence))
        summary = ""
        for sentence1 in chronSentences:
            for sentence2 in sortedSentences:
                if sentence1 == sentence2:
                    summary += sentence1 + "<<sentence>>"
                    sortedSentences.remove(sentence2)
                    break
        return summary