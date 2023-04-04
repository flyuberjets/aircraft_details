
def generate_tail_sitemap():
    import configparser
    conf = configparser.ConfigParser()
    conf.read('conf.ini')
    from simple_salesforce import Salesforce
    sf = Salesforce(username=conf['SALESFORCE']['username'], instance=conf['SALESFORCE']['instance'], password=conf['SALESFORCE']['password'], security_token=conf['SALESFORCE']['security_token'])
    sql = f"select Name from Aircraft_Tail__c WHERE Aircraft_Type__c != null"
    results = sf.bulk.Aircraft_Tail__c.query(sql)
    #print(results)
    url_entries = ""
    for record in results:
        url_entries+= f"""   
            <url>
                <loc>https://flyuberjets.com/aircraft/{record['Name']}</loc>
            </url>"""
    

    sitemap=f'''<?xml version="1.0" encoding="UTF-8"?>

    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

        {url_entries}

    </urlset> '''
    
    f = open("tail_map.xml", "w", encoding="utf-8")
    f.write(sitemap)
    f.close()
generate_tail_sitemap()