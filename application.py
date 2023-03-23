import json
from flask import Flask
from generate_site_map import generate_tail_sitemap
from flask import send_file
# EB looks for an 'application' callable by default.
application = Flask(__name__)
from flask import jsonify
from flask import request
from flask import abort
from flask_cors import CORS

import configparser
conf = configparser.ConfigParser()
conf.read('conf.ini')
from simple_salesforce import Salesforce
sf = Salesforce(username=conf['SALESFORCE']['username'], instance=conf['SALESFORCE']['instance'], password=conf['SALESFORCE']['password'], security_token=conf['SALESFORCE']['security_token'])

CORS(application)
@application.route('/aircraft/')
def get_tail_details(tail = None, key = None):
    print(f"Aircraft details on {tail}")
    tail = None
    tail = request.args.get('tail')
    key = request.args.get('key')
    if key != "74679a79-b0a7-4387-9c27-69bfe1603e9b":
        print("BAD KEY")
        abort(403) 
    if tail:
        sql = f"SELECT Aircraft_Type__c, Base_Airport__r.Name, Base_Airport__r.Airport_Name__c, Base_Airport__r.City_Image_Url__c, Image_Url_1__c, Image_Url_2__c, Image_Url_3__c, Exterior_Image__c, Interior_Image__c, wifi__c, pax__c, Safety_Rating__c FROM Aircraft_Tail__c WHERE Name = '{tail}' LIMIT 1"
        results = sf.query(sql)
        print(results)
        details = {}
        if len(results['records']) > 0:
            record = results['records'][0]
            print(record)
            if record['Aircraft_Type__c'] is not None:
                make_results = sf.query(f"SELECT Name, Category__c, Baggage_Capacity__c, Cabin_Height__c, Cabin_Length_ft__c, Cabin_Width_ft__c, Max_Passengers__c, Max_Payload__c, Max_Speed__c, Service_Ceiling__c, Typical_Seating__c, Cruise_Speed__c, Interior_Image__c, Exterior_Image__c, Range__c, Enclosed_Lav__c FROM Aircraft__c WHERE id = '{record['Aircraft_Type__c']}'")
                if len(results['records']) > 0:
                    make_record = make_results['records'][0]
                    details['make'] = {}
                    for key, val in make_record.items():
                        if key != "attributes":
                            details['make'][key] = val
            details['tail'] = tail
            details['Image_Url_1__c'] = record['Image_Url_1__c']
            details['Image_Url_2__c'] = record['Image_Url_2__c']
            details['Image_Url_3__c'] = record['Image_Url_3__c']
            details['Interior_Image__c'] = record['Interior_Image__c']
            details['Exterior_Image__c'] = record['Exterior_Image__c']
            details['wifi__c'] = record['wifi__c']
            details['Safety_Rating__c'] = record['Safety_Rating__c']
            details['pax__c'] = record['pax__c']
            if record['Base_Airport__r']:
                details['Base_Airport_City_Image'] = record['Base_Airport__r']['City_Image_Url__c']
                details['Base_Airport_Code'] = record['Base_Airport__r']['Name']
                details['Base_Airport_Name'] = record['Base_Airport__r']['Airport_Name__c']
            else:
                details['Base_Airport_Code'] = None
                details['Base_Airport_Name'] = None
            return jsonify(details)
        else:
            return jsonify(None)
@application.route('/tail_map.xml')
def return_sitemap():
    generate_tail_sitemap()
    return send_file('tail_map.xml', attachment_filename='tail_map.xml')
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
