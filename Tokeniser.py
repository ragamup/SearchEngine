#Author: Raghavender Muppavaram

import os
import re
import platform
from porter_stemmer import PorterStemmer

class Tokeniser:
    

    #Extract terms from the documents in a directory and calculates terms frequency
    
    def tokeniseText(self,doc,isFile,stemFlag):
        stemmer=PorterStemmer();
        tokens=dict();
        stopWords=self.loadStopWords();
        fh=list()    
        if isFile is True:
            fh=open(doc);
        else :
            fh.append(doc)
        for line in fh:        
            line=re.sub('(<.*>)','',line);
            line=re.sub('[^0-9a-zA-Z]+',' ',line);
            line=line.strip().lower();
            words=line.split();
            if stemFlag is True :
                for word in words:
                    if word not in stopWords:
                        word=stemmer.stem(word,0,len(word)-1);
                        if len(word)>1 and word not in stopWords:
                            tokens[word]=tokens.get(word,0)+1;
            else:
                for word in words:
                    if len(word)>1:
                        tokens[word]=tokens.get(word,0)+1;                    
        return tokens
    
    #Loading stop words
    def loadStopWords(self):
        handle=open("stopwords.txt");
        stopWords=list();
        for line in handle:
            stopWords.append(line.rstrip());
        return stopWords
