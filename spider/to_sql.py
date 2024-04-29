# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 18:19:32 2024

@author: Doloro
"""
import os
import yaml
import sys
import fcntl
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR, Float, Integer

def get_config(var):
    curPath = os.path.dirname(os.path.abspath(__file__))
    yamlPath = os.path.join(curPath, "config.yaml")
    with open(yamlPath,'r') as f:
        fcntl.flock(f,fcntl.LOCK_SH)  
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
        sql_database_config=config['sql_database_config']
        fcntl.flock(f,fcntl.LOCK_UN)
    user = sql_database_config['user']
    password = sql_database_config['password']
    host = sql_database_config['host']
    port = sql_database_config['port']
    db = sql_database_config['db']
    if var == 'database':
        return user, password, host, port, db
    else:
        return config[var]
    
def write_config(key, new_value):
    yamlPath = './config.yaml'
    curPath = os.path.dirname(os.path.abspath(__file__))
    yamlPath = os.path.join(curPath, "config.yaml")
    with open(yamlPath) as f:
        fcntl.flock(f,fcntl.LOCK_SH)  
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
        config[key] = new_value
        fcntl.flock(f,fcntl.LOCK_UN)
    with open(yamlPath, 'w') as f:
        fcntl.flock(f,fcntl.LOCK_EX)  
        yaml.dump(config, f)
        fcntl.flock(f,fcntl.LOCK_UN)

def get_conn():
    try:
        user, password, host, port, db = get_config('database')
        conn = pymysql.connect(host=host,port=port,user=user,passwd=password,db=db)
        cursor = conn.cursor()
    except Exception as e:
        print("connect bangumi error: %s", str(e))
        sys.exit(1)
    return conn, cursor

def mapping_df_types(df):
    dtypedict = {}
    for i, j in zip(df.columns, df.dtypes):
        if "object" in str(j):
            dtypedict.update({i: NVARCHAR(length=512)})
        if "float" in str(j):
            dtypedict.update({i: Float(precision=2, asdecimal=True)})
        if "int" in str(j):
            dtypedict.update({i: Integer()})
    return dtypedict

def get_engine():
    user, password, host, port, db = get_config('database')
    expr = 'mysql+pymysql://'+str(user)+':'+str(password)+'@'+host+':'+str(port)+'/'+str(db)+'?charset=utf8mb4'
    try:
        engine = create_engine(expr)
    except Exception as e:
        print("get engine error: %s", str(e))
        sys.exit(1)
    else:
        return engine
    
def pd2sql(df, table, dtypedict):
    try:
        engine = get_engine()
        dtypedict = mapping_df_types(df)
        df.to_sql(table, engine, if_exists='append', index=False, dtype=dtypedict)
    except Exception as e:
        print("pd2sql error: %s", str(e))
        sys.exit(1)


