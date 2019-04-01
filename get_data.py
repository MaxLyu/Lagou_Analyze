import requests
import os
import csv
import json
import time
import random
import pandas as pd


class LagouSpider(object):

    def __init__(self):
        # user_agent 池
        self.USER_AGENT = [
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
            'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12'
        ]
        # 请求头
        self.headers = {
            'Host': 'www.lagou.com',
            'Referer': 'https://www.lagou.com/jobs/list_python%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=',
            'User-Agent': random.choice(self.USER_AGENT),
            'X-Requested-With': 'XMLHttpRequest'
        }
        # 起始 url
        self.start_url = 'https://www.lagou.com/jobs/list_python%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput='
        # 目标 url
        self.target_url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'

    # 保存 items
    def save_data(self, items):
        # 获取文件大小
        file_size = os.path.getsize(r'E:\Python\lagou.csv')
        if file_size == 0:
            # 表头
            name = ['ID', '学历要求', '工作经验', '薪资']
            # 建立DataFrame对象
            file_test = pd.DataFrame(columns=name, data=items)
            # 数据写入
            file_test.to_csv(r'analyst.csv', encoding='gbk', index=False)
        else:
            with open(r'analyst.csv', 'a+', newline='') as file_test:
                # 追加到文件后面
                writer = csv.writer(file_test)
                # 写入文件
                writer.writerows(items)

    # 请求起始 url 返回 cookies
    def get_start_url(self):
        session = requests.session()
        session.get(self.start_url, headers=self.headers, timeout=3)
        cookies = session.cookies
        return cookies

    # 将返回的 cookies 一起 post 给 target_url 并获取数据
    def post_target_url(self):
        cookies = self.get_start_url()
        pn = 1
        for pg in range(30):
            formdata = {
                'first': 'false',
                'pn': pn,
                'kd': 'python数据分析'
            }
            pn += 1

            response = requests.post(self.target_url, data=formdata, cookies=cookies, headers=self.headers, timeout=3)
            self.parse(response)
            time.sleep(60)      # 拉勾的反扒技术比较强，短睡眠时间会被封

    # 解析 response，获取 items
    def parse(self, response):
        print(response)
        items = []
        print(response.text)
        data = json.loads(response.text)['content']['positionResult']['result']

        if len(data):
            for i in range(len(data)):
                positionId = data[i]['positionId']
                education = data[i]['education']
                workYear = data[i]['workYear']
                salary = data[i]['salary']
                list = [positionId, education, workYear, salary]
                items.append(list)
        self.save_data(items)
        time.sleep(1.3)


spider = LagouSpider()
spider.post_target_url()
