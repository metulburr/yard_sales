#!/usr/bin/python3

import argparse
import sys
from bs4 import BeautifulSoup
import webbrowser as wb
import difflib
if sys.version[0] == '2':
    from urllib2 import Request, urlopen
    import Tkinter
else:
    from urllib.request import Request, urlopen
    import tkinter
    
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
parser.add_argument('-p' , '--page', type=int, default=5,
    help='number of pages to parse')
parser.add_argument('-o' , '--output', type=str,
    help='output to filename given')
parser.add_argument('-x' , '--exclude', type=str, nargs='*',
    help='remove entries from list if found in address line')
parser.add_argument('-i' , '--include', type=str, nargs='*',
    help='include only entries from list if found in address line')
parser.add_argument('-f' , '--diff', type=str,
    help='Check current difference from file. This file is a previous output from -o')
args = vars(parser.parse_args())

print('Searching for yard sales, please wait')

start_url = 'http://www.yardsalesearch.com/garage-sales.html?week=0&date=0&zip=elmira+ny&r=30&q='
url = start_url
page = 1
total_sales = 0
output_str = ''
ex = args['exclude']
inc = args['include']

while True:
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    desc = soup.find_all('span', {'itemprop':'description'})

    for i,sale in enumerate(desc):
        ex_flag = False
        in_flag = False
        link = desc[i].find('a', href=True)['href']
        html = urlopen(link)
        d = BeautifulSoup(html, 'html.parser') #open description link
        description = d.find_all('p')[1].text
        address = d.find('div',{'class':'info'}).text.strip()
        date = d.find_all('div',{'class':'info'})[1].text.strip()
        if not args['address']:
            if ex:
                for e in ex:
                    if e in address:
                        ex_flag = True
            elif inc:
                ex_flag = True
                for i in inc:
                    if i in address:
                        in_flag = True
            if not ex_flag or in_flag:
                output_str += address + '\n'
        if not args['link']:
            if not ex_flag or in_flag:
                output_str += link + '\n'
        if not args['time']:
            if not ex_flag or in_flag:
                output_str += date + '\n'
        if not args['desc']:
            if not ex_flag or in_flag:
                output_str += description + '\n'
        if not args['sep']:
            if not ex_flag or in_flag:
                output_str += '-'*50 + '\n'
        if not ex_flag or in_flag:
            total_sales += 1
    page += 1
    url = start_url + '&p={}'.format(page)
    if page == args['page']+1:
        break
if not args['entire']:
    output_str += str(total_sales) + '\n'
    
    
    
if args['diff']:
    old = open(args['diff'])
    new = output_str
    for char in difflib.unified_diff(old.readlines(), new.splitlines(True), fromfile=old.name, tofile='current', lineterm='\n'):
        print(char)
    old.close()

if args['output']:
    f = open(args['output'], 'w')
    f.write(output_str.encode('ascii', 'ignore'))
    f.close()
    
    print('Check {} file to view sales'.format(args['output']))
    wb.open('{}'.format(args['output']))
else:
    if not args['diff']:
        print(output_str)

