from underthesea import pos_tag
from transformers import BertModel,BertTokenizer
import pandas as pd
from utils import *
import torch
from memoization import cached
from db_clients import get_product,get_company
from extract_code import get_kw_title,get_kw
from collections import Counter
import time
import math
import sys
sys.path.append("./faiss_index/")
from faiss_index import add_vector
import requests
from datetime import datetime, timedelta
from interruptingcow import timeout
import numpy as np
import os
from tqdm import tqdm

ignore_words = []
with open('./stopword.txt','r') as lines:
    for line in lines:
        line = line.replace('\n','')
        ignore_words.append(line)
vocab = load_vocab()


def post_api(text):
    url = 'http://118.70.151.32:9990/represent_product'
    r = requests.post(url,json={'text':text})
    return r.json()



def create_data(df_dir,ids_path,vector_path):
    if not os.path.exists(df_dir) or not os.path.exists(ids_path) or not os.path.exists(vector_path):
        print('Invalid path')
    else:
        root_id_company = load_ids(ids_path)
        root_ids = [i[0] for i in root_id_company]
        data_dir = df_dir
        list_file = os.listdir(data_dir)
        for f in list_file:
            df = pd.read_csv(os.path.join(data_dir,f))
            df = df.dropna()
            s = time.time()
            # batch_size = 5k
            batch_size = 20000
            num_path = math.ceil(len(df)/batch_size)
            for i in range(num_path):
                ids = []
                vectors = []

                b_df = df[i*batch_size:(i+1)*batch_size]
                for idx,row in b_df.iterrows():
                    if idx%5000==0:
                        print(idx)
                    if int(row['ID']) in root_ids:
                        continue
                    else:                
                        try:
                            # with timeout(1, exception=RuntimeError):
                                kw = row['keyword']
                                vector = post_api(kw)['product_vector']
                                if len(vector)>0:
                                    vectors.append(vector)
                                    try:
                                        company = get_company(row['ID'])
                                    except:
                                        company = ''
                                    ids.append((row['ID'],company))
                        # except RuntimeError:
                        #     continue
                        except Exception as e:
                            print(e)
                            continue

                print(time.time()-s)
                s = time.time()
                add_vector(ids,vectors,ids_path,vector_path)
            print("store successfull")


if __name__ == "__main__":
    import time
    s= time.time()
    create_data_2()
    print(time.time()-s)
