import requests
import re
import random
import configparser
#import  json, ssl, urllib.request
#import  urllib.request,csv
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from imgurpython import ImgurClient
from urllib.request import urlretrieve
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
#PTT 表特版 近期大於 10 推的文章 此功能尚未開放
app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
handler = WebhookHandler(config['line_bot']['Channel_Secret'])
client_id = config['imgur_api']['Client_ID']
client_secret = config['imgur_api']['Client_Secret']
album_id = config['imgur_api']['Album_ID']
API_Get_Image = config['other_api']['API_Get_Image']


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return '哈囉! 阿叔'


def pattern_mega(text):
    patterns = [
        'mega', 'mg', 'mu', 'ＭＥＧＡ', 'ＭＥ', 'ＭＵ',
        'ｍｅ', 'ｍｕ', 'ｍｅｇａ', 'GD', 'MG', 'google',
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

'''
def eyny_movie():
    target_url = 'http://www.eyny.com/forum-205-1.html'
    print('Start parsing eynyMovie....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ''
    for titleURL in soup.select('.bm_c tbody .xst'):
        if pattern_mega(titleURL.text):
            title = titleURL.text
            if '11379780-1-3' in titleURL['href']:
                continue
            link = 'http://www.eyny.com/' + titleURL['href']
            data = '{}\n{}\n\n'.format(title, link)
            content += data
    return content


def apple_news():
    target_url = 'https://tw.appledaily.com/new/realtime'
    print('Start parsing appleNews....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('.rtddt a'), 0):
        if index == 5:
            return content
        link = data['href']
        content += '{}\n\n'.format(link)
    return content
'''

def drama():
    target_url = 'https://777tv.app/vod/type/id/20.html'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for index, data in enumerate(soup.select('div.myui-vodlist__detail h4 a')):
        if index == 20:
            return content       
        title = data.text
        link =  data['href']
        abc="https://777tv.app"
        link=abc+link
        
        content += '{}\n{}\n'.format(title, link)
        
    return content

def jack():
    target_url = 'https://www.jkforum.net/forum-574-1.html'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for index, data in enumerate(soup.select('div.c a')):
        
        if index == 20:
            return content       
        title = data.text
        link =  data['style']
        content += '{}\n{}\n'.format(title, link)

    return content

def dramat():
    
    target_url = 'https://777tv.app/vod/type/id/14.html'
    print('Start dramataiwan ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""

    for index, data in enumerate(soup.select('div.myui-vodlist__detail h4 a')):
        if index == 12:
            return content
        title = data.text
        link = data['href']
        abc="https://777tv.app"
        link=abc+link
        content += '{}\n{}\n\n'.format(title, link)
    return content

def dramac():
    res = requests.get('https://777tv.app/vod/show/id/13.html',
    headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
    })
    #res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""

    for data in enumerate(soup.select('div.myui-vodlist__detail h4 a')):
        title = data.text
        link = data['href']
        abc="https://777tv.app"
        link=abc+link
        content += '{}\n{}\n\n'.format(title, link)
    return content

def movie777():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    
    target_url = 'https://dogevod.com/browse/movies.html'
    print('Start movie777 ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""

    for index, data in enumerate(soup.select('div.myui-vodlist__detail h4 a')):
        if index == 12:
            return content
        title = data.text
        link = data['href']
        abc="https://dogevod.com"
        link=abc+link
        content += '{}\n{}\n\n'.format(title, link)
    return content

def invoice():

    res = requests.get("https://bluezz.com.tw")
    soup = BeautifulSoup(res.text,'html.parser')    

    for img in soup.select('img'):
        match = re.search(r'<img alt=.*(https:.*\.jpg)',str(img))
        if match:
            # print(match.group(1))
            return str(match.group(1))

def movieo():
    target_url = 'https://movies.yahoo.com.tw/'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for index, data in enumerate(soup.select('div.movielist_info h2 a')):
        if index == 20:
            return content       
        title = data.text
        link =  data['href']
        content += '{}\n{}\n'.format(title, link)
    return content

def apple_news2():
    target_url = 'https://www.ettoday.net/news/news-list.htm'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for index, data in enumerate(soup.select('div.part_list_2 h3 a')):
        if index == 20:
            return content       
        title = data.text
        link =  data['href']
        abc='https://www.ettoday.net'
        link= abc + link
        content += '{}\n{}\n'.format(title, link)
    return content

def sag():
    print('Start dram ...')
    res = requests.get('https://www.elle.com/tw/starsigns/today/a21346791/sagittarius-today/',
    headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    })
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""

    for index, data in enumerate(soup.select('div.standard-body ul')):
        title = data.text
        
        
    return title

def sky():
    print('Start dra...')
    res = requests.get('https://www.elle.com/tw/starsigns/today/a21533471/libra-today/',
    headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    })
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""

    for index, data in enumerate(soup.select('div.standard-body ul')):
        title = data.text
        
        
    return title

def moo():
    print('Start dra...')
    res = requests.get('def sky():
    print('Start dra...')
    res = requests.get('https://www.elle.com/tw/starsigns/today/a21533471/libra-today/',
    headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    })
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""

    for index, data in enumerate(soup.select('div.standard-body ul')):
        title = data.text
        
        
    return title',
    headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    })
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""

    for index, data in enumerate(soup.select('div.standard-body ul')):
        title = data.text
        
        
    return title

def aqu():
    print('Start drac ...')
    res = requests.get('https://www.elle.com/tw/starsigns/today/a21265913/aquarius-today/',
    headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    })
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    

    for index, data in enumerate(soup.select('div.standard-body ul')):
        title = data.text
        #link = data['href']
        #abc="https://777tv.app"
        #link=abc+link
        
    return title

def sport_news():
    target_url = 'https://www.sportsv.net/'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for index, data in enumerate(soup.select('div.item_lish h4 a')):
        if index == 20:
            return content       
        title = data.text
        link =  data['href']
        content += '{}\n{}\n'.format(title, link)
    return content

def sport2020():
    target_url = 'https://www.sportsv.net/'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for index, data in enumerate(soup.select('div.list')):
        if index == 20:
            return content       
        title = data.text
        link =  data['href']
        content += '{}\n{}\n'.format(title, link)
    return content

def get_page_number(content):
    start_index = content.find('index')
    end_index = content.find('.html')
    page_number = content[start_index + 5: end_index]
    return int(page_number) + 1


def craw_page(res, push_rate):
    soup_ = BeautifulSoup(res.text, 'html.parser')
    article_seq = []
    for r_ent in soup_.find_all(class_="r-ent"):
        try:
            # 先得到每篇文章的篇url
            link = r_ent.find('a')['href']
            if link:
                # 確定得到url再去抓 標題 以及 推文數
                title = r_ent.find(class_="title").text.strip()
                rate = r_ent.find(class_="nrec").text
                url = 'https://www.ptt.cc' + link
                if rate:
                    rate = 100 if rate.startswith('爆') else rate
                    rate = -1 * int(rate[1]) if rate.startswith('X') else rate
                else:
                    rate = 0
                # 比對推文數
                if int(rate) >= push_rate:
                    article_seq.append({
                        'title': title,
                        'url': url,
                        'rate': rate,
                    })
        except Exception as e:
            # print('crawPage function error:',r_ent.find(class_="title").text.strip())
            print('本文已被刪除', e)
    return article_seq


def crawl_page_gossiping(res):
    soup = BeautifulSoup(res.text, 'html.parser')
    article_gossiping_seq = []
    for r_ent in soup.find_all(class_="r-ent"):
        try:
            # 先得到每篇文章的篇url
            link = r_ent.find('a')['href']

            if link:
                # 確定得到url再去抓 標題 以及 推文數
                title = r_ent.find(class_="title").text.strip()
                url_link = 'https://www.ptt.cc' + link
                article_gossiping_seq.append({
                    'url_link': url_link,
                    'title': title
                })

        except Exception as e:
            # print u'crawPage function error:',r_ent.find(class_="title").text.strip()
            # print('本文已被刪除')
            print('delete', e)
    return article_gossiping_seq

def beauty_hot():
    random_page = random.randint(2250,2264)
    # print(random_page)

    # https://webptt.com/m.aspx?n=bbs/Beauty/index2264.html
    # print("程式進入")
    res = requests.get("https://webptt.com/m.aspx?n=bbs/Beauty/index"+str(random_page)+'.html')
    soup = BeautifulSoup(res.text,'html.parser')

    beauty_gril_article = []
    beauty_gril_url = []
    # <a href="./m.aspx?n=bbs/Beauty/M.1504596296.A.331.html">[正妹] 台北雙層巴士</a>
    # print("執行第一迴圈")
    for a_tag in soup.select('a'):
        # print(a_tag)
        match = re.search(r'.*href="\./m\.aspx\?n=bbs/Beauty/M(.*?)">\[正妹\]',str(a_tag))
        if match:
            # print(match.group(1))
            beauty_gril_article.append('https://webptt.com/m.aspx?n=bbs/Beauty/M'+match.group(1))
            # https://webptt.com/m.aspx?n=bbs/Beauty/M.1504590665.A.10B.html

    # print(beauty_gril_article)

    # for url in beauty_gril_article:

    while True:
        res = requests.get(beauty_gril_article[(random.randint(0,len(beauty_gril_article)-1))])
        soup = BeautifulSoup(res.text,'html.parser')

        # beauty_target = 5
        # beauty_counter = 0
        # print("執行第二迴圈")
        for a_tag in soup.select('a'):
            # print(div_tag)
            match_img = re.findall(r'href="(http.*?.jpg)"',str(a_tag))
            if match_img:
                # beauty_counter += 1
                beauty_gril_url.append(match_img)
                # print(match_img)
                # if beauty_counter == beauty_target:
                #     break
                # break
        if len(beauty_gril_url)!=0:
            break


    # print(len(beauty_gril_url)-1)
    random_range = random.randint(0,len(beauty_gril_url)-1)
    final_url = ''.join(beauty_gril_url[random_range])
    # print(final_url)
    if final_url[4]!='s':
        final_url = final_url.replace('http', 'https')
    
    return final_url

def ptt_gossiping():
    rs = requests.session()
    load = {
        'from': '/bbs/Gossiping/index.html',
        'yes': 'yes'
    }
    res = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=load)
    soup = BeautifulSoup(res.text, 'html.parser')
    all_page_url = soup.select('.btn.wide')[1]['href']
    start_page = get_page_number(all_page_url)
    index_list = []
    article_gossiping = []
    for page in range(start_page, start_page - 2, -1):
        page_url = 'https://www.ptt.cc/bbs/Gossiping/index{}.html'.format(page)
        index_list.append(page_url)

    # 抓取 文章標題 網址 推文數
    while index_list:
        index = index_list.pop(0)
        res = rs.get(index, verify=False)
        # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
        if res.status_code != 200:
            index_list.append(index)
            # print u'error_URL:',index
            # time.sleep(1)
        else:
            article_gossiping = crawl_page_gossiping(res)
            # print u'OK_URL:', index
            # time.sleep(0.05)
    content = ''
    for index, article in enumerate(article_gossiping, 0):
        if index == 15:
            return content
        data = '{}\n{}\n\n'.format(article.get('title', None), article.get('url_link', None))
        content += data
    return content


def ptt_beauty():
    rs = requests.session()
    res = rs.get('https://www.ptt.cc/bbs/Beauty/index.html', verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    all_page_url = soup.select('.btn.wide')[1]['href']
    start_page = get_page_number(all_page_url)
    page_term = 2  # crawler count
    push_rate = 10  # 推文
    index_list = []
    article_list = []
    for page in range(start_page, start_page - page_term, -1):
        page_url = 'https://www.ptt.cc/bbs/Beauty/index{}.html'.format(page)
        index_list.append(page_url)

    # 抓取 文章標題 網址 推文數
    while index_list:
        index = index_list.pop(0)
        res = rs.get(index, verify=False)
        # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
        if res.status_code != 200:
            index_list.append(index)
            # print u'error_URL:',index
            # time.sleep(1)
        else:
            article_list = craw_page(res, push_rate)
            # print u'OK_URL:', index
            # time.sleep(0.05)
    content = ''
    for article in article_list:
        data = '[{} push] {}\n{}\n\n'.format(article.get('rate', None), article.get('title', None),
                                             article.get('url', None))
        content += data
    return content


def ptt_hot():
    target_url = 'http://disp.cc/b/PttHot'
    print('Start parsing pttHot....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for data in soup.select('#list div.row2 div span.listTitle'):
        title = data.text
        link = "http://disp.cc/b/" + data.find('a')['href']
        if data.find('a')['href'] == "796-59l9":
            break
        content += '{}\n{}\n\n'.format(title, link)
    return content


def moto():
    target_url = 'https://www.moto7.net/?s=NINJA+400'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for index, data in enumerate(soup.select('div.overlay h2 a')):
        if index == 20:
            return content       
        title = data.text
        link =  data['href']
        content += '{}\n{}\n'.format(title, link)
    return content

def moto1():
    target_url = 'https://www.moto7.net/?s=SUZUKI+GSX-R150'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for index, data in enumerate(soup.select('div.overlay h2 a')):
        if index == 20:
            return content       
        title = data.text
        link =  data['href']
        content += '{}\n{}\n'.format(title, link)
    return content

def moto7():
    target_url = 'https://www.moto7.net/'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for index, data in enumerate(soup.select('div.overlay h2 a')):
        if index == 20:
            return content       
        title = data.text
        link =  data['href']
        content += '{}\n{}\n'.format(title, link)
    return content

def car():
    target_url = 'https://autos.yahoo.com.tw/'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for index, data in enumerate(soup.select('div.main-news-list a')):
        title = data.text
        link =  data['href']
        content += '{}\n{}\n'.format(title, link)
    return content

def cell():
    target_url = 'https://www.eprice.com.tw/product/'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for index, data in enumerate(soup.select('div.weekly-ranking ul a')):
        if index == 20:
            return content       
        title = data.text
        link =  data['href']
        content += '{}\n{}\n'.format(title, link)
    return content

def pmpm():
    target_url = 'https://autos.yahoo.com.tw/'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for index, data in enumerate(soup.select('div.county span')):
              
        title = data.text
        link =  data['href']
        content += '{}\n{}\n'.format(title, link)
    return content


def carrank():
    target_url = 'https://autos.yahoo.com.tw/new-cars/research'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for index, data in enumerate(soup.select('divranking-right a')):
        if index == 20:
            return content       
        title = data.text
        link =  data['href']
        content += '{}\n{}\n'.format(title, link)
    return content
'''
def movie():
    target_url = 'http://www.atmovies.com.tw/movie/next/0/'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('ul.filmNextListAll a')):
        if index == 20:
            return content
        title = data.text.replace('\t', '').replace('\r', '')
        link = "http://www.atmovies.com.tw" + data['href']
        content += '{}\n{}\n'.format(title, link)
    return content
'''

def technews():
    target_url = 'https://technews.tw/'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""

    for index, data in enumerate(soup.select('article div h1.entry-title a')):
        if index == 12:
            return content
        title = data.text
        link = data['href']
        content += '{}\n{}\n\n'.format(title, link)
    return content




def panx():
    target_url = 'https://panx.asia/' #泛科技
    print('Start parsing ptt hot....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for data in soup.select('div.container div.row div.desc_wrap h2 a'):
        title = data.text
        link = data['href']
        content += '{}\n{}\n\n'.format(title, link)
    return content


def oil_price():
    target_url = 'https://gas.goodlife.tw/'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.select('#main')[0].text.replace('\n', '').split('(')[0]
    gas_price = soup.select('#gas-price')[0].text.replace('\n\n\n', '').replace(' ', '')
    cpc = soup.select('#cpc')[0].text.replace(' ', '')
    content = '{}\n{}{}'.format(title, gas_price, cpc)
    return content


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    '''
    if event.message.text.lower() == "eyny":
        content = eyny_movie()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    
    if event.message.text == "蘋果即時新聞":
        content = movie()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    
    
        
    if event.message.text == 'PTT 表特版 近期大於 10 推的文章':
        content = ptt_beauty()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    '''

    if event.message.text == "最新電影資訊":
        a=movieo()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
        return 0

    if event.message.text == "毛毛圖片":
        client = ImgurClient(client_id, client_secret)
        images = client.get_album_images(album_id)
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0
        '''
    if event.message.text == "正妹圖片":
        image = requests.get(API_Get_Image)
        url = image.json().get('Url')
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0
        '''

    if event.message.text == "正妹圖片":
        
        url=beauty_hot()

        print(url)
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0

    if event.message.text == "忍400" :
        content =moto()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "小阿魯" :
        a=moto1()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
        return 0
    if event.message.text == "摩托車" :
        a=moto7()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
        return 0

    if event.message.text == "手機" :
        a=cell()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
        return 0
    if event.message.text == "股票" :
        url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=open_data'
        webpage = urllib.request.urlopen(url)  #開啟網頁
        data = csv.reader(webpage.read().decode('utf-8').splitlines()) #讀取資料到data陣列中
        for i in data:
            print(i[1],' 漲跌價差',i[8], ' 成交筆數',i[9])
        line_bot_api.reply_message(event.reply_token,TextSendMessage(i[1],' 漲跌價差',i[8], ' 成交筆數',i[9]))

    if event.message.text == "汽車"  :
        a=car()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
        return 0

    if event.message.text == "汽車排名"  :
        a=carrank()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
        return 0

    if event.message.text == "PM2.5"  :
        url = 'https://data.epa.gov.tw/api/v1/aqx_p_432?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&sort=ImportDate%20desc&format=json'
        context = ssl._create_unverified_context()

        with urllib.request.urlopen(url, context=context) as jsondata:
             #將JSON進行UTF-8的BOM解碼，並把解碼後的資料載入JSON陣列中
            data = json.loads(jsondata.read().decode('utf-8-sig')) 

        for i in data['records']:
            #print(i['SiteName'],' AQI=',i['AQI'], ' 狀態=', i['Status'])
            a=i['SiteName'],' AQI=',i['AQI'], ' 狀態=', i['Status']
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
        return 0

    if event.message.text == "發票":
        
        url=invoice()

        print(url)
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0

    if event.message.text == "近期熱門廢文":
        content = ptt_hot()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "即時廢文":
        content = ptt_gossiping()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    
    if event.message.text == "近期上映電影":
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='此功能尚未開放'))
        return 0
    '''
    if event.message.text == "觸電網-youtube":
        target_url = 'https://www.youtube.com/user/truemovie1/videos'
        rs = requests.session()
        res = rs.get(target_url, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        seqs = ['https://www.youtube.com{}'.format(data.find('a')['href']) for data in soup.select('.yt-lockup-title')]
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=seqs[random.randint(0, len(seqs) - 1)]),
                TextSendMessage(text=seqs[random.randint(0, len(seqs) - 1)])
            ])
        return 0
    '''
    if event.message.text == "科技新報":
        content = technews()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "運動新聞":
        content = sport_news()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "PanX泛科技":
        content = panx()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    
    if event.message.text == "最新新聞":
        a=apple_news2()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
        return 0

    if event.message.text == "jack":
        a=jack()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
        return 0

    if event.message.text == "ko":
        a=drama()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
        return 0

    if event.message.text == "射手座":
        a=sag()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
        return 0

    if event.message.text == "天秤座":
        a=sky()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
        return 0

    if event.message.text == "牡羊座":
        a=moo()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
        return 0

    if event.message.text == "水瓶座":
        a=aqu()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
        return 0

    if event.message.text == "tai":
        a=dramat()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
        return 0

    if event.message.text == "chi":
        content=dramac()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0

    if event.message.text == "看電影":
        a=movie777()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
        return 0

    if event.message.text == "空氣品質":
        a=api()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
        return 0

    if event.message.text == "奧運":
        a=sport2020()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
        return 0

    if event.message.text == "幫我開燈":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='不要'))
        return 0
    if event.message.text == "開始玩":
        buttons_template = TemplateSendMessage(
            alt_text='開始玩 template',
            template=ButtonsTemplate(
                title='選擇服務',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/xQF5dZT.jpg',
                actions=[
                    MessageTemplateAction(
                        label='新聞',
                        text='新聞'
                    )
                    ,
                    MessageTemplateAction(
                        label='電影',
                        text='電影'
                    ),
                    MessageTemplateAction(
                        label='看廢文',
                        text='看廢文'
                    ),
                    MessageTemplateAction(
                        label='毛毛',
                        text='毛毛'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    if event.message.text == "新聞":
        buttons_template = TemplateSendMessage(
            alt_text='新聞 template',
            template=ButtonsTemplate(
                title='新聞類型',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/vkqbLnz.png',
                actions=[
                    
                    MessageTemplateAction(
                        label='科技新報',
                        text='科技新報'
                    ),
                    MessageTemplateAction(
                        label='PanX泛科技',
                        text='PanX泛科技'
                    ),
                    MessageTemplateAction(
                        label='Ettody新聞',
                        text='最新新聞'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    if event.message.text == "電影":
        buttons_template = TemplateSendMessage(
            alt_text='電影 template',
            template=ButtonsTemplate(
                title='服務類型',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/sbOTJt4.png',
                actions=[
                    MessageTemplateAction(
                        label='小阿魯',
                        text='小阿魯'
                    ),
                    MessageTemplateAction(
                        label='Ettoday',
                        text='最新新聞'
                    ),
                    MessageTemplateAction(
                        label='最新電影資訊',
                        text='最新電影資訊'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    if event.message.text == "看廢文":
        buttons_template = TemplateSendMessage(
            alt_text='看廢文 template',
            template=ButtonsTemplate(
                title='想看廢文嗎',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/ocmxAdS.jpg',
                actions=[
                    MessageTemplateAction(
                        label='近期熱門廢文',
                        text='近期熱門廢文'
                    ),
                    MessageTemplateAction(
                        label='即時廢文',
                        text='即時廢文'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    
    if event.message.text == "毛毛":
        buttons_template = TemplateSendMessage(
            alt_text='毛毛 template',
            template=ButtonsTemplate(
                title='選擇服務',
                text='請選擇',
                thumbnail_image_url='https://imgur.com/zN0pSfR.jpg',
                actions=[
                    MessageTemplateAction(
                        label='忍400',
                        text='忍400'
                    ),
                    MessageTemplateAction(
                        label='來張毛毛們の圖片',
                        text='毛毛圖片'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    if event.message.text == "應聲蟲 bot":
        carousel_template_message = TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://imgur.com/hUl9Y0B.jpg',
                        action=URIAction(
                            label='加我好友試玩應聲蟲',
                            uri='https://liff.line.me/1645278921-kWRPP32q?accountId=082gjlvw&openerPlatform=native&openerKey=home%3Arecommend#mst_challenge=49UsXRNkPheJ8kjMEO7dNJwIG8_bA8fU6VH7m94a8F0'
                        ),
                    ),
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            carousel_template_message)
        return 0
    if event.message.text == "油價查詢":
        content = oil_price()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    carousel_template_message = TemplateSendMessage(
        alt_text='目錄 template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/AdHZG7E.jpg',
                    title='選擇服務',
                    text='請選擇',
                    actions=[
                        MessageAction(
                            label='開始玩',
                            text='開始玩'
                        ),
                        URIAction(
                            label='大愛廣播台',
                            uri='http://daairadio.tw/Page/Home/Index.aspx'
                        ),
                        URIAction(
                            label='廣播',
                            uri='https://hichannel.hinet.net/radio/index.do?id=259'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://imgur.com/8vH3dft.jpg',
                    title='選擇服務',
                    text='請選擇',
                    actions=[
                        MessageAction(
                            label='other bot',
                            text='應聲蟲 bot'
                        ),
                        MessageAction(
                            label='油價查詢',
                            text='油價查詢'
                        ),
                        URIAction(
                            label='TVBS',
                            uri='https://www.youtube.com/watch?v=KDRwIRKP5tY'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/h4UzRit.jpg',
                    title='選擇服務',
                    text='請選擇',
                    actions=[
                        URIAction(
                            label='分享 bot',
                            uri='https://line.me/R/nv/recommendOA/@932xhoiw'
                        ),
                        URIAction(
                            label='PTT',
                            uri='https://www.ptt.cc/bbs/hotboards.html'
                        ),
                        URIAction(
                            label='羅時豐 不務正YA',
                            uri='https://www.youtube.com/channel/UCL2xWAoY0XAcAdoYiRGwMQw'
                        )
                    ]
                )
                
            ]
        )
    )

    line_bot_api.reply_message(event.reply_token, carousel_template_message)




@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    print("package_id:", event.message.package_id)
    print("sticker_id:", event.message.sticker_id)
    # ref. https://developers.line.me/media/messaging-api/sticker_list.pdf
    sticker_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 100, 101, 102, 103, 104, 105, 106,
                   107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
                   126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 401, 402]
    index_id = random.randint(0, len(sticker_ids) - 1)
    sticker_id = str(sticker_ids[index_id])
    print(index_id)
    sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id=sticker_id
    )
    line_bot_api.reply_message(
        event.reply_token,
        sticker_message)


if __name__ == '__main__':
    app.run()