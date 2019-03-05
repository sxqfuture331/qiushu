import pymongo
import requests
from flask import Flask
from datetime import datetime
from lxml import html
from scrapy import Selector
from bs4 import BeautifulSoup

from flask import Flask, render_template_string, render_template, request
app = Flask(__name__)

 
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["shuju"]
mycol = mydb["asd"]

@app.route('/test')
def test():

    url = request.args.get('tag')
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    }
    wb_data = requests.get(url,headers=headers)
    wb_data.encoding = 'utf-8'
    soup = BeautifulSoup(wb_data.text,'lxml')
    divs = soup.find_all(class_ = 'book_content')
    divs_no = soup.find_all(id = 'stsm')
    # 处理内容
    nei_zong = ''
    neirong = ''
    for div in divs_no:
        nei_zong = div.get_text()
    for div in divs:
        i = div.get_text()
        neirong = i[:-len(nei_zong)-11]
    # 处理章节名
    nei_zhang = ''
    nei_qi = ''
    div_zhang = soup.find_all(class_ = 'date')
    div_qi = soup.find_all(class_ = 'info')
    for div in div_qi:
      nei_qi = div.get_text()
    for div in div_zhang:
      i = div.get_text()
      nei_zhang = i[:-len(nei_qi)-1]
    params = {
        'succ' : neirong,
        'nei_zhang' : nei_zhang
    }
    return render_template('home/content.html', params=params)

@app.route('/', methods=['GET', 'POST'])
def home_sort():
    _data = request.values.get('tag')
    fan_ye = request.values.get('ye')
    fan_ye_lei = request.values.get('ye_lei')
    aa = []
    if bool(_data or fan_ye_lei):
      # import ipdb; ipdb.set_trace()
      # i = mycol.find({"booktype": ' 官场职场 '})
      y = 0
      if bool(fan_ye):
        y = 0 + int(fan_ye)
      i = mycol.find({"booktype": _data}).skip(0).limit(10)
      jj = ''
      if bool(fan_ye_lei):
        jj = fan_ye_lei[0:6]
        y = 0 + int(fan_ye_lei.split(fan_ye_lei[0:6])[1])
        i = mycol.find({"booktype": jj}).skip(y).limit(10)
      for x in i :
          params_x = {
            # 作者
            'author' : x['author'],
            # 书籍分类标签
            'booktype' : x['booktype'],
            # 书籍状态
            'state' : x['state'],
            # 书籍封面
            'tuurl' : x['tuurl'],
            # 书籍描述
            'describe' : x['describe'][0:200],
          }
          params_shu = dict(zip([x['name']], [x['showUrl']]))
          bb = {}
          bb['params_x']=params_x
          bb['params_shu']=params_shu
          bb['y'] = y + 10
          if bool(_data):
            bb['_data'] = _data
          bb['jj'] = jj
          aa.append(bb)
      return render_template('home/sort.html', params=aa)
    else:
      yy = 0
      if bool(fan_ye):
        yy = 0 + int(fan_ye)
      y = 0 + yy
      i = mycol.find().skip(y).limit(10)
      # 一共有多少条数据
      # print(i.count())
      for x in i :
          params_x = {
            # 作者
            'author' : x['author'],
            # 书籍分类标签
            'booktype' : x['booktype'],
            # 书籍状态
            'state' : x['state'],
            # 书籍封面
            'tuurl' : x['tuurl'],
            # 书籍描述
            'describe' : x['describe'][0:200],
          }
          params_shu = dict(zip([x['name']], [x['showUrl']]))
          bb = {}
          bb['params_x']=params_x
          bb['params_shu']=params_shu
          bb['y'] = y + 10
          aa.append(bb)
      return render_template('home/sort.html', params=aa)

@app.route('/sou', methods=['GET', 'POST'])
def home_sou():
    sou_data = request.values
    name = sou_data.get('searchkey')
    print(name)
    # 根据名字查询
    xi = mycol.find_one({"name":name})
    if xi == None:
        return home_sort()
    params_x = {
          # 书名
          'name' : xi['name'],
          # 作者
          'author' : xi['author'],
          # 书籍分类标签
          'booktype' : xi['booktype'],
          # 书籍状态
          'state' : xi['state'],
          # 书记封面
          'tuurl' : xi['tuurl'],
          # 书籍描述
          'describe' : xi['describe'],
        }
    params_zhang = dict(zip(xi['chapter'], xi['chapterurl']))
    params = {
        'params_x' : params_x,
        'params_zhang' : params_zhang,
    }
    return render_template('home/details.html', params=params)

@app.route('/details')
def home_details():
    '''小说详情'''
    url = request.args.get('tag')
    # 根据链接查询
    xi = mycol.find_one({"showUrl":url})
    params_x = {
          # 书名
          'name' : xi['name'],
          # 作者
          'author' : xi['author'],
          # 书籍分类标签
          'booktype' : xi['booktype'],
          # 书籍状态
          'state' : xi['state'],
          # 书记封面
          'tuurl' : xi['tuurl'],
          # 书籍描述
          'describe' : xi['describe'],
        }
    params_zhang = dict(zip(xi['chapter'], xi['chapterurl']))
    params = {
        'params_x' : params_x,
        'params_zhang' : params_zhang,
    }
    return render_template('home/details.html', params=params)



if __name__ == '__main__':
    app.run(debug=True)