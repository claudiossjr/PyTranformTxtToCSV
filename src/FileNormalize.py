'''
Created on 11 de nov de 2016

@author: Claudio Big Data
'''
import sys, json, glob, os
from Help.OptionsLoad import ConsoleHelper


class NormalizeFile(object):
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
        
    def run (self):
        os.chdir(self.configuration["InputFolder"])
        metric = self.configuration["Metrics"]
        files_search_key = str.format("{0}-*.txt",metric)
        files_list = glob.glob(files_search_key)
        
        for filePath in files_list:
            fileNameElems = str(filePath).replace(".txt", "").split("-")
            
            #If file name is not on right format
            if len(fileNameElems) != 7:
                old_file_path = os.path.join(self.configuration["InputFolder"], filePath)
                err_file_path = os.path.join(self.configuration["ErrorFolder"], filePath)
                os.rename(old_file_path, err_file_path)
                continue
                
            metrics = fileNameElems[0]
            
            datePosition = len(fileNameElems)-3
            year,month,day = fileNameElems[datePosition:]
            #print(str.format("{0} {1} {2} {3}", metrics, year, month, day))
            
            old_file_path = os.path.join(self.configuration["InputFolder"], filePath)
            work_file_path = os.path.join(self.configuration["WorkFolder"], filePath)
            os.rename(old_file_path, work_file_path)
            
            dictionary = self.work_on_file(filePath)
            
            outFile = str.format("{0}-{1}-{2}-{3}.txt", metrics, year, month, day)
            outFile = os.path.join(self.configuration["OutputFolder"], outFile)
            
            file_writer = open(outFile, "w")
            
            for key in dictionary.keys():
                list_values = dictionary[key]
                sumer,count_elems = self.get_sum(list_values)
                if count_elems == 0:
                    continue
                avr = sumer/count_elems
                file_writer.write(str.format("{0},{1}\n", key, avr))
                
            file_writer.close()
            
    def get_sum(self, list_values):
        sum_value = -1
        count_elems = 0
        for value in list_values:
            if value != '.':
                try:
                    number = float(value)
                    sum_value += number
                    count_elems += 1
                except BaseException:
                    continue
        if sum_value != -1:
            return sum_value + 1, count_elems
        return sum_value, count_elems
    
    def work_on_file(self, filePath):
        work_file_path = os.path.join(self.configuration["WorkFolder"], filePath)
        file_content = open(work_file_path, "r", encoding="utf-8")    
        
        full_content_dictionary = {}
        print(filePath)
        
        try:
            
#             for line in file_content:
            line = file_content.readline();
            while line:
                
                try:
                    line = file_content.readline()
                except BaseException:
                    continue
                
                
                line_elems = str(line).split(" ")
                
                if len(line_elems) < 28:
                    continue
                
                destination = line_elems[1]
                metrics_count = len(line_elems)-2
                metrics_values = line_elems[2:metrics_count]
                
                dict_list = full_content_dictionary.get(destination) 
                if not(dict_list is None):
                    for value in metrics_values :
                        full_content_dictionary[destination].append(value)
                else:
                    dict_list = metrics_values
                    full_content_dictionary[destination] = dict_list
        except BaseException:
            file_content.close()
            if len(full_content_dictionary) <= 0:
                err_file_path = os.path.join(self.configuration["ErrorFolder"], filePath)
                os.rename(work_file_path, err_file_path)
            else:
                print(len(full_content_dictionary.keys()))
            return full_content_dictionary
        
        print(len(full_content_dictionary.keys()))
        file_content.close()
        
        return full_content_dictionary
            
if __name__ == '__main__' :
    args = sys.argv[1:]
    console_helper = ConsoleHelper()
    options = console_helper.parse_args(args)
    print(options)
    configFilePath = options["ConfigFile"]
    instance = NormalizeFile(configFilePath)
    instance.run() 
    
    