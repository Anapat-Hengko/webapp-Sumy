from pythainlp.corpus import thai_stopwords 
thai_stopwords = list(thai_stopwords()) 
from pythainlp.tokenize import sent_tokenize 
from pythainlp.tokenize import word_tokenize 
from string import punctuation 
from heapq import nlargest

import gradio as gr

def summerizethai(input_):
   news_th = input_
   word_th = word_tokenize(news_th)
   sent_th = sent_tokenize(news_th)

   word_freq_th = {} 
   for word in word_th: 
     if word not in thai_stopwords: 
       if word not in punctuation:  
         if word not in " ": 
           if word not in word_freq_th.keys(): 
             word_freq_th[word] = 1 
           else:
             word_freq_th[word] += 1 

   max_freq_th = max(word_freq_th.values())
   for word in word_freq_th.keys():
     word_freq_th[word] = word_freq_th[word]/max_freq_th

   sent_scores_th = {} 
   for sent in sent_th: 
     for word in sent: 
       if word in word_freq_th.keys(): 
         if sent not in sent_scores_th.keys(): 
           sent_scores_th[sent] = word_freq_th[word] 
         else:   
           sent_scores_th[sent] += word_freq_th[word] 

   select_len_th = int(len(sent_scores_th)*0.1)
   sum_th = nlargest(select_len_th, sent_scores_th, key=sent_scores_th.get)

   return sum_th

title = "Web App Summy Thai"

iface = gr.Interface(
    summerizethai,
    [
      gr.inputs.Textbox(5)
    ],
    "text",
    title=title
    
)
iface.launch(share=True)