# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 14:26:12 2022

@author: franc
"""

import pyodbc
import mariadb as mdb
import pandas as pd
from datetime import datetime
import numpy as np
import os




class dbhandler:
    
    
    def __init__(self,conn,dbtype):
        
        self.conn = conn
        self.dbtype = dbtype
        
        self.cur = self.conn.cursor()
        
        try: 
            self.cur.execute("USE rapidb ;")
        except:
            self.cur.execute("CREATE DATABASE rapidb ;")
            self.cur.execute("USE rapidb ;")
        
        self.table_memory = []
        
        
    def insert_row(self,table_name,values):
        
        # Check if table was already called
        if( (table_name in self.table_memory) == False ):
            
            self.table_memory.append(table_name)
            
            try:
                if self.dbtype == "mssql":
                    self.cur.execute(f"""
                                        CREATE TABLE {table_name}
                                        (
                                            id INT IDENTITY(1,1) PRIMARY KEY,
                                            date_time DATETIME DEFAULT CURRENT_TIMESTAMP
                                        );    
                                    """)
                elif self.dbtype == "mariadb":
                    self.cur.execute(f"""
                                        CREATE TABLE IF NOT EXISTS {table_name}
                                        (
                                            id INT AUTO_INCREMENT PRIMARY KEY,
                                            date_time DATETIME(6) DEFAULT CURRENT_TIMESTAMP
                                        );    
                                    """)
            except:
                0
        
        # Query beginning
        if(self.dbtype == "mssql"):
            query_part1 = f" INSERT INTO {table_name} ("
            query_part2 = """ VALUES ( """
            
        elif(self.dbtype == "mariadb"):
            query_part1 = f" INSERT INTO {table_name} (date_time,"
            query_part2 = f""" VALUES ("{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}","""    
            
        # Query data insertion
        all_keys = []
        for key in list(values.keys()):
            key = key.replace(' ','_').lower()
            all_keys.append(key)
            query_part1 = query_part1 + key + ","
            valm = values[key]
            if( isinstance(valm, str) ):
                valm = values[key].replace("'","\\'")
            query_part2 = query_part2 + f"""'{valm}',"""
            
        # Query completion
        query_part1 = query_part1[:-1]
        query_part2 = query_part2[:-1]
        query_total = query_part1 + ") " + query_part2 + ") "
        
        try:
            self.cur.execute(query_total)
            
        except:
            
            # List columns
            if(self.dbtype == "mssql"):
                self.cur.execute(f"""SELECT *
                                    FROM INFORMATION_SCHEMA.COLUMNS
                                    WHERE TABLE_NAME = N'{table_name}'""")
                all_columns = self.cur.fetchall()
                all_columns = list(np.array(all_columns).flatten())
            elif(self.dbtype == "mariadb"):
                self.cur.execute(f"SHOW COLUMNS FROM {table_name}")
                all_columns = self.cur.fetchall()
                all_columns = list(np.array(all_columns)[:,0])
                
            # Add missing columns
            for key in all_keys:
                key = key.replace(' ','_').lower()
                if( ( key in all_columns ) == False ):
                    
                    if( isinstance(values[key],str) ):
                        typec = "TEXT"
                    elif( isinstance(values[key],float) | isinstance(values[key],int) ):
                        typec = {"mssql":"FLOAT","mariadb":"DOUBLE"}[self.dbtype]
                    else:
                        raise "TYPE ERROR"
                    
                    if(self.dbtype == "mssql"):
                        self.cur.execute(f"ALTER TABLE {table_name} ADD {key} {typec}")
                    elif(self.dbtype == "mariadb"):
                        self.cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {key} {typec}")
            
            # Call again row insertion
            self.cur.execute(query_total)
            
                
    def get_DataFrame(self,table_name):
        return pd.read_sql(f"SELECT * FROM {table_name}",self.conn,index_col="id")
    


    


class mssql(dbhandler):
    
    def __init__(self,
                 server=None,
                 user_id=None,
                 password=None):
        
        if server is None:
            server = os.environ['COMPUTERNAME'] + "\SQLEXPRESS"
        
        add_conn = ""
        if(user_id is not None):
            add_conn = add_conn + "User Id="+user_id+";"
        if(password is not None):
            add_conn = add_conn + "Password="+password+";"
        
        conn = pyodbc.connect('Driver={SQL Server};'+\
                                      'Server={'+server+'};'+\
                                      'Trusted_Connection=yes;'+add_conn
                              ,autocommit=True)
        
        dbhandler.__init__(self,conn,"mssql")



class mariadb(dbhandler):
    
    def __init__(self,
                 user="root",
                 host="127.0.0.1",
                 port=3306,
                 password=""):
        
        conn = mdb.connect(
                        user=user,
                        host=host,
                        port=port,
                        password=password,
                        autocommit=True
                    )
        
        dbhandler.__init__(self,conn,"mariadb")
        