'''
Created on 14 de nov de 2016

@author: claudio
'''
import sys, json, os, glob
from Help.OptionsLoad import ConsoleHelper
from Help.DatabaseConnector import MySQLDAO

class FillDatabaseIndex(object):
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
        
        human_index = self.configuration["HumanIndex"]
        fileName = self.configuration["InputFile"]
        print(fileName)
        file_reader = open(fileName, "r")
        header = file_reader.readline().split(",")
        for line in file_reader:
            elems = line.replace("'", " ").replace("’", " ").replace(u"\u2018", " ").replace(u"\u2019", " ").split(",")
            if len(elems) < 2:
                continue
            print(line)
            country_name = elems[0].replace("'", " ").replace("’", " ").replace(u"\u2018", " ").replace(u"\u2019", " ")
            
            process = True
            
            elems_remain = elems[1:len(elems)]
            while process:
                process = False
                for i, elem in enumerate(elems_remain):
                    year = int(header[i+1])
                    value = elem
                    if value == '' or value == '\n': 
                        value = 0
                    else:
                        try:
                            value = float(value)
                        except BaseException as e:
                            country_name = str.format("{0}, {1}", country_name, value )
                            value = elems_remain[i+1]
                            elems_remain = elems_remain[i+1:len(elems_remain)]
                            process = True
                            break
                
                    self.db.insert_human_index(country_name, year, human_index, value)
                
            
        
if __name__ == '__main__' :
    args = sys.argv[1:]
    console_helper = ConsoleHelper()
    options = console_helper.parse_args(args)
    print(options)
    configFilePath = options["ConfigFile"]
    instance = FillDatabaseIndex(configFilePath)
    instance.run() 
    