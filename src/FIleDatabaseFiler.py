'''
Created on 14 de nov de 2016

@author: claudio
'''
import sys, json, os, glob
from Help.OptionsLoad import ConsoleHelper
from Help.DatabaseConnector import MySQLDAO

class FillDatabase(object):
    '''
    classdocs
    '''


    def __init__(self, configFilePath):
        '''
        Constructor
        '''
        file = open(configFilePath, "r")
        jsonData = ""
        for line in file:
            jsonData += line
        
        self.configuration = json.loads(jsonData)
        
        
        DbConfig = self.configuration["ConfigDatabase"]
        print(DbConfig)
        self.db = MySQLDAO(DbConfig)
        
    def run (self):
        os.chdir(self.configuration["InputFolder"])
        metric = self.configuration["Metrics"]
        files_search_key = str.format("{0}-*.txt",metric)
        files_list = glob.glob(files_search_key)
        
        for fileName in files_list:
            old_file_name = os.path.join(self.configuration["InputFolder"], fileName)
            new_file_name = os.path.join(self.configuration["WorkFolder"], fileName)
            os.rename(old_file_name, new_file_name)
            
            file_reader = open(new_file_name, "r")
            for line in file_reader:
                node_name = line[0]
                node_ip = line[1]
                lat = line[2]
                lng = line[3]
                country = line[4]
                region = line[5]
                site_name = line[6]
                metric_value = line[7]
                metric = self.configuration["Metrics"]
                
                node_id = self.db.get_metric_id(node_name)
                metric_id = self.db.get_metric_id(metric)
                
                if node_id == -1:
                    node_id = self.db.insert_node(node_name, node_ip, lat, lng, country, region, site_name)
                
                if metric_id == -1:
                    metric_id = self.db.insert_metrics(metric)
                
                elems = fileName.replace(".txt", "").split("-")
                year = int(elems[1])
                month = int(elems[2])
                
                self.db.insert_has_metric(metric_id, node_id, year, month, metric_value)
                
            break
        
if __name__ == '__main__' :
    args = sys.argv[1:]
    console_helper = ConsoleHelper()
    options = console_helper.parse_args(args)
    print(options)
    configFilePath = options["ConfigFile"]
    instance = FillDatabase(configFilePath)
    instance.run() 
    