# 导入数据请求模块
import requests
# 导入数据解析模块
import parsel
import _thread
import os
import time
name = ''
title_list = []
item_id_list = []
def get_item_id(book_id):
    global name,title_list,item_id_list
    url = 'https://fanqienovel.com/page/'+book_id+'?enter_from=stack-room'
    # 发送请求
    response = requests.get(url=url, headers=headers)
    # 获取响应的文本数据 (html字符串数据)
    html = response.text
    """解析数据: 提取我们需要的数据内容"""
    # 把html字符串数据转成可解析对象
    selector = parsel.Selector(html)
    # 提取书名
    name = selector.css('.info-name h1::text').get()
    # 提取章节名
    title_list = selector.css('.chapter-item-title::text').getall()
    # 提取章节ID
    href = selector.css('.chapter-item-title::attr(href)').getall()
    del href[0]
    for i in href:
        item_id_list.append(i.replace('/reader/',''))
    print('书名:'+name)
def get_content(title,item_id):
        # 完整的小说章节链接
        link_url = 'https://fqnovel.pages.dev/txt?item_id=' + item_id
        # 发送请求+获取数据内容
        link_data = requests.get(url=link_url, headers=headers).text
        # 把<p>转 \n 换行符
        content=link_data.replace('<p>','\n').replace('</p>','\n')
        # print(content)
        #print(link_url)
        with open('./'+ name +'/'+ title + '.txt', mode='w', encoding='utf-8') as f:
            f.write(title)
            f.write('\n\n')
            f.write(content)
            f.write('\n\n')
            f.close
        print(title+'爬取成功')

# 模拟浏览器
headers = {
    # User-Agent 用户代理, 表示浏览器/设备的基本身份信息
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    #cookie
    ,'Cookie': 'csrf_session_id=ecc1986ed4e8cdfe3a06dfe01285fa8e; s_v_web_id=verify_ly3qomo2_YbogndOi_P9uK_4NB6_8CYW_FsTfqhp6OoPd; novel_web_id=7386846545851434505; ttwid=1%7C-n-jiMa0TuCOPkCYZwrd8_Xpn9Nc2YovLKk8V4ONXv4%7C1719884402%7Cd4e110824fc3fa733e5b77bb41293daff10fc51e14be1376f440e2bb0ccc9dee; msToken=acpdNP7HJyaV7GUMudUbSdsV5y4n-xa-jGbYWEY6uBw4byUx-XT7UcAgrYzTiJeOeUCboYYpJa5o1geUcUzP-z9U12Hb9rAcP9VgxET_'
    }
# url地址(小说主页)
book_id = input('book_id:')
get_item_id(book_id)
if not os.path.exists(name):
    os.makedirs(name)
c = input('1.爬取全文\n2.爬取单章\nNext:')
if c == '1':
    #print(title_list)
    #print(href)
    # for循环遍历, 提取列表里元素
    if input('是否全文爬取(这将会爬取书籍的所有章节，若否则将会爬取未被爬取的章节)y/n(默认n):') == 'y':
        for title,item_id in zip(title_list, item_id_list):
            _thread.start_new_thread(get_content,(title,item_id))
            time.sleep(0.04125)
        input('--------------------------------------------\n总章数:'+str(len(title_list))+"\n等待所有线程下载完毕后，按下回车键\n--------------------------------------------\n")
    print('开始效验并更新文件')
    for title,item_id in zip(title_list, item_id_list):
        if os.path.exists('./'+ name +'/'+ title + '.txt'):
            print(f"{title}已创建")
        else:
            print(f'提示:{title}没有被创建')
            _thread.start_new_thread(get_content,(title,item_id))
    input('--------------------------------------------\n总章数:'+str(len(title_list))+"\n等待所有线程下载完毕后，按下回车键\n--------------------------------------------\n")
elif c == '2':
    print(title_list)
    c1 = int(input('选择:'))
    get_content(title_list[c1-1],item_id_list[c1-1])
else:
    print('unknown')
