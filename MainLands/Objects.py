__author__ = 'claudio'


class NodeInfoOut:

    def __init__(self, lat_monitor, long_monitor, monitor_name, lat_monitorado, long_monitorado, monitorado_name, date_hour, value):
        self.__lat_monitor__ = lat_monitor
        self.__long_monitor__ = long_monitor
        self.__monitor_name__ = monitor_name
        self.__lat_monitorado__ = lat_monitorado
        self.__long_monitorado__ = long_monitorado
        self.__monitorado_name__ = monitorado_name
        self.__date_hour__ = date_hour
        self.__value__ = value

    def print_info(self):
        information = str.format("{0},{1},{2},{3},{4},{5},{6},{7}", self.__lat_monitor__,
                                                                     self.__long_monitor__,
                                                                     self.__monitor_name__,
                                                                     self.__lat_monitorado__,
                                                                     self.__long_monitorado__,
                                                                     self.__monitorado_name__,
                                                                     self.__date_hour__,
                                                                     self.__value__,)

        return information


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

    def __init__(self, _attr):
        self.__id__ = _attr[self.__elem_dict__["_id"]]
        self.__node_name__ = _attr[self.__elem_dict__["node_name"]]
        self.__node_ip__ = _attr[self.__elem_dict__["node_ip"]]
        self.__latitude__ = _attr[self.__elem_dict__["latitude"]]
        self.__longitude__ = _attr[self.__elem_dict__["longitude"]]
        self.__nick_name__ = _attr[self.__elem_dict__["nick_name"]]
        self.__full_name__ = _attr[self.__elem_dict__["full_name"]]
        self.__site_name__ = _attr[self.__elem_dict__["site_name"]]
        self.__project_type__ = _attr[self.__elem_dict__["project_type"]]

    def print_info(self):
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

    def get_lat_long(self):
        return self.__latitude__, self.__longitude__

    def get_source_name(self):
        return self.__node_name__