
from utils import *
from db_clients import get_product,get_company
import sys
sys.path.append("../")
from faiss_index import RemoveID
import faiss


ignore_ids = []
with open('./ignore_index.txt','r') as lines:
    for line in lines:
        line = line.replace('\n','')
        ignore_ids.append(line)

root_ids = load_ids('../index/products.pkl')

index_path = '../index/vectors.index'

remover = RemoveID(index_path)




index = faiss.read_index(index_path)
print(index)