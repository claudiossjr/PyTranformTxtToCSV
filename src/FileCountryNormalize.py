'''
Created on 12 de nov de 2016

@author: Claudio Big Data
'''
import sys, json, os, glob
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
        print(len(self.node_details))
        os.chdir(self.configuration["InputFolder"])
        metric = self.configuration["Metrics"]
        file_search_key = str.format("{0}-*.txt", metric)
        list_files = glob.glob(file_search_key)
        
        for file_name in list_files:
            old_file_path = os.path.join(self.configuration["InputFolder"], file_name)
            new_file_path = os.path.join(self.configuration["WorkFolder"], file_name)
            os.rename(old_file_path, new_file_path)
            
            normalized_file = os.path.join(self.configuration["OutputFolder"], file_name)
            
#             print(normalized_file)
            
            file_to_read = open(new_file_path, "r")
            file_to_write = open(normalized_file, "w")
            
            for line in file_to_read:
                elems = line.split(",")
                node_name = elems[0]
                metric_value = float(elems[1])
                
                if node_name in self.node_details.keys():
                    node_detail = self.node_details.get(node_name)
                    node_detail.set_value(metric_value)
                    node_detail.write_information(file_to_write)
                    
            file_to_write.close()
            
    def load_node_details(self):
        self.node_details = {}
        file_node_details = open(self.configuration["NodeDetails"], "r")
        
        file_node_details.readline()
        i = 0
        for line in file_node_details:
            elems = line.split(",")
            
            if len(elems) > 7:
                i += 1
                continue
            
            node_name = elems[0].replace("\n","")
#             if elems[4].replace("\n","") == "" or elems[4].replace("\n","") == "NOT-SET":
#                 continue
            node_details = NodeDetail(elems)
            
            self.node_details[node_name] = node_details
            
        print(self.node_details)
        print(i)

class NodeDetail:
    
    def __init__(self, elems):
        self.node_name = elems[0].replace("\n","")
        self.node_ip = elems[1].replace("\n","")
        self.lat = elems[2].replace("\n","")
        self.lng = elems[3].replace("\n","")
        self.country = elems[4].replace("\n","")
        self.region = elems[5].replace("\n","")
        if len(elems) > 6:
            self.site_name = elems[6].replace("\n","")
        else:
            self.site_name = ""
        self.value = 0        
    
    def set_value(self, new_value):
        self.value = new_value
    
    def write_information(self, file_to_write):
        info = str.format("{0},{1},{2},{3},{4},{5},{6},{7}\n", self.node_name, self.node_ip, self.lat, self.lng, self.country, self.region, self.site_name, self.value)
        file_to_write.write(info)

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