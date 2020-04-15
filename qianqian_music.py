import json
import os
from lxml import etree
import time
import requests

#下载_url = 'http://audio04.dmhmusic.com/71_53_T10052953671_128_4_1_0_sdk-cpm/cn/0209/M00/E1/B8/ChR47F33J_yAHE_JACrgf2qqnyQ634.mp3?xcode=b6c7ddc5ee2997b662f7d7f3ac08d0b04b92413'
#去掉别的参数之后的地址：  http://musicapi.taihe.com/v1/restserver/ting?method=baidu.ting.song.playAAC&songid=672865438
#原始json里面包含下载地址: http://musicapi.taihe.com/v1/restserver/ting?method=baidu.ting.song.playAAC&format=jsonp&callback=jQuery172005758230970954559_1586973302537&songid=672865438&from=web&_=1586973305533

url = 'http://music.taihe.com/top'
base_url = 'http://music.taihe.com'
song_base_url = 'http://musicapi.taihe.com/v1/restserver/ting?method=baidu.ting.song.playAAC&songid='
result = requests.get(url).content.decode()
#print(result)
dom = etree.HTML(result)
song_ids = dom.xpath('//dd/a[@href]/@href')[:-2]
song_names = dom.xpath('//dd/a[@href]/text()')[:-2]
#print(song_ids)
#print(song_names)


for song_id, song_name in zip(song_ids, song_names):
    #time.sleep(0.0001)
    sub_url = base_url + song_id
    #print(base_url + song_id)
    #print(song_name)
    sub_text = requests.get(sub_url).content.decode()
    #print(sub_text)
    sub_dom = etree.HTML(sub_text)

    #第一种方法:contains对属性进行查找
    #sub_song_ids = sub_dom.xpath('//a[contains(@href,"/song/")]/@href')[1:]
    #sub_song_names = sub_dom.xpath('//a[contains(@href,"/song/")]/text()')[1:]

    #第二种方法:xpath定位
    sub_song_ids = sub_dom.xpath('//span[@class="song-title "]/a[1]/@href')
    sub_song_names = sub_dom.xpath('//span[@class="song-title "]/a[1]/text()')

    print(len(sub_song_ids))
    print(len(sub_song_names))

    for sub_song_id, sub_song_name in zip(sub_song_ids, sub_song_names):
        if '/' in sub_song_name:
            sub_song_name.replace('/', '')
        sub_song_url = requests.get(song_base_url + sub_song_id.split('/')[-1]).content
        #print(sub_song_url)
        dict_url = json.loads(sub_song_url)
        result = dict_url['bitrate']['show_link']
        song = requests.get(result).content  #音乐

        #创建目录
        file_path = f'./BaiduMusic/{song_name}'
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        #保存数据
        print(song_name, sub_song_name)
        with open(f'{file_path}/%s.mp3'%sub_song_name, 'wb') as file:
            file.write(song)



