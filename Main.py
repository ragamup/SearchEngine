'''
Created on April 28, 2017

@author: Raghavender
'''

from __future__ import division
import platform
import os
import math
import pickle
from Tokeniser import Tokeniser
import collections
import sqlite3

#Path for documents dataset
class search:
    

    def invertIndexDocs(self):
        pkl_file = open('unt_index.pkl', 'rb')
        inverted_index = pickle.load(pkl_file)
        return inverted_index;
    
    def calulateDocLens(self,invertIndexDict):
        docLens=dict();
        for docList in invertIndexDict.values():
            idf=docList[0];
            for doc,tf in docList[1].items():
                docLens[doc]=docLens.get(doc,0)+math.pow(idf*tf,2);
    
        for doc,idfs in docLens.items():
            docLens[doc]=math.sqrt(idfs);
        return docLens;
    
    def retrievalDocsOnQuery(self,query,invertedIndex):
        queryWords=Tokeniser().tokeniseText(query, False, True);
        simTable=dict();
        queryLength=0;
        maxTF=1;
        if len(queryWords)>=1:
            maxTF=self.topNWordsinVocab(queryWords, 1).popitem()[1];
        for qWord, qWordLen in queryWords.items():
            #idf=0
            if qWord in invertedIndex.keys():
                qWordLen=qWordLen/maxTF;
                idf=invertedIndex[qWord][0];
                docList=invertedIndex[qWord][1];
                queryLength=queryLength+math.pow(idf*qWordLen,2);
                for doc, tf in docList.items():
                    simTable[doc]=simTable.get(doc,0)+(tf*idf)*(qWordLen*idf);
        queryLength=math.sqrt(queryLength);
        docLenTable=self.calulateDocLens(invertedIndex);
        for doc in simTable.keys():
            docLen=docLenTable.get(doc);
            simTable[doc]=simTable[doc]/(docLen*queryLength);
        return simTable;
    
    def rankRetrievedDocs(self,simTable,n):
        rankedDocs=list();
        sortedDocs=list();
        for key, val in simTable.items():
            sortedDocs.append((val,key));
    
        sortedDocs.sort(reverse=True);
        for key, val in sortedDocs[:n]:
            file_path=val
            rankedDocs.append(file_path);
        return rankedDocs;
    
    def topNWordsinVocab(self,terms,n):
        topWords=dict();
        termList=list();
        for key, val in terms.items():
            termList.append((val,key));
            
        termList.sort(reverse=True);
        i=0;
        for key, val in termList[:n]:
            i=i+1;
            #print(i,val,key);
            topWords[val]=key;
            
        return topWords;
    
    def search_for_text(self, ii, text):
        simTable=self.retrievalDocsOnQuery(text,ii);
        rankedAllDocs=self.rankRetrievedDocs(simTable, len(simTable));
        rankedList = self.loadURLsFromDB(rankedAllDocs)
        return rankedList

    def loadURLsFromDB(self, pageList):
        rankedList=list();
        conn = sqlite3.connect('unt_web.sqlite')
        cur = conn.cursor()
        for id in pageList:
            cur.execute('SELECT url FROM Pages where id=?',(int(id),))
            rankedList.append(cur.fetchone()[0])
        return rankedList

if __name__=='__main__':
    s = search()
    print "Loading the inverted index object.."
    ii = s.invertIndexDocs()
    moreQueries = True
    while moreQueries is True:
        l = s.search_for_text(ii, raw_input("Enter the query to search for:"));
        rank = 1
        for link in l:
            print rank, link
            rank = rank+1
            if(rank>10):
                break
        if(raw_input("Another Query?(Y or N)") in ["Y", "y"]):
            moreQueries = True
        else:
            moreQueries = False

