'''
Created on 12 de nov de 2016

@author: Claudio Big Data
'''
import sys, json
from Help.OptionsLoad import ConsoleHelper

class CountryFileNormalize(object):
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
    
    def run(self):
        print(self.configuration)
        self.load_node_details()
        
    def load_node_details(self):
        self.node_details = {}
        
if __name__ == '__main__':
    args = sys.argv[1:]
    console_helper = ConsoleHelper()
    options = console_helper.parse_args(args)
#     print(options)
    configFilePath = options.get("ConfigFile")
    if configFilePath is None :
        print("Does not have configFile parameter")
        sys.exit(2)
    instance = CountryFileNormalize(configFilePath)
    instance.run()