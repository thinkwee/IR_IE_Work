import os
import jieba.analyse
import pickle
import re

path = "./corpora"  # 文件夹目录
path_raw = "./corpora_raw"  # 文件夹目录
files = os.listdir(path)  # 得到文件夹下的所有文件名称

path_keywords = "./keywords"
path_pickle = "./tfidf"

jieba.initialize()
jieba.analyse.set_idf_path("./idf_list.txt")

dict_sender = {}
dict_time = {}

count = 0


def process_content(content, title):
    pos_s = content.find("站内")

    pos_sender_start = content.find("发信人")
    pos_sender_end = content.find("信区")

    content_sender = content[pos_sender_start + 4:pos_sender_end - 2]

    pos_time_start = content.find("发信站")
    content_time = content[pos_time_start + 3:pos_s]
    p1 = re.compile(r'[(](.*?)[)]', re.S)

    print(title)
    if re.findall(p1, content_time):
        content_time = re.findall(p1, content_time)[0]
    else:
        content_time = "0"

    return content_sender, content_time


for title in files:
    topK = 30
    content = open(path_raw + "/" + title, 'r').read()
    content_sender, content_time = process_content(content, title)
    dict_sender[title] = content_sender
    dict_time[title] = content_time

    content_main = open(path + "/" + title, 'r').read()

    dict_tfidf = {}
    tags = jieba.analyse.extract_tags(content_main, topK=topK, withWeight=True)
    file_keyword = open(path_keywords + "/" + title, "w")

    for word, value in tags:
        file_keyword.write(word + " " + str(value) + "\n")
        dict_tfidf[word] = value

    file = open(path_pickle + "/" + title + '.pickle', 'wb')
    pickle.dump(dict_tfidf, file)
    file.close()

    file = open(path + "/" + title, 'w')
    file.write(content_main)
    file.close()

    count += 1
    if count % 200 == 0:
        print("%d/5936" % count)

file = open('./sender.pickle', 'wb')
pickle.dump(dict_sender, file)
file.close()

file = open('./time.pickle', 'wb')
pickle.dump(dict_time, file)
file.close()
