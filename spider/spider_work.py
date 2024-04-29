# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 20:46:57 2024

@author: Doloro
"""
import sys
from multiprocessing import Process
import random
import time
import get_anime,get_anisong,to_sql
from sqlalchemy.types import NVARCHAR

useragent_list=[
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
]

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '',
    'Host': 'bangumi.tv',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': ''
}

headers_api = {
    'User-Agent': 'sinopeal/anisong-project'  
    #使用您的User-Agent：https://github.com/bangumi/api/blob/master/docs-raw/user%20agent.md
}

def anime_work():
    print('anime_work is running...')
    page = to_sql.get_config('anime_index') #从配置中读取当前需要爬取的页数
    df = get_anime.save_anime_rank(headers , page) # test
    dtype_dict = to_sql.mapping_df_types(df)
    while True:
        try:
            sleeptime=random.uniform(2,4)
            headers['User-Agent'] = useragent_list[random.randint(0,5)]         
            df = get_anime.save_anime_rank(headers , page)
            to_sql.pd2sql(df, table='anime', dtypedict=dtype_dict)
        except Exception as e:
            print("anime_work error: %s", str(e))
            sys.exit(1)
        else:
            #更新成功爬取的页数
            page += 1
            to_sql.write_config('anime_index', page)
            time.sleep(sleeptime)

def anisong_work():
    time.sleep(3)   #根据anime表的结果决定当前爬取的anisong，延迟30s工作       
    print('anisong_work is running...')
    conn, cursor = to_sql.get_conn()
    anisong_index = to_sql.get_config('anisong_index')
    dtype_dict={'object': NVARCHAR(length=512)}
    while True:
        try:
            sleeptime=random.uniform(3,5)
            sql = 'select subject_id from anime where anime.rank = ' + str(anisong_index)
            cursor.execute(sql)
            subject_id = cursor.fetchall()
            subject_id = subject_id[0][0]
            df = get_anisong.get_anisong_meta(subject_id, headers_api)
            to_sql.pd2sql(df, table='anisong', dtypedict=dtype_dict)
        except Exception as e:
            print("anisong_work error: %s", str(e))
            sys.exit(1)
        else:
            anisong_index += 1
            to_sql.write_config('anisong_index', anisong_index)
            time.sleep(sleeptime)
            
def spider_work():
    print('spider_work is running')
    task_get_anime = Process(target = anime_work)
    task_get_anisong = Process(target = anisong_work)
    task_get_anime.start()
    task_get_anisong.start()
    task_get_anime.join()
    task_get_anisong.join()
        

if __name__ == "__main__":
    spider_work()
    
