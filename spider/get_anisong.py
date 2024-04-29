# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 17:59:44 2024

@author: Doloro
"""

import requests
import pandas as pd
import json

#根据接口爬取
def get_anisong_meta(subject_id,headers_api):
    url='https://api.bgm.tv/v0/subjects/'+str(subject_id)+'/subjects'
    r = requests.get(url,headers=headers_api)
    if r.status_code!=200:
        return 'request status code:' + str(r.status_code)
    data = json.loads(r.text)
    df=pd.DataFrame(columns=['type','name','song_id','subject_id','images'])
    for i in data:
        if i['relation'] in ['原声集','片头曲','片尾曲']:
            new_row={'type':i['relation'],'name':i['name'],'song_id':i['id'],
                     'subject_id':subject_id,'images':i['images']['large']}
            df = pd.concat([df,pd.DataFrame(new_row,index=[0])])
    return df
            
