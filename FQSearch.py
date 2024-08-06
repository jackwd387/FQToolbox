from requests import Session
import pyperclip
# Cookie
Cookie = 'csrf_session_id=ecc1986ed4e8cdfe3a06dfe01285fa8e; s_v_web_id=verify_ly3qomo2_YbogndOi_P9uK_4NB6_8CYW_FsTfqhp6OoPd; novel_web_id=7386846545851434505; ttwid=1%7C-n-jiMa0TuCOPkCYZwrd8_Xpn9Nc2YovLKk8V4ONXv4%7C1719884402%7Cd4e110824fc3fa733e5b77bb41293daff10fc51e14be1376f440e2bb0ccc9dee; msToken=acpdNP7HJyaV7GUMudUbSdsV5y4n-xa-jGbYWEY6uBw4byUx-XT7UcAgrYzTiJeOeUCboYYpJa5o1geUcUzP-z9U12Hb9rAcP9VgxET_'
# 搜索api
search_url = 'https://novel.snssdk.com/api/novel/channel/homepage/search/search/v1/'
# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Danger hiptop 3.4; U; AvantGo 3.2)',
    'Cookie': Cookie
    }


self = Session()  # 创建一个Session对象，并赋值给self
def search(self, keywords: str) -> list[dict] | str:
    """
    搜索书籍信息
    参数:
    keywords (str): 关键字
    返回:
    list: 书籍信息列表
    """
    # 获得书本基本信息
    params = {
        'aid': 1967,
        'q': keywords
    }
    book_list_info = self.get(search_url, params=params, headers=headers).json()
    return book_list_info['data']['ret_data'] if 'ret_data' in book_list_info['data'].keys() else '未配置cookie或者cookie失效'
search_content = input('搜索内容:')
search_result = (search(self,search_content))
for i in range(len(search_result)):
    print(f'No.{i+1}')
    print('title:'+search_result[i]['title'])
    
    print('abstract:'+search_result[i]['abstract'])
    
    print('author:'+search_result[i]['author'])
    
    print('book_id:'+search_result[i]['book_id'])
    
    print('thumb_url:'+search_result[i]['thumb_url'])
    
choose = int(input('请选择:'))-1
print('title:'+search_result[choose]['title'])
pyperclip.copy(search_result[choose]['book_id'])
print('已复制book_id:'+search_result[choose]['book_id'])
