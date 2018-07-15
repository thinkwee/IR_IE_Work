# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 16:29:25 2018

@author: Xie Yang
"""

import re
import os


# 提取楼主的发帖内容
def get_content(post):
    # 提取楼主发帖内容
    pattern = '\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*.*?\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*'
    content = re.search(pattern, post, flags=re.DOTALL).group()
    # 去掉*
    content = content[40:-40].strip()
    # 去掉html转义字符
    content = content.replace('&nbsp;', '')
    content = content.replace('&quot;', '')
    content = content.replace('&amp;', '')
    content = content.replace('&lt;', '')
    content = content.replace('&gt;', '')
    content = content.replace('&nbsp;', '')
    # 去掉‘※ 修改:’
    pattern = '※ 修改:.*'
    content = re.sub(pattern, '', content).strip()
    # 提取标题
    pattern = '标题:.*'
    title = ''
    if re.search(pattern, content):
        title = re.search(pattern, content).group()[4:]
    # 去掉‘发信人’到‘站内’之间的内容
    pattern = '发信人:.*?, 站内'
    content = re.sub(pattern, '', content, flags=re.DOTALL).strip()
    # 把标题放在第一行
    content = title + '\n' + content
    # print(content)
    return content


# 批量提取楼主发帖内容
def traverse():
    root_path = 'D:\\BUPT\\研究生\\课程\\信息检索与信息抽取\\大作业\\corpora_raw\\'
    result_path = 'D:\\BUPT\\研究生\\课程\\信息检索与信息抽取\\大作业\\content\\'
    # 检查遍历目录和结果目录是否存在
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    if not os.path.exists(root_path):
        print(root_path + ' is not exist!')
    else:
        file_name = 1
        for root, dirs, files in os.walk(root_path):
            for file in files:
                # 判断文件是否为空
                if os.path.getsize(root + '\\' + file) and 'Re:' not in file:
                    with open(root + '\\' + file, 'r', encoding='utf8') as fin:
                        print(root, file)
                        content = get_content(fin.read())
                        with open(result_path + str(file_name) + '.txt', 'w', encoding='utf8') as fout:
                            fout.write(content)
                        file_name += 1


traverse()
