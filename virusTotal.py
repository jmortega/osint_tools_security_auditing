import json
import requests
import argparse

def get_data_virus_total(ip,domain):
    
    url_ip_address = 'https://www.virustotal.com/vtapi/v2/ip-address/report'
    url_domain = 'https://www.virustotal.com/vtapi/v2/domain/report'

    #parameters = {'ip': ip, 'apikey': '-- YOUR API KEY --'}
    parameters_ip = {'ip': ip, 'apikey': '1c2fb58f31b82e29a93c6a87392b21bc3b64247b8af0a42788a7dd03d6728c57'}
    parameters_domain = {'domain': domain, 'apikey': '1c2fb58f31b82e29a93c6a87392b21bc3b64247b8af0a42788a7dd03d6728c57'}
 
    if ip is not None:
        
        response = requests.get(url_ip_address,params=parameters_ip)
        response_dict = json.loads(response.text)
        print(json.dumps(response_dict, sort_keys=True,indent=4))
        
        with open('data_virus_total.txt', 'w') as file:
                json.dump(response_dict, file, ensure_ascii=False,indent=4)        


    if domain is not None:
        response = requests.get(url_domain,params=parameters_domain)
        response_dict = json.loads(response.text)
        print(json.dumps(response_dict, sort_keys=True,indent=4))
        
        with open('data_virus_total.txt', 'w') as file:
                        json.dump(response_dict, file, ensure_ascii=False,indent=4)           

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Makes a search onto virustotal.com.', prog='virusTotal.py', epilog="", add_help=False)
    # Adding the main options
    general = parser.add_mutually_exclusive_group(required=True)
    general.add_argument('-d', '--domain', metavar='<domain>', action='store', help='query to be resolved by virustotal.com.')
    general.add_argument('-ip', '--ipv4', metavar='<ipv4>', action='store', help='query to be resolved by virustotal.com.')   
    args = parser.parse_args()        
    
    get_data_virus_total(args.ipv4,args.domain)