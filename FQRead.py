# 导入数据请求模块
import requests
# 导入数据解析模块
import parsel
import os
import time
import edge_tts
import asyncio
import _thread
name = ''
title_list = []
item_id_list = []
executable = 'False'
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
        return link_data.replace('<p>','   ').replace('</p>','   ')
def thread(p):
    global content,voice,rate_count,volume_count,executable
    print('正在爬取并生成音频')
    content = get_content(title_list[p-1],item_id_list[p-1])
    asyncio.run(run_tts(title_list[p-1]+content,voice,rate_count,volume_count))
    if executable == 'False':
        executable = 'True'
async def run_tts(text: str, voice: str,rate:str,volume:str) -> None:
    global title_list,output_files,count
    communicate =  edge_tts.Communicate(text=text, voice=voice,rate=rate,volume=volume)
    await communicate.save(output_files+title_list[p-1+count]+'_TEMP.mp3')
    print('生成'+output_files+title_list[p-1+count]+'_TEMP.mp3'+'成功')
#   模拟浏览器
headers = {
    # User-Agent 用户代理, 表示浏览器/设备的基本身份信息
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    #cookie
    ,'Cookie': 'csrf_session_id=ecc1986ed4e8cdfe3a06dfe01285fa8e; s_v_web_id=verify_ly3qomo2_YbogndOi_P9uK_4NB6_8CYW_FsTfqhp6OoPd; novel_web_id=7386846545851434505; ttwid=1%7C-n-jiMa0TuCOPkCYZwrd8_Xpn9Nc2YovLKk8V4ONXv4%7C1719884402%7Cd4e110824fc3fa733e5b77bb41293daff10fc51e14be1376f440e2bb0ccc9dee; msToken=acpdNP7HJyaV7GUMudUbSdsV5y4n-xa-jGbYWEY6uBw4byUx-XT7UcAgrYzTiJeOeUCboYYpJa5o1geUcUzP-z9U12Hb9rAcP9VgxET_'}
# url地址(小说主页)
if __name__ == '__main__':
    book_id = input('book_id:')
    get_item_id(book_id)
    c = input('选择阅读方法:\n1.pyttsx4\n2.edge-tts\n你都选择是:')
    print(title_list)
    # 阅读方法1
    if c == '1':
        import pyttsx4
        engine = pyttsx4.init()   # 初始化
        count = 0
        p = int(input('选择:'))
        voices = engine.getProperty('voices')
        for voice in voices:
            print ('id = {} \nname = {} \n'.format(voice.id, voice.name))
        s = int(input('设置语音:'))
        engine.setProperty('voice', voices[s-1].id)  #设置发音人
        rate_count = int(input('语速大小:'))
        rate = engine.getProperty('rate')   # getting details of current speaking rate
        engine.setProperty('rate', rate_count)     # setting up new voice rate

        volume_count = float(input('音量大小:'))
        volume = engine.getProperty('volume')  #getting to know current volume level (min=0 and max=1)
        engine.setProperty('volume',volume_count)    # setting up volume level  between 0 and 1
        while True:
            print('正在爬取'+title_list[p-1+count])
            content = get_content(title_list[p-1+count],item_id_list[p-1+count])
            if count+p > len(item_id_list):
                engine.say('已播放完最新章节')
                engine.runAndWait()
                break
            else:
                engine.say(title_list[p-1+count]+'\n'+content)
            print('正在播放:'+name+':'+title_list[p-1+count])
            engine.runAndWait()
            count += 1
    elif c == '2':
        p = int(input('选择:'))
        count = 0
        content = None
        title = title_list[p-1+count]
        output_files = './' + name + '_ceche/'
        os.system('edge-tts --list-voices')
        voice = input('请选择音色(默认zh-CN-XiaoxiaoNeural):')
        rate_count = input('语速大小(默认+0%):')
        volume_count = input('音量大小(默认+0%):')
        if voice == '':
            voice = 'zh-CN-XiaoxiaoNeural'
        if rate_count == '':
            rate_count = '+0%'
        if volume_count == '':
            volume_count = '+0%' 
        if not os.path.exists(output_files):
            os.makedirs(output_files)
        _thread.start_new_thread(thread,(p+count,))
        while True:
            if executable == 'True':
                title = title_list[p-1+count]
                if count+p > len(item_id_list):
                    os.system('edge-playback --text "已播放完最新章节" --voice '+ voice)
                    break
                else:
                    count += 1
                    print('即将播放:'+name+':'+title)
                    _thread.start_new_thread(thread,(p+count,))
                    os.system('mpv '+'"'+output_files+title+'_TEMP.mp3'+'"')
                    os.remove(output_files+title+'_TEMP.mp3')
            else:
                print('等待章节爬取完毕')
                time.sleep(1)
