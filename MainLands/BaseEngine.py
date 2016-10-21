__author__ = 'claudio'
from pathlib import Path
from Objects import NodeInfo


class TransformEngine:

    def __init__(self, destination, source, folder):
        self.__destination_node__ = destination
        self.__source_node__ = source
        self.__folder__ = folder
        self.__main_folder__ = Path(self.__destination_node__).parent
        self.__sourceInfo_dict__ = {}

    def run(self):
        self.__build_sourceInfo__()

    def __parse_dest_and_sour_file(self, file_name):
        """
        This function opens destination and source node file in order to fill node information dictionary
        """
        file_reader = open(file_name, "r")
        # temp_path = str.format("{0}/{1}", self.__main_folder__, "exitFile.txt")
        # file_writer = open(temp_path, "w+")
        for line in file_reader:
            #file_writer.write(line)
            elems = str.split(line, ",")
            if len(elems) < 9:
                continue
            node = NodeInfo(elems)
            node_name = node.get_source_name()
            if not(node_name in self.__sourceInfo_dict__.keys()):
                self.__sourceInfo_dict__[node_name] = node
        file_reader.close()

    def __build_sourceInfo__(self):
        """
        This function build dictionary that will be used to get lat/long node information
        """
        # Reading destination file
        self.__parse_dest_and_sour_file(self.__destination_node__)

        # Now, Reading source nodes file
        self.__parse_dest_and_sour_file(self.__source_node__)




