import shodan
import argparse
import socket


def get_shodan_data(target,search):
        
        SHODAN_API_KEY = "v4YpsPUJ3wjDxEqywwu6aF5OZKWj8kik"

        api = shodan.Shodan(SHODAN_API_KEY)
        
        if search is not None:
                # Wrap the request in a try/ except block to catch errors
                try:
                        # Search Shodan
                        results = api.search(search)

                        # Show the results
                        print('Results sodan search: %s' % results['total'])
                        for result in results['matches']:
                                print('IP: %s' % result['ip_str'])
                                print(result['data'])

                except shodan.APIError as e:
                        print('Error: %s' % e)
        

        if search is not None:
                # Wrap the request in a try/ except block to catch errors
                try:
                        # Search Shodan
                        results = api.count(search)
        
                        # Show the results
                        print('Results sodan search: %s' % results['total'])
                        for result in results['matches']:
                                print('IP: %s' % result['ip_str'])
                                print(result['data'])
                
                except shodan.APIError as e:
                        print('Error: %s' % e)

        
        if target is not None:
                
                hostname = socket.gethostbyname(target)
                
                # Lookup the host
                host = api.host(hostname)
        
                # Print general info
                print("""
                IP: %s
                Organization: %s
                Operating System: %s
                """ % (host['ip_str'], host.get('org', 'n/a'), host.get('os', 'n/a')))
        
                # Print all banners
                for item in host['data']:
                        print("""Port: %s
                        Banner: %s""" % (item['port'], item['data']))
        
        
if __name__ == "__main__":
        parser = argparse.ArgumentParser(description='Shodan search', prog='demoShodanSearch.py', epilog="", add_help=False)
        # Adding the main options
        general = parser.add_mutually_exclusive_group(required=True)
        # Main arguments
        general.add_argument("-target", dest="target", help="target IP / domain", required=None)
        general.add_argument("-search", dest="search", help="search", required=None)
        
        args = parser.parse_args()
            
        get_shodan_data(args.target,args.search)        