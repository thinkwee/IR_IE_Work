# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 15:24:43 2018

@author: Xie Yang
"""

import jieba
import os
from math import log
from math import sqrt

N = 5936
path_root = os.path.abspath('.')
path_root += '/search'


# 加载自定义停用词表
def load_stopwords(stopwords_file):
    with open(stopwords_file, 'r') as f:
        stopwords = [line.strip() for line in f]
        return stopwords


# 分词且去掉停用词
def segment(text, stopwords):
    words = jieba.lcut(text)
    words = [word for word in words if word not in stopwords and word != ' ' and word != '\n']
    return words


# 得到索引文件
def save_index_file():
    root_path = path_root + '/content/'
    stopwords = load_stopwords(path_root + '/stopwords.txt')
    # 每个term在每篇文档中出现的频率
    kw_tf_dict = {}
    # 每个term出现在不同文档中的文档个数
    kw_df_dict = {}
    for root, dirs, files in os.walk(root_path):
        for file in files:
            with open(root + '\\' + file, 'r', encoding='utf8') as f:
                # 一篇文档的去停用词的分词结果
                words = segment(f.read(), stopwords)
                # 更新每个term的tf值
                for word in words:
                    if word not in kw_tf_dict:
                        kw_tf_dict[word] = {file: 1}
                    elif file not in kw_tf_dict[word]:
                        kw_tf_dict[word][file] = 1
                    else:
                        kw_tf_dict[word][file] += 1
                # 更新每个term的df值
                for word in set(words):
                    if word not in kw_df_dict:
                        kw_df_dict[word] = 1
                    else:
                        kw_df_dict[word] += 1
    # 保存到本地
    index_file = path_root + '/index.txt'
    with open(index_file, 'w', encoding='utf8') as f:
        for word in kw_df_dict:
            f.write(word + ' ' + str(kw_df_dict[word]) + ' ')
            for file in kw_tf_dict[word]:
                f.write(file + ' ' + str(kw_tf_dict[word][file]) + ' ')
            f.write('\n')


# 载入索引文件
def load_index_file():
    index_file = path_root + '/index.txt'
    kw_tf_dict = {}
    kw_idf_dict = {}
    with open(index_file, 'r', encoding='utf8') as f:
        for line in f.readlines():
            line = line.strip().split()
            # 构造每个term的idf词典
            word = line[0]
            kw_idf_dict[word] = log(N / (int(line[1])), 10)
            # 构造每个term的tf词典
            line = line[2:]
            kw_tf_dict[word] = {}
            for i in range(0, len(line), 2):
                kw_tf_dict[word][line[i]] = int(line[i + 1])
    return kw_tf_dict, kw_idf_dict


# 遍历根目录下的文档，并对文档进行分词
def traverse_segment():
    root_path = path_root + '/content/'
    result_path = path_root + '/segment/'
    stopwords = load_stopwords(path_root + '/stopwords.txt')
    # 检查遍历目录和结果目录是否存在
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    if not os.path.exists(root_path):
        print(root_path + ' is not exist!')
    else:
        for root, dirs, files in os.walk(root_path):
            for file in files:
                with open(root + '/' + file, 'r', encoding='utf8') as fin:
                    words = segment(fin.read(), stopwords)
                    with open(result_path + file, 'a', encoding='utf8') as fout:
                        for word in words:
                            fout.write(word + ' ')
                        fout.write('\n')


# 合并两个字典，并将键相同的值相加
def merge_dict(d1, d2):
    for key in d2:
        if key in d1:
            d1[key] += d2[key]
        else:
            d1[key] = d2[key]
    return d1


# 计算查询和文档的相似度，并做归一化处理
def cal_sim(kw_list):
    sim_dict = {}
    d_dict = {}
    # 计算每篇文档的w*d
    for kw_idf, kw_w_dict in kw_list:
        kw_wd_dict = {}
        for file in kw_w_dict:
            kw_wd_dict[file] = kw_w_dict[file] * kw_idf
        sim_dict = merge_dict(sim_dict, kw_wd_dict)
    # 对每篇文档记录d^2
    for kw_idf, kw_w_dict in kw_list:
        for file in kw_w_dict:
            if file not in d_dict:
                d_dict[file] = [pow(kw_w_dict[file], 2)]
            else:
                d_dict[file].append(pow(kw_w_dict[file], 2))
    # 计算归一化的相似度
    for file in sim_dict:
        sim_dict[file] /= sqrt(sum(d_dict[file]))

    return sim_dict


# 用户信息检索
def retrieval(keywords):
    tf_dict, idf_dict = load_index_file()
    kw_list = []
    for keyword in jieba.cut(keywords):
        if keyword == ' ' or keyword == '\n':
            continue
        if keyword in idf_dict:
            print(keyword)
            kw_idf = idf_dict[keyword]
            kw_w_dict = tf_dict[keyword]
            for file in kw_w_dict:
                kw_w_dict[file] *= kw_idf
            kw_list.append([kw_idf, kw_w_dict])
        else:
            continue
    sim_dict = cal_sim(kw_list)

    dict_ans = {}
    content_path = path_root + '/content/'
    sorted_sim_dict = sorted(sim_dict.items(), key=lambda sim_dict: sim_dict[1], reverse=True)
    for idx, (file_name, sim) in enumerate(sorted_sim_dict):
        if idx > 10:
            break
        with open(content_path + '/' + file_name, 'r', encoding='utf8') as fin:
            title = fin.readline().strip('\n') + '.txt'
            dict_ans[title] = sim
    return dict_ans
