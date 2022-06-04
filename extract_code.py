import pandas as pd
import re
from vncorenlp import VnCoreNLP
from memoization import cached
import json
from utils import *

vncore_path = "/content/drive/MyDrive/VnCoreNLP/VnCoreNLP-1.1.1.jar"
rdrsegmenter = VnCoreNLP(vncore_path,annotators="pos", max_heap_size='-Xmx4g')
ignore_words = []
special_words = []

with open('./stopword.txt','r') as lines:
    for line in lines:
        line = line.replace('\n','')
        ignore_words.append(line)

with open('./special_word.txt','r') as lines:
    for line in lines:
        line = line.replace('\n','')
        special_words.append(line)

vocab = load_vocab()
vocab2 = load_vocab2()

def lower_text(inputString):
    ori_dict = {}
    res_text = []
    for word in inputString.split():
        tmp = word
        for w in word:
            if w.isdigit():
                next
            elif w not in vocab2:
                tmp = word.lower()
                if tmp != word:
                    ori_dict[tmp] = word
                else:
                    next
                # break

        res_text.append(tmp)

    return " ".join(res_text), ori_dict

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)
    
def get_kw_product(text, max_len_phrase=15):
    # text = clean(text, vocab)
    text, original = lower_text(text)
    # print(original)
    tmp = rdrsegmenter.annotate(text)['sentences']
    phrases = []
    b_tokens = []
    for count_token,token in enumerate(tmp):
        if count_token>1:
            break
        for d in token:  
            form = d['form']
            pos_tag = d['posTag']
            print(form, pos_tag)
            # if form not in ignore_words:
            ## giữ các cụm từ   
            if "_" in form and pos_tag=="N":
                pos_tag = "Q"
            tup = [(form,pos_tag)]
            b_tokens += tup
            
        pos_tags = [convert_pos(tok[1]) for tok in b_tokens]
        pos_tags = "".join(pos_tags)
        print(pos_tags)
        # pattern = r"(.*?)*P+M*|Q+M*"
        pattern = r"(.*?)*N+O*M*U*N*|Q+O*M*U*N*"
        iterator = re.finditer(pattern, pos_tags)
        b_phrases = filter(lambda x: len(x) <= max_len_phrase, [[token[0] for token in b_tokens[match.start():match.end()]] for match in iterator])
        b_phrases = [" ".join(phrase) for phrase in b_phrases]
        b_phrases = [word.replace("_"," ") for word in b_phrases]
        phrases += b_phrases
    # return phrases
        if len(phrases) > 0:
            res = phrases[0]
            res= " ".join([original.get(w) if original.get(w,False) else w for w in res.split()])
        else:
            res = ""

    return res        

def convert_pos(pos_tag):
        if pos_tag == 'Q':
            return 'Q'
        elif pos_tag == 'Np' or pos_tag == 'Ny':
            return 'T'
        elif pos_tag == "M":
            return 'M'
        elif pos_tag == "Nu":
            return 'U'
        elif pos_tag == "N" or pos_tag == "Nb" or pos_tag == "V" or pos_tag == "A":
            return 'N'
        elif pos_tag == "Cc":
            return 'N'
        else:
            return 'O'

def convert_pos_case_nonNp(pos_tag):
        if pos_tag == 'M':
            return 'M' #contain number
        else:
            return 'K' #keep
if __name__ == "__main__":

    # from db_clients import get_product
    # df = get_product(100)
    # texts = df.Name.values.tolist()
    # for text in texts:
    #     print(get_kw_title(text))
    
    # from blog_db_clients import get_content
    # id_blog = "20220227094237283"
    # text = get_content(id_blog)
    # phrases = list(set(get_kw_title(text)))
    # print(phrases)  

    # text = " Cối xay tiêu loại B Mỹ Nghệ Việt MNV-SPGB-WC-0"
    # text = title+ " " + sapo + " " + body
    # phrases = list(set(get_kw_title(text)))
    # print(phrases)
    
    text = "Thiết bị chia mạng Switch Linksys LGS124, 24-Port"
    # print(text)
    print(get_kw_product(text))
    rdrsegmenter.close()
