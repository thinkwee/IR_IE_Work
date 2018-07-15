from django.shortcuts import render
from .forms import AddForm
import jieba
import os
import sys
from .ir import work
import pickle
from .segment import retrieval

path_root = os.path.abspath('.')
path_root += '/search'
with open(path_root + '/sender.pickle', 'rb') as file:
    dict_sender = pickle.load(file)
with open(path_root + '/time.pickle', 'rb') as file:
    dict_time = pickle.load(file)
path_keywords = path_root + "/keywords"  # 关键词目录
path = path_root + "/corpora"  # 文档文件夹目录


class result:
    def __init__(self, title, value, sender, time, keywords, abstract):
        self.title = title
        self.value = value
        self.sender = sender
        self.time = time
        self.keywords = keywords
        self.abstract = abstract


def index(request):
    if request.method == 'POST':
        query = ""
        form = AddForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['keywords']
            order_dict, order_dict_embedding = work(query)
            order_dict_xieyang = retrieval(query)
        itmp = 0
        result_list = []
        for key, value in order_dict:
            itmp += 1
            if itmp == 10:
                break
            sender = dict_sender[key]
            time = dict_time[key]
            keywords = ""
            file = open(path_keywords + "/" + key, "r")
            for line in file:
                word, freq = line.strip().split(' ')
                keywords += word + " "
            file.close()
            contents = open(path + "/" + key, "r").read().split('\n')
            abstract = ""
            for content in contents:
                abstract += content
            r = result(key, value, sender, time, keywords, abstract[len(key) - 4:100])
            result_list.append(r)

        itmp = 0
        result_list_embed = []
        for key, value in order_dict_embedding:
            itmp += 1
            if itmp == 10:
                break
            sender = dict_sender[key]
            time = dict_time[key]
            keywords = ""
            file = open(path_keywords + "/" + key, "r")
            for line in file:
                word, freq = line.strip().split(' ')
                keywords += word + " "
            file.close()
            contents = open(path + "/" + key, "r").read().split('\n')
            abstract = ""
            for content in contents:
                abstract += content
            r = result(key, value, sender, time, keywords, abstract[len(key) - 4:100])
            result_list_embed.append(r)

        itmp = 0
        result_list_xieyang = []
        for key, value in order_dict_xieyang.items():
            itmp += 1
            if itmp == 10:
                break
            sender = dict_sender[key]
            time = dict_time[key]
            keywords = ""
            file = open(path_keywords + "/" + key, "r")
            for line in file:
                word, freq = line.strip().split(' ')
                keywords += word + " "
            file.close()
            contents = open(path + "/" + key, "r").read().split('\n')
            abstract = ""
            for content in contents:
                abstract += content
            r = result(key, value, sender, time, keywords, abstract[len(key) - 4:100])
            result_list_xieyang.append(r)

        return render(request, 'response.html',
                      {'result_list': result_list, 'result_list_embed': result_list_embed, 'query': query,
                       'result_list_xieyang': result_list_xieyang})
    else:
        form = AddForm()
        return render(request, 'index.html', {'form': form})

# Create your views here.
