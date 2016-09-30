import sys 
import json
import requests
import argparse

API_URL = "https://www.censys.io/api/v1"
UID = "6f5c0df4-3908-430f-9f17-fb350db03fa3"
SECRET = "9s7nwqeXjJxzBkij4gxFNYC5EQYhX6QG"

def get_censys_data(ip,domain):
    
    if ip is not None:
        res = requests.get(API_URL + "/view/ipv4/"+ip, auth=(UID,SECRET))
        params ={"query": ip, "page":1} 
        res2 = requests.post(API_URL + "/search/certificates",auth=(UID, SECRET), json=params)

    if domain is not None:    
        res = requests.get(API_URL + "/view/websites/"+domain, auth=(UID,SECRET))

    if res.status_code != 200: 
        print("error occurred: %s" % res.json()["error"])
        sys.exit(1)

    print(json.dumps(res.json(), indent=4))

    with open('data_censys.txt', 'w') as file:
        json.dump(res.json(), file, ensure_ascii=False,indent=4)
        
    if res2 is not None and res2.status_code == 200: 
        with open('data_censys_certificates.txt', 'w') as file:
            json.dump(res2.json(), file, ensure_ascii=False,indent=4)        
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Uses censys for search ipv4/domain.', prog='censys_data.py', epilog="", add_help=False)
    # Adding the main options
    general = parser.add_mutually_exclusive_group(required=True)
    general.add_argument('-d', '--domain', metavar='<domain>', action='store', help='query to be resolved.')
    general.add_argument('-ipv4', '--ipv4', metavar='<ipv4>', action='store', help='query to be resolved.')       
    args = parser.parse_args()       
        
        
    get_censys_data(args.ipv4,args.domain)