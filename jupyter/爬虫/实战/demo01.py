from bs4 import BeautifulSoup
import requests
import sys
import requests
from urllib import request
import time

kw = '西安建筑科技大学'
red_tag = 'i2937740099'

#获取将要访问的所有网址
def init_addr():
	address = []
	i = 0
	while i < 1000:
		url2 = 'http://tieba.baidu.com/f?kw='+kw+'&ie=utf-8&pn='+str(i)
		address.append(url2)
		i += 50
	return address
	
#获取该网址所在html 
def get_html_data(url):
	print(url)
	html = requests.get(url).text
	sp = BeautifulSoup(html,'html.parser')
	return sp

#获取该网页中所有帖子的网址
def find_href(url):
	hrefs=[]
	file = open('所有帖子的网址.txt','a',encoding='utf-8')
	sp = get_html_data(url)
	all_links = sp.find_all('a')
    #检	查该网页中所有帖子的网址
	for link in all_links:
		href = link.get('href')
		if href != None and href.startswith('/p/'):
			href = 'http://tieba.baidu.com' + href
			hrefs.append(href)
			file.write(href + '\n')
	return hrefs
	
	
#解析每个帖子	
def parser_tiezi(url):
	file = open('帖子的内容.txt','a',encoding='utf-8')
	file2 = open('用户.txt','a',encoding='utf-8')
	sp = get_html_data(url)
	titles = sp.find_all('cc')
	#解析出用户名
	imgs = sp.find_all('img')
	imgs = sp.find_all('img')
	for img in imgs:
		username = img.get('username')
		img_src = img.get('src')
		if username != None:	
			file2.write(username + ':' + img_src + '\n')
			# 将远程数据下载到本地，第二个参数就是要保存到本地的文件名
			request.urlretrieve(img_src,filename = 'F:/Image/'+ str(int(time.time())) +'.jpg')
	zhuti = sp.find('h1').get_text()
	file.write("******主题***********"+'\n'+ zhuti + '\n')
	i = 0
	for title in titles:
		title = title.get_text()
		if i > 0:
			file.write('回复'+ str(i) + ':' + title.lstrip() + '\n')
		else:
			file.write("********标题**********"+'\n'+ title.lstrip() + '\n')
		i += 1
	
		
if __name__ == '__main__':
#获取将要访问的所有网址,并保存至文件
	address = init_addr()
	file = open('将要访问的网址.txt','w',encoding='utf-8')
	for addr in address:
		file.write(addr + '\n')
	#逐个遍历已存在网页，将帖子的网址放入列表tiezi_links
	tiezi_links = []
	for addr in address:
	#获取当前网页的所有帖子网址
		hrefs = find_href(addr)
		for href in hrefs:
			tiezi_links.append(href)
	#解析每个网页中的内容
	for link in tiezi_links:
		parser_tiezi(link)
	
	
	
	
	