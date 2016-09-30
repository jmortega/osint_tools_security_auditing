import requests
import re
import argparse

def get_emails(domain):
    
    if not domain.startswith("http://") == True:
        domain="http://"+domain
    
    response = requests.get(domain)
    text = response.text
    patron = re.compile("[-a-zA-Z0-9._]+@[-a-zA-Z0-9_]+.[a-zA-Z0-9_.]+")
    mails = re.findall(patron,text)
    emails = str(mails)

    print(emails)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='gets emails from domain.', prog='get_emails_from_url.py', epilog="", add_help=False)
    # Adding the main options
    general = parser.add_mutually_exclusive_group(required=True)
    general.add_argument('-d', '--domain', metavar='<domain>', action='store', help='domain to be resolved.')
    args = parser.parse_args()
    
    get_emails(args.domain)