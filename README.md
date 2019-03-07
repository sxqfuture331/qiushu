
项目运行之前运行这句话
pip install -r requirements -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
运行爬虫，获取数据
scrapy crawl QiushuSpider（必须启动MongoDB服务）
然后运行python run.py
