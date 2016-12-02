import pymysql

def connection():

    conn = pymysql.connect(host="localhost", unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock', user="root", passwd="root", db="PingERVis")
    c = conn.cursor()

    return c, conn