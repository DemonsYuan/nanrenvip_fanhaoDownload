import os
from bs4 import BeautifulSoup
import requests
import re
import time
import random
import datetime

headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
html=requests.get('http://nanrenvip.cc/nvyouku/ssyouya.html',headers=headers)
soup=BeautifulSoup(html.content,'lxml')
soup_text=soup.find('div',class_='zp_list').find_all('a')
actor=soup.find('div',class_='infosay fr pos-r').find('h1')   #演员名字标签
actor_name=actor.text
cur=datetime.datetime.now()               #获取时间
year=cur.year
month=cur.month
day=cur.day
downloadtime=str(cur.year)+'0'+str(cur.month)+'0'+str(cur.day)
print(downloadtime)
path='E:\\人间辞话\\'+actor_name+downloadtime                    #文件夹路径
isExists = os.path.exists(path)

# 判断结果
if not isExists:
    # 如果不存在则创建目录
    os.makedirs(path)
imagesource = []
for links in soup_text:
    a='http://nanrenvip.cc'+links.get('href')
    imagesource.append(a)
print(imagesource)
count=0
#在每个图片页面中下载图片
for i in imagesource:
    time.sleep(random.random())
    os.chdir(path)
    html = requests.get(i)
    soup = BeautifulSoup(html.content, 'lxml')
    soup_fanhao = soup.find('div', class_='artCon').find('p',text=re.compile('.*番号.*')) #获取番号标签
    soup_date = soup.find('div', class_='artCon').find('p', text=re.compile('.*日期.*'))  #获取日期标签
    soup_img = soup.find('div', class_='artCon').find('img')                              #获取图片标签
    soup_imgaddress='http://nanrenvip.cc'+soup_img.get('data-echo')                       #获取图片地址
    print(soup_fanhao.text,soup_date.text,soup_imgaddress)
    data = requests.get( soup_imgaddress, headers=headers).content  # 获取图片的二进制格式
    print(path+'\\'+soup_fanhao.text+'.jpg')
    with open(path+'\\'+soup_fanhao.text+'.jpg', 'wb') as f:
        f.write(data)
    count+=1
    print("【正在下载】 %s 共%d 张" % (soup_fanhao.text,count))
    with open(path+'\\'+'readme.txt', 'a') as f:
        f.write("【正在下载】 %s 共%d 张" % (soup_fanhao.text,count)+downloadtime+'\n')
