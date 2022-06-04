import pickle
import re
import pandas as pd
from tqdm import tqdm
import json

def load_vocab():
    with open('./vocab.json','r') as f:
        vocab = json.load(f)
    vocab = list(vocab.keys())
    upper = [v.upper() for v in vocab if not v.isdigit()]
    vocab = vocab + upper
    return vocab

def load_vocab2():
    with open('./vocab2.json','r') as f:
        vocab = json.load(f)
    vocab = list(vocab.keys())
    upper = [v.upper() for v in vocab if not v.isdigit()]
    vocab = vocab + upper
    return vocab

def clean(text,vocab):
    cleanr = re.compile(r'<[^>]+>|<.*?>|&nbsp;|&amp;|&lt|p&gt|\u260e|<STYLE>(.*?)<\/STYLE>|<style>(.*?)<\/style>')
    text = re.sub(cleanr, ' ', text)
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    text = re.sub("[!\"#%&\\(\)\*\+,:;<=>?@[\]^_{|}~]]",". ",text)
    text = re.sub("(\d+\/\d+\/\d+|\d+\/\d+)"," ",text) # remove datetime
    inside_pattern = re.compile(r'\[.*\]|\(.*\)|\{.*\}')
    text = inside_pattern.sub(r'',text)
    text = text.replace(' - ',' ')
    text = text.replace(' – ',' ')
    text = " ".join(["".join([e for e in word if e in vocab ]) for word in text.split()])
    text = re.sub("\xa0","",text)
    text = re.sub("\.+",'. ',text)
    text = re.sub("\s+",' ',text)
    return text

def create_keyword(file_path):
    with open(file_path,'rb') as f:
        data = pickle.load(f)
    words = set()
    for d in tqdm(data):
        if type(d)!= float:
             for t in d.lower().split():
                words.add(t)
    words = list(words)
    with open('allow_words.pkl','wb+') as f:
        pickle.dump(words,f)
    print(len(words))
    print(words[:50])

def load_allow_words(file_path):
    with open(file_path,'rb') as f:
        data = pickle.load(f)
    return data

def load_ids(file_path):
    with open(file_path,'rb') as f:
        data = pickle.load(f)
    return data

if __name__ == "__main__":
    create_keyword("../gen_tag_wss/keywords.pkl")
    # a = set([1,1,2,3,3,4])
    # print(list(a))