#   信息抽取与信息检索大作业

##  项目环境
-	大作业构建为一个django项目，后端使用python，前端使用html+css，前后端数据交互采用django，数据多记录成词典并用pickle存取。
-	Python3 、Django2.0.7、结巴分词、Ubuntu16.04

## 项目文件
-	主要在mysite文件夹下
-	mysite
	-	mysite:主站点配置
	-	db.sqlite3:默认数据库，未使用
	-	manage.py:工作脚本，通过此脚本启动本地服务器
	-	search:大作业搜索引擎网页app
		-	content:归一化tfidf检索所用语料，处理成编号形式
		-	corpora:结巴tfidf和词嵌入检索所用语料，与content相同，但保留原标题
		-	keywords:语料关键词及其tfidf值
		-	migrations:Django项目自带目录
		-	static:Django项目静态文件项目
		-	templates:Django项目模板文件夹，包含搜索和搜索结果两个主要的html文件
		-	tfidf:pickle保存的所有语料关键词词典及其tfidf值
		-	admin.py、apps.py、models.py、tests.py、urls.py:Django项目自带文件
		-	bbs.model:归一化检索所用数据
		-	byr.py:爬虫脚本
		-	create_embedding.py:载入预训练词嵌入，并只保留语料中存在的单词
		-	create_idf.py:计算idf表
		-	create_raw.py:整理爬取后的文件
		-	dict_idf.pickle、time.pickle、sender.pickle、embedding.pickle:pickle保存的idf词典、发帖时间和发帖人词典、词嵌入模型
		-	forms.py:创建搜索框
		-	index.txt:归一化tfidf检索所用编号语料索引
		-	ir.py:词嵌入和结巴tfidf索引主程序
		-  preprocessing.py:创建tfidf表，信息抽取程序
		-  pretreat:语料预处理
		-  segment.py:归一化tfidf检索主程序
		-  segment.txt:分词文件
		-  stopwords.txt:停用词表
		-  views.py:Django前后端数据交互主程序

##	如何使用
确认环境安装好后，运行爬虫文件和预处理文件得到数据，切换到manage.py所在目录，命令行输入：
```python
python manage.py runserver
```
在浏览器中输入：
```
http://127.0.0.1:8000
```
载入搜索界面并使用

## 效果图
-	检索
![检索](http://ojtdnrpmt.bkt.clouddn.com/ir.png)
-	三种检索模式结果
![检索1](http://ojtdnrpmt.bkt.clouddn.com/irr1.png)
![检索2](http://ojtdnrpmt.bkt.clouddn.com/irr2.png)
![检索3](http://ojtdnrpmt.bkt.clouddn.com/irr3.png)

##	已知问题
由于归一化tfidf是另外一位同学缩写，在处理标题上会存在一点不兼容，可能遇到词典查找错误，可在view.py和response.html中删除相应部分，直接修改运行segment.py进行检索。

##	数据
数据爬取自北邮人论坛缘来如此板块，需要的同学可以自行修改爬虫爬取，暂时不提供帖子数据，注意需输入自己的用户名和密码登录