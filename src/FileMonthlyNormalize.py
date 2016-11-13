'''
Created on 11 de nov de 2016

@author: Claudio Big Data
'''
import sys, json, os, glob
from Help.OptionsLoad import ConsoleHelper

class MonthlyNormalize:
    
    def __init__(self, configFilePath):
        file = open(configFilePath, "r")
        jsonData = ""
        for line in file:
            jsonData += line
        
        self.configuration = json.loads(jsonData)
        
        
    def run(self):
        os.chdir(self.configuration["InputFolder"])
        start_year = self.configuration["YearBegin"]
        end_year = self.configuration["YearEnd"]
        metric = self.configuration["Metrics"]
        for year in range(start_year, end_year+1):
            for month in range(1, 13):
                if month < 10:
                    month = str.format("0{0}", month)
                search_file_key = str.format("{0}-*-{1}-{2}-*.txt", metric, year, month)
                files_list = glob.glob(search_file_key)
                
                if(len(files_list) == 0):
                    continue
                
                month_dictionary = self.get_month_avr_from_file_list(files_list)
                
                fileName = str.format("{0}-{1}-{2}.txt", self.configuration["Metrics"], year, month)
                file_out_path = os.path.join(self.configuration["OutputFolder"], fileName)
                file_writer = open(file_out_path, "w")
                print(fileName)
                
                for key in month_dictionary.keys():
                    list_values = month_dictionary.get(key)
                    sum = self.get_sum(list_values)
                    avrg = float(sum/len(list_values))
                    
                    line = str.format("{0},{1}\n", key, avrg)
                    file_writer.write(line)
                
#                 print(str.format("{0} {1}", year, month))
    def get_sum(self, list_values):
        sum_value = 0
        for value in list_values:
            if value != '.':
                try:
                    number = float(value)
                    sum_value += number
                except BaseException:
                    continue
        return sum_value
               
    def get_month_avr_from_file_list(self, file_list):
        averages_dictionary = {}
        for fileName in file_list:    
            
            base_file_path = os.path.join(self.configuration["InputFolder"], fileName)
            work_full_path = os.path.join(self.configuration["WorkFolder"], fileName)
            os.rename(base_file_path, work_full_path)                
            
            file_reader = open(work_full_path, "r")
            
            for line in file_reader:
                elems= line.split(",")
                
                key = elems[0]
                value = float(elems[1])
                
                if not(key in averages_dictionary.keys()):
                    list = []
                    list.append(value)
#                     print (list)
                    averages_dictionary[key] = list
#                     print(averages_dictionary)
                else:
                    elem = averages_dictionary.get(key)
                    elem.append(value)
#                     print(elem)
                    averages_dictionary[key] = elem
#                     print(averages_dictionary)
                    
#             print(averages_dictionary)
        
        return averages_dictionary
if __name__ == '__main__':
    args = sys.argv[1:]
    console_helper = ConsoleHelper()
    options = console_helper.parse_args(args)
#     print(options)
    configFilePath = options.get("ConfigFile")
    if configFilePath is None :
        print("Does not have configFile parameter")
        sys.exit(2)
    instance = MonthlyNormalize(configFilePath)
    instance.run()