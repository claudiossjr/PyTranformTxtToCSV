'''
Created on 11 de nov de 2016

@author: Claudio Big Data
'''

class ConsoleHelper(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.initialization = True
    
    def parse_args(self, args):
        args_dictionary = {}
        
        for row in args:
            elem = str(row)
            key, value = elem.split("=")
            args_dictionary[key] = value
            
        return args_dictionary