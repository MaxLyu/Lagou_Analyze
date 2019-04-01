#!/usr/bin/env python
# _*_ coding utf-8 _*_
import csv
import time
import re
import requests
from lxml import etree


headers = {
    'Host': 'www.lagou.com',
    'Referer': 'https://www.lagou.com/jobs/list_python%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/536.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
}


# 生成详情页 url
def get_url():
    urls = []
    with open("analyst.csv", 'r', newline='') as file:
        # 读取文件
        reader = csv.reader(file)
        for row in reader:
            # 根据 positionID 补全 url
            if row[0] != "ID":
                url = "https://www.lagou.com/jobs/{}.html".format(row[0])
                urls.append(url)

    file.close()
    return urls


# 获取详细信息
def get_info():
    urls = get_url()
    length = len(urls)
    for url in urls:
        print(url)
        description = ''
        print(length)
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        content = etree.HTML(response.text)
        detail = content.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()')
        print(detail)

        for i in range(1, len(detail)):

            if '要求' in detail[i-1]:
                for j in range(i, len(detail)):
                    detail[j] = detail[j].replace('\xa0', '')
                    detail[j] = re.sub('[、;；.0-9。]', '', detail[j])
                    description = description + detail[j] + '/'
                print(description)
        write_file(description)
        length -= 1
        time.sleep(3)


# 将获取到的文本信息保存到 txt 文件中
def write_file(description):
    with open("description.txt", 'a+', encoding='utf-8') as file:
        file.write(description)
    file.close()


get_info()
