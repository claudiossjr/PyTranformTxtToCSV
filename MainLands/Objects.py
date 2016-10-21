__author__ = 'claudio'


class NodeInfo:

    __elem_dict__ = {"_id": 0,
                     "node_name": 1,
                     "node_ip": 2,
                     "latitude": 3,
                     "longitude": 4,
                     "nick_name": 5,
                     "full_name": 6,
                     "site_name": 7,
                     "project_type": 8
                    }

    def __init__(self, attrs):
        self.__id__ = attrs[self.__elem_dict__["_id"]]
        self.__node_name__ = attrs[self.__elem_dict__["node_name"]]
        self.__node_ip__ = attrs[self.__elem_dict__["node_ip"]]
        self.__latitude__ = attrs[self.__elem_dict__["latitude"]]
        self.__longitude__ = attrs[self.__elem_dict__["longitude"]]
        self.__nick_name__ = attrs[self.__elem_dict__["nick_name"]]
        self.__full_name__ = attrs[self.__elem_dict__["full_name"]]
        self.__site_name__ = attrs[self.__elem_dict__["site_name"]]
        self.__project_type__ = attrs[self.__elem_dict__["project_type"]]

    def printInfo(self):
        information = str.format("{0}   {1} {2} {3} {4} {5} {6} {7} {8}", self.__id__,
                                                                          self.__node_name__,
                                                                          self.__node_ip__,
                                                                          self.__latitude__,
                                                                          self.__longitude__,
                                                                          self.__nick_name__,
                                                                          self.__full_name__,
                                                                          self.__site_name__,
                                                                          self.__project_type__)

        print(information)

    def get_source_name(self):
        return self.__node_name__