# -*- coding: utf-8 -*-
"""PriorityText.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jjNTzBz-s10StS4hYM76eA84Nr_56nWY
"""

!pip install textacy
import textacy.vsm
from textacy.vsm import Vectorizer

from nltk.tokenize import TweetTokenizer
from nltk import pos_tag, ne_chunk

import string,re
import spacy,nltk

nlp = spacy.load("en_core_web_sm")
nltk.download('averaged_perceptron_tagger')

nltk.download('stopwords')
from nltk.corpus import stopwords 
stop=stopwords.words('english')

text=["The over-flowing water has really caused untold miseries. Villages after villages have been submerged.You might have noticed that a vast tract of land looks like a sheet of water. People had to desert the villages. Thousands are already rendered homeless.Yes, they have been shifted to emergency flood-centers. Relief materials are scanty. Some of them have already died.  It is terribly shocking. The condition of domestic animals beggar description. They do not have flood-shelters and relief camps.I have seen many corpses and carcasses flowing down the streams of water. There is another negative effect of it. They are seriously polluting water.Exactly! Besides, the stench that comes out of them is very harmful to the environment. Diseases have started breaking out.Yes, the incidence of cholera, diarrhea, typhoid, fever and flu has greatly increased recently. Medical facilities are quite inadequate to combat the battle.Exactly, this water has worked out a ghastly havoc. A lot of houses have toppled down, and household properties have been washed away.Besides, standing crops have been destroyed. People have a black and blank future.","Hello. Very good of you to respond this early. I am Ramesh. I am the witness of the accident. It happened in the Green Park area at XYZ street.Yeah, sure. There is a couple travelling by a bike. The husband was sitting behind and the wife was driving the bike. Perhaps it was the first time for the women and the husband was teaching her how to drive.  when they were crossing a traffic signal, the wife was unable to apply the brakes. Suddenly there was a truck coming from the other side and it hit the bike very hard. The husband was spot dead at the location and the wife was barely alive with fractures in her leg and hand. So you need to hurry. This happened 35 minutes ago and no help has come till now. Yes. I am with the women with another 4-5 person keeping her awake. Can you give us some first aid advice that may help her. Ok. come soon. We will do whatever possible. Be gods with her.","We need an ambulance right away.Dirk Omora.There was a car accident.	I’m not sure. I was driving in my car when I saw the pileup. I’m somewhere on Blossom Road. Can you trace my location?	 One of the drivers is lying on the ground unconscious and the other one is bleeding. There’s someone trapped in the back of her car, too. We need to rescue her before the car explodes! I’m going to see if I can help.Okay, but hurry!","I need a doctor immediately! ,My wife just collapsed on the floor! , I'm sorry. It's just that my wife. I need the emergency room., What's taking you so long?" ,"Help me! I need a doctor! My wife is on the floor! I need some help, right now! Hurry, please!"]

text[1]

i=1;
for w in text:
  doc = nlp(w)
  print(str(i)+"  Text")
  i=i+1
  for ent in doc.ents:
    print(ent.text,ent.label_)

ss= input()



main_words = [u'help',u'emergency', u'died', u'injured', u'stranded', u'wounded', u'hurt', u'helpless', u'wrecked', u'flood',u'accident',u'doctor']
useful_entities = [u'NORP', u'FACILITY', u'ORG', u'GPE', u'LOC', u'EVENT', u'DATE', u'TIME',u'CARDINAL']
nn=[]
new_nn=nn
nn=ss.split(' ')
for n in nn:
  if(n not in stop):

    main_words.append(n)
#print(main_words)

nlp = spacy.load('en')
spacy_tweets = []

for doc in nlp.pipe(text, n_threads = -1):
    spacy_tweets.append(doc)
print(spacy_tweets)

content_tweets = []
for single_tweet in spacy_tweets:
    single_tweet_content = []
    for token in single_tweet: 
        if ((token.ent_type_ in useful_entities)  
            or (token.pos_ == u'NUM') 
            or (token.lower_ in main_words)):
            single_tweet_content.append(token)
    content_tweets.append(single_tweet_content)

tweet_num=0
print ("original_tweet \n" + str(spacy_tweets[tweet_num]) 
       + "\n\noriginal_tweet\n" + str([str(x) for x in spacy_tweets[tweet_num]])
       + "\n\ncontent_tweet\n" + str(content_tweets[tweet_num])
      )

vectorizer = Vectorizer(tf_type='linear', apply_idf=True, idf_type='smooth')
term_matrix = vectorizer.fit_transform([tok.lemma_ for tok in doc] for doc in spacy_tweets)
np_matrix = term_matrix.todense()
np_matrix.shape

for key in sorted(vectorizer.vocabulary_terms, reverse=True)[:2]:
    print (key, vectorizer.vocabulary_terms[key])

import numpy as np
for token in content_tweets[0]:
    print (token.lemma_, vectorizer.vocabulary_terms[token.lemma_], np.max(np_matrix[:,vectorizer.vocabulary_terms[token.lemma_]]))

len(content_tweets[3])

tfidf_dict = {}
content_vocab = []
for tweet in content_tweets: 
    for token in tweet: 
        if token.lemma_ not in tfidf_dict: 
            
            content_vocab.append(token.lemma_)
            tfidf_dict[token.lemma_] = np.max(np_matrix[:,vectorizer.vocabulary_terms[token.lemma_]])

class my_dictionary(dict):  
  
    # __init__ function  
    def __init__(self):  
        self = dict()  
          
    # Function to add key:value  
    def add(self, key, value):  
        self[key] = value  
  
# Main Function  
prior = my_dictionary()  

ind=0
for key in tfidf_dict:
  #print(key)
  for i in range(0,len(content_tweets),1):
    #print(i)
    for j in content_tweets[i]:
      if(key==j.lemma_):
        if(tfidf_dict[key]):
          temp=tfidf_dict[key]
          prior.add(i,tfidf_dict[key]+temp)
        else:
          prior.add(i,tfidf_dict[key])
        
new={}
new=prior.copy()

for key in new:
  
  new[key]=new[key]/len(content_tweets[key])
  
print(prior)
print(new)
print("Calls should be done in priority:")
print(sorted(new,key=new.__getitem__,reverse=True))

for key in sorted(tfidf_dict)[:]:
    print ("WORD:" + str(key) + " -- tf-idf SCORE:" +  str(tfidf_dict[key]))



#COWTS

!pip install pymprog
from pymprog import *

begin('COWTS')
# This defines whether or not a tweet is selected
x = var('x', len(spacy_tweets), bool)

# Check this worked
print(x[2])
y = var('y', len(content_vocab), bool)

maximize(sum(x) + sum([tfidf_dict[content_vocab[j]]*y[j] for j in range(len(y))]));

## Maximum length of the entire tweet summary

# Was 150 for the tweet summary, 
# But generated a 1000 word summary for CONABS
L = 150

# hiding the output of this line since its a very long sum 
sum([x[i]*len(spacy_tweets[i]) for i in range(len(x))]) <= L;

def content_words(i):
    '''Given a tweet index i (for x[i]), this method will return the indices of the words in the 
    content_vocab[] array
    Note: these indices are the same as for the y variable
    '''
    tweet = spacy_tweets[i]
    content_indices = []
    
    for token in tweet:
        if token.lemma_ in content_vocab:
            content_indices.append(content_vocab.index(token.lemma_))
    return content_indices

def tweets_with_content_words(j):
    '''Given the index j of some content word (for content_vocab[j] or y[j])
    this method will return the indices of all tweets which contain this content word
    '''
    content_word = content_vocab[j]
    
    index_in_term_matrix = vectorizer.vocabulary_terms[content_word]
    
    matrix_column = np_matrix[:, index_in_term_matrix]
    
    return np.nonzero(matrix_column)[0]

for j in range(len(y)):
    sum([x[i] for i in tweets_with_content_words(j)])>= y[j]

for i in range(len(x)):
    sum(y[j] for j in content_words(i)) >= len(content_words(i))*x[i]

solve()

result_x =  [value.primal for value in x]
print(result_x)
result_y = [value.primal for value in y]
end()

chosen_tweets = np.nonzero(result_x)
chosen_words = np.nonzero(result_y)



print(chosen_tweets[0])

#len(chosen_tweets[1]), len(chosen_words[1])

for i in chosen_tweets[0]:
    print ( i)
    print( spacy_tweets[i])
    print( len(spacy_tweets[i]))



