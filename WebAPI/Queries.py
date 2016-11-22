from dbconnect import connection

def queryManager(country, year_from, year_to, metric, human_index):
    c, conn = connection()
    
    query = "SELECT hm.year, avg(hm.value) FROM Node n  inner join hasMetrics hm on n.idNode = hm.idNode inner join Metrics m on m.idMetrics = hm.idMetric where n.Country = '{0}' and m.Tipo = '{1}' and (hm.year between {2} and {3}) GROUP BY hm.year "
    
    result_set_country = c.execute(str.format(query, country, metric, year_from, year_to))
    
    
    result_finalize = {}
    
    for result in c:
        year, average = result
        average = float(average)
        if not(year in result_finalize.keys()):
            result_finalize[year] = [average]
        else:
            list = result_finalize[year]
            list.append(average)
            result_finalize[year] = list
    
    result_set_human = c.execute(str.format(query, country, metric, year_from, year_to))
    
    for result in c:
        year, average = result
        average = float(average)
        if not(year in result_finalize.keys()):
            result_finalize[year] = [average]
        else:
            list = result_finalize[year]
            list.append(average)
            result_finalize[year] = list
    
    c.close()
    conn.close()
    return result_finalize