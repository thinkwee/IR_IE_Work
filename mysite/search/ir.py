import pickle
import jieba
import os
import math

path_root = os.path.abspath('.')
path_root += '/search'
with open(path_root + '/dict_idf.pickle', 'rb') as file:
    dict_idf = pickle.load(file)
with open(path_root + '/embedding.pickle', 'rb') as file:
    dict_embedding = pickle.load(file)

path = path_root + "/corpora"  # 文档文件夹目录
path_tfidf = path_root + "/tfidf"  # tfidf词典目录
files = os.listdir(path)  # 得到文件夹下的所有文件名称


def calc(vectora, vectorb):
    lena = 0.0
    lenb = 0.0
    dot_product = 0.0
    for i in range(300):
        lena += pow(vectora[i], 2)
        lenb += pow(vectorb[i], 2)
        dot_product += vectora[i] * vectorb[i]
    lena = math.sqrt(lena)
    lenb = math.sqrt(lenb)
    return dot_product / (lena * lenb)


def work(query):
    seg_list = jieba.cut_for_search(query)
    dict_query = {}
    for query_word in seg_list:
        if str(query_word) in dict_idf:
            dict_query[query_word] = float(dict_idf[query_word])
        else:
            dict_query[query_word] = 0.0

    dict_ir = {}
    dict_ir_embedding = {}

    for title in files:
        with open(path_tfidf + '/' + title + '.pickle', 'rb') as file_tfidf:
            dict_tfidf = pickle.load(file_tfidf)
        value = 0.0
        value_embedding = 0.0
        for key_query in dict_query:
            if key_query in dict_tfidf:
                value += dict_query[key_query] * dict_tfidf[key_query] + 1.0
                for key_document in dict_tfidf:
                    if key_query in dict_embedding and key_document in dict_embedding:
                        value_embedding += calc(dict_embedding[key_query], dict_embedding[key_document])

        dict_ir[title] = value

        dict_ir_embedding[title] = value_embedding

    order_dict_ir = sorted(dict_ir.items(), key=lambda item: item[1], reverse=True)
    order_dict_ir_embedding = sorted(dict_ir_embedding.items(), key=lambda item: item[1], reverse=True)

    return order_dict_ir, order_dict_ir_embedding
