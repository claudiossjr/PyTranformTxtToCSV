'''
Created on 11 de nov de 2016

@author: Claudio Big Data
'''

class MonthlyNormalize:
    
    def __init__(self):
        self.configuration = "sds"
        
    def run(self):
        print(str.format("olha meu {0}", self.configuration))

if __name__ == '__main__':
    instance = MonthlyNormalize()
    instance.run()