# -*- encoding: utf-8 -*-
import requests
import os
import re
import chardet

my_header = {'x-requested-with': 'XMLHttpRequest'}
byr_data = {'id': '************', 'passwd': '*************'}

# session = requests.Session()

# print(req.text)

print('本脚本可以帮助您下载某个版块的帖子' + '\n')
boarddic = {'1': 'Python', '2': 'AimGraduate', '3': 'Job', '4': 'Linux', '5': 'Friends'}
print('1 ---> Python')
print('2 ---> AimGraduate')
print('3 ---> Job')
print('4 ---> Linux')
print('5 ---> Friends')
boardnum = input('请直接输入您所选择查询的版面数字(1-5): ')
board = boarddic[boardnum]
PAGE = int(input('请输入您想下载的页数，一页代表最新的30篇帖子: '))

bourl = "http://bbs.byr.cn/board/" + board + "?p="

# headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#            'Accept-Encoding': 'gzip, deflate, compress',
#            'Accept-Language': 'en-us;q=0.5,en;q=0.3',
#            'Cache-Control': 'max-age=0',
#            'Connection': 'keep-alive',
#            'X-Requested-With': 'XMLHttpRequest',
#            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                          'Chrome/35.0.1916.153 Safari/537.36'}

# if PAGE >= 50:
#     PAGE = 50

i = 295

count_valid = 0
count_invalid = 0
while i <= PAGE:
    bbourl = bourl + str(i)
    print(bbourl)
    session = requests.Session()
    r_url = 'https://bbs.byr.cn/user/ajax_login.json'
    req = session.post(r_url, data=byr_data, headers=my_header)
    bbocont = session.get(bbourl, data=byr_data, headers=my_header).content
    # bbocont=bbocont.decode("GBK")
    # print(bbocont)
    # bbocont = session.get(bbourl, headers=my_header).content
    # find title url and name
    res = b'<td\sclass="title_9"><a\shref="(.*?)">(.*?)</a>'
    reg = re.compile(res)

    articletitle = re.findall(res, bbocont)
    # articletitle = articletitle.decode("GBK")
    # print(articletitle)

    for art in articletitle:
        # print art[0]
        # print art[1]
        headline_name = str(art[1], encoding="GBK")
        if art[1][:2] == b'Re':
            print("!!!!!!!!!!---原贴已删，跳过---!!!!!!!!!!")
            count_invalid += 1
        else:
            print(headline_name)
            count_valid += 1
            link = str(art[0], encoding="utf-8")
            articleurl = "http://bbs.byr.cn" + link
            # print(articleurl)
            pathname = './' + str(i)
            if os.path.exists(pathname):
                pass
            else:
                os.makedirs(pathname)
            filename = pathname + '/' + headline_name.replace('?', '').replace('.', '') \
                .replace(':', '').replace('<', '').replace('>', '').replace('|', '') \
                .replace('*', '').replace('/', '').replace('\\', '') + ".txt"
            # print(filename)

            if os.path.exists(filename):
                continue
            else:
                articlename = open(filename, 'w+')

            articlecontent = session.get(articleurl, data=byr_data, headers=my_header).content
            # calculate page num
            regpage = b'<li\sclass="page-pre">.*?<i>(.*?)</i>'
            respage = re.compile(regpage)
            pagedata = re.search(respage, articlecontent)
            pageall = int(pagedata.group(1))
            # print pageall
            yushu = 0
            if (pageall % 9) > 0:
                yushu = 1
            page = pageall / 9 + yushu
            # print 'page=',page
            j = 1
            while page > 0:
                pageurl = articleurl + '?p=' + str(j)
                # print 'pageurl=',pageurl
                pagecontent = session.get(pageurl, data=byr_data, headers=my_header).content
                regname = b'<span\sclass="a-u-name"><a\shref=".*?">(.*?)</a>.*?<div\sclass="a-content-wrap">(.*?)<font\sclass="f000"></font>'
                resname = re.compile(regname)
                namecontent = re.findall(resname, pagecontent)
                for nc in namecontent:
                    # print("nc1: ")
                    # print(nc[1])
                    encode_type = chardet.detect(nc[1])
                    if encode_type['encoding'] == 'GB2312':
                        encode_type['encoding'] = 'GB18030'
                        nc = str(nc[1], encoding=encode_type['encoding'])
                        tempsrc = nc.replace('<br />', '\n').replace(' ', '  ')
                        # remove picture
                        resformat = r'<a.*?>.*?</a>'
                        tempstr2 = re.sub(resformat, '', tempsrc)
                        # remove font
                        resformat2 = r'<font.*?>|</font>'
                        tempstr3 = re.sub(resformat2, '', tempstr2)
                        # remove img
                        resformat3 = r'<img.*?/>'
                        tempstr4 = re.sub(resformat3, '', tempstr3)
                        sepe = '*' * 40
                        tempstr = sepe + '\n' + tempstr4 + '\n'
                        # print tempstr
                        articlename.write(tempstr)
                page -= 1
                j += 1
    i += 1

print("有效帖子数: %d" % count_valid)
print("无效帖子数: %d" % count_invalid)
