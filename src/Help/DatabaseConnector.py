'''
Created on 14 de nov de 2016

@author: claudio
'''

import pymysql, sys, json
from Help.OptionsLoad import ConsoleHelper

class MySQLDAO(object):
    '''
    classdocs
    '''


    def __init__(self, DBConfig):
        '''
        Constructor
        '''
        host = DBConfig.get("Host")
        userName = DBConfig.get("UserName")
        passwd = DBConfig.get("Password")
        db = DBConfig.get("DBName")
        
        self.con = pymysql.connect(host=host, unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock', user=userName, passwd=passwd, db=db)

    def get_node_id(self, name):
        cur = self.con.cursor()
        query = str.format("Select idNode from Node where Node_Name = '{0}'", name)
        
        cur.execute(query)
        elem = cur.fetchone()
        cur.close()
        if not(elem is None):
            return elem[0]
        return -1
    
    def get_metric_id(self, metric_name):
        cur = self.con.cursor()
        query = str.format("Select idMetrics from Metrics where Tipo = '{0}'", metric_name)
        
        cur.execute(query)
        elem = cur.fetchone()
        cur.close()
        if not(elem is None):
            return elem[0]
        return -1
    
    def insert_human_index(self, country_name, year, human_index, value ):
        cur = self.con.cursor()
        query = str.format("INSERT INTO HumanIndex \
                                (CountryName, \
                                Year, \
                                HumanIndex, \
                                value) \
                                VALUES \
                                ('{0}', \
                                {1}, \
                                '{2}', \
                                {3})", country_name, year, human_index, value)
        cur.execute(query)
        
        try:
            self.con.commit()
        except:
            self.con.rollback()                   
        
        cur.close()       
    
    def insert_node(self, node_name, node_ip, lat, lng, country, region, site_name):
        cur = self.con.cursor()
        query = str.format("INSERT INTO Node \
                                (Node_Name, \
                                Node_IP, \
                                LAT, \
                                LNG, \
                                COUNTRY, \
                                REGION, \
                                SITE_NAME) \
                                VALUES \
                                ('{0}', \
                                '{1}', \
                                '{2}', \
                                '{3}', \
                                '{4}', \
                                '{5}', \
                                '{6}')", node_name, node_ip, lat, lng, country, region, site_name )
        cur.execute(query)
        
        try:
            self.con.commit()
        except:
            self.con.rollback()                   
        
        cur.close()         
        
        return self.get_node_id(node_name)
        
    def insert_metrics(self, tipo):
        cur = self.con.cursor()
        query = str.format("INSERT INTO Metrics \
                                (Tipo ) \
                                VALUES \
                                ('{0}')", tipo )
        cur.execute(query)

        try:
            self.con.commit()
        except:
            self.con.rollback()                   
        
        cur.close()
        
        return self.get_metric_id(tipo)
    
    def insert_has_metric(self, idMetrics, idNode, year, month, value):
        cur = self.con.cursor()
        query = str.format("INSERT INTO hasMetrics \
                        (idMetric, \
                        idNode, \
                        value, \
                        year, \
                        month) \
                        VALUES \
                        ({0}, \
                        {1}, \
                        {2}, \
                        {3}, \
                        {4})", int(idMetrics), int(idNode), float(value), int(year), int(month) )
        cur.execute(query)
        

        try:
            self.con.commit()
        except:
            self.con.rollback()                   
        
        cur.close()
    
    def close_connection(self):
        self.con.close()
    
if __name__ == '__main__':
    args = sys.argv[1:]
    console_helper = ConsoleHelper()
    options = console_helper.parse_args(args)
    print(options)
    configFilePath = options["ConfigFile"]
    
    file = open(configFilePath, "r")
    jsonData = ""
    for line in file:
        jsonData += line
    
    configInfo = json.loads(jsonData)

    
    DbConfig = configInfo["ConfigDatabase"]
    print(DbConfig)
    myclass = MySQLDAO(DbConfig)
    id = myclass.get_node_id("Joao")
    print(id)
    
    id = myclass.insert_node("dsdsa", "", "", "", "Brasil", "", "")
    print(id)
    
    metrics_id = myclass.insert_metrics("retre")
    print(metrics_id)
    
    myclass.insert_has_metric(metrics_id, id , 2016, 10, 2588.56)
    
    
    
    