#!/usr/bin/python3

import argparse
import sys
from bs4 import BeautifulSoup
import webbrowser as wb
if sys.version[0] == '2':
    from urllib2 import Request, urlopen
else:
    from urllib.request import Request, urlopen
    
parser = argparse.ArgumentParser(description='Arguments')
parser.add_argument('-l','--link', action='store_true', 
    help='Remove links from output')
parser.add_argument('-d','--desc', action='store_true', 
    help='Remove descriptions from output')
parser.add_argument('-t','--time', action='store_true', 
    help='Remove date and time from output')
parser.add_argument('-s','--sep', action='store_true', 
    help='Remove separator from output')
parser.add_argument('-a','--address', action='store_true', 
    help='Remove address from output')
parser.add_argument('-e','--entire', action='store_true', 
    help='Remove entire total sales number from output')
parser.add_argument('-p' , '--page', type=int, default=10,
    help='number of pages to parse')
parser.add_argument('-o' , '--output', type=str,
    help='output to filename given')
args = vars(parser.parse_args())

orig_stdout = sys.stdout
if args['output']:
    print('Searching for yard sales, please wait')
    f = open(args['output'], 'w')
    sys.stdout = f

start_url = 'http://www.yardsalesearch.com/garage-sales.html?week=0&date=0&zip=elmira+ny&r=30&q='
url = start_url
page = 1
total_sales = 0
while True:
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    desc = soup.find_all('span', {'itemprop':'description'})

    for i,sale in enumerate(desc):
        link = desc[i].find('a', href=True)['href']
        html = urlopen(link)
        d = BeautifulSoup(html, 'html.parser') #open description link
        description = d.find_all('p')[1].text
        address = d.find('div',{'class':'info'}).text.strip()
        date = d.find_all('div',{'class':'info'})[1].text.strip()
        if not args['link']:
            print(link)
        if not args['address']:
            print(address)
        if not args['time']:
            print(date)
        if not args['desc']:
            print(description.encode('ascii', 'ignore'))
        if not args['sep']:
            print('-'*50)
        total_sales += 1
    page += 1
    url = start_url + '&p={}'.format(page)
    if page == args['page']+1:
        break
if not args['entire']:
    print(total_sales)
sys.stdout = orig_stdout
print('COMPLETE')
if args['output']:
    print('Check {} file to view sales'.format(args['output']))
    wb.open('{}'.format(args['output']))

