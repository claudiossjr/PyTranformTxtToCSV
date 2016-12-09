from dbconnect import connection

def countryQuery(country, year_from, year_to, metric, human_index):
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
            
    queryHumanIndex = "SELECT hm.year, hm.value FROM HumanIndex hm where hm.CountryName like '%{0}%' and hm.HumanIndex = '{1}' and (hm.Year between {2} and {3}) "
    
    result_set_human = c.execute(str.format(queryHumanIndex, country, human_index, year_from, year_to))
    #result_set_human = c.execute(str.format(query, country, metric, year_from, year_to))

    for result in c:
        year, average = result
        average = float(average)
        if not(year in result_finalize.keys()):
            result_finalize[year] = [-1,average]
        else:
            list = result_finalize[year]
            list.append(average)
            result_finalize[year] = list
    
    c.close()
    conn.close()
    return result_finalize

def heatMapQuery(year_from, year_to, metric, human_index, op):
    c, conn = connection()
    
    result_finalize = {}
    
    if  str(op).upper().find('METRICS') >= 0:
        query = "select n.COUNTRY, avg(hm.value) from Node n inner join hasMetrics hm on hm.idNode = n.idNode inner join Metrics m on m.idMetrics = hm.idMetric where m.Tipo = '{0}' and (hm.year between {1} and {2}) GROUP BY n.COUNTRY"
        
        result_set_country = c.execute(str.format(query, metric, year_from, year_to))
        
        for result in c:
            country, average = result
            average = float(average)
            result_finalize[country] = average
            
    
    elif str(op).upper().find('INDEX') >= 0:
        queryHumanIndex = "select hi.CountryName, avg(hi.value) from HumanIndex hi where hi.HumanIndex = '{0}' and (hi.Year between {1} and {2}) GROUP BY hi.CountryName"
        
        result_set_human = c.execute(str.format(queryHumanIndex, human_index, year_from, year_to))
        #result_set_human = c.execute(str.format(query, country, metric, year_from, year_to))
    
        for result in c:
            country, average = result
            average = float(average)
            result_finalize[country] = average
            
        

    c.close()
    conn.close()
        
    return result_finalize