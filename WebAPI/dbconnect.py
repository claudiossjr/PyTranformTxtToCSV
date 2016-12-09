import pymysql

def connection():

    conn = pymysql.connect(host="192.168.0.25", user="root", passwd="423123dinhU@", db="PingERVis")
    c = conn.cursor()

    return c, conn