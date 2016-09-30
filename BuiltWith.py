import requests
import argparse

# encoding=utf8
import sys


class BuiltWith():

    def __init__(self):
        
        self.key = '1fb25d4e-31b7-468c-8793-4ecebc3467be'
        self.url ='http://api.builtwith.com/v5/api.json'
        
    def module_run(self, domains):

        title = 'BuiltWith contact'
        for domain in domains:
            print("\n\nDomain "+domain +"\n")
            payload = {'key': self.key, 'lookup': domain}
            response = requests.get(self.url, params=payload)
            json=response.json()
            for result in json['Results']:
                # extract and add emails to contacts
                emails = result['Meta']['Emails']
                if emails is None: emails = []
                print('Emails\n\n')
                for email in emails:
                    print(email)
                # extract and add names to contacts
                names = result['Meta']['Names']
                if names is None: names = []
                print('Contacts\n\n')
                for name in names:
                    fname, mname, lname = self.parse_name(name['Name'])
                    print(fname+" "+mname+" "+lname)
                # extract and consolidate hosts and associated technology data
                data = {}
                for path in result['Result']['Paths']:
                    domain = path['Domain']
                    subdomain = path['SubDomain']
                    host = subdomain if domain in subdomain else '.'.join(filter(len, [subdomain, domain]))
                    if not host in data: data[host] = []
                    data[host] += path['Technologies']
                print('Technologies\n')
                for host in data:
                    # add host to hosts
                    # *** might domain integrity issues here ***
                    domain = '.'.join(host.split('.')[-2:])
                    if domain != host:
                        print('Host '+host)
                # process hosts and technology data
                for host in data:
                    # display technologies
                    for item in data[host]:
                        print("----------------------------")
                        for tag in item:
                            print('%s: %s' % (tag.encode('utf-8'), str(item[tag]).encode('utf-8')))
                            

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='BuiltWith')
    parser.add_argument('--domains', action="store", dest="domains",required=True)
    given_args = parser.parse_args()
    domain_list = given_args.domains.split(',')
    builtWith  = BuiltWith();
    builtWith.module_run(domain_list);