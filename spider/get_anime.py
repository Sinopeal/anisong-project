"""
获取所有的歌手信息
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def save_anime_rank(headers,page):
    params = {'sort':'rank','page': page}
    r = requests.get('https://bangumi.tv/anime/browser',headers=headers,params=params)
    if r.status_code!=200:
        return 'request status code:' + str(r.status_code)
    # 网页解析
    soup = BeautifulSoup(r.content.decode(), 'html.parser')
    body = soup.body
    
    #初始化dataframe
    df=pd.DataFrame(columns=['subject_id','rank','title','originaltitle','info','rate','rate_num','link','img'])
    df['rank']=df['rank'].astype(int)
    df['rate']=df['rate'].astype(float)
    
    #处理爬取的内容
    re_anime=re.compile('clearit')
    animes=body.find_all('li',attrs={'class':re_anime})
    for i in range(len(animes)):
        anime_rank = int(animes[i].find_all('span',attrs={'class':'rank'})[0].contents[1])
        anime_title = str(animes[i].select('.l')[0].contents[0])
        anime_originaltitle_tmp = animes[i].select('h3 > small')
        if anime_originaltitle_tmp != []:
            anime_originaltitle = str(anime_originaltitle_tmp[0].contents[0])
        else:
            anime_originaltitle = ''
        anime_info = animes[i].select('p',class_ = 'info tip')[0].contents[0].strip("\n ")
        anime_rate = float(animes[i].select('p > small')[0].contents[0])
        anime_rate_num = animes[i].select('p > span')[1].contents[0].strip('()')
        anime_link = 'bangumi.tv'+animes[i].select('.l')[0].get('href')
        anime_img = animes[i].select('img')[0].get('src')
        anime_subject_id = re.findall(r'\d+',anime_link)
        new_row={'subject_id':anime_subject_id,'rank':anime_rank,'title':anime_title,
                 'originaltitle':anime_originaltitle,'info':anime_info,'rate':anime_rate,
                 'rate_num':anime_rate_num,'link':anime_link,'img':anime_img}
        df = pd.concat([df,pd.DataFrame(new_row,index=[24*(page-1)+i])])
    return df




        
        
    