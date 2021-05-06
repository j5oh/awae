#!/usr/bin/python3

import requests
import argparse
import sys

parser = argparse.ArgumentParser(description='Examine some web pages')
parser.add_argument("-b", "--baseurl", dest='baseurl', action='store', help="base url to prepend to each file in filepaths")
parser.add_argument("-f", "--filepaths", dest='filepaths', action='store', help="path and filename for files to examine, one per line")
parser.add_argument("-a", "--aquatone", dest='aquatone', action='store_true', default=False, help="aquatone friendly output")
parser.add_argument("-m", "--minlength", dest='minlength', action='store', type=int, default=1000, help="minimum number of characters on response, defaults to 1000")
args = parser.parse_args()

if (args.baseurl == None or args.filepaths == None):
    print("Must supply both -b and -f")
    parser.print_usage()
    sys.exit(1)

def getUrls(base, findOutput):
    f = open(findOutput, 'r')
    lines = f.readlines()
    f.close()
    urls = []
    for line in lines:
        line = line.rstrip('\n')
        if (line.startswith('./')):
            line = line.lstrip('./')
        elif (line.startswith('/')):
            line = line.lstrip('/')
        urls.append("%s%s" % (base,line))
    return urls

def checkUrl(url, minlength, aquatone=False):
    response = requests.get(url)
    if (len(response.text) > minlength):
        output = "%s -- %s" % (url, len(response.text))
        if (aquatone):
            output = url
        print(output)
        return True
    return False

if (not args.baseurl.endswith('/')):
    args.baseurl = args.baseurl + "/"    
urls = getUrls(args.baseurl, args.filepaths)
for url in urls:
    checkUrl(url, args.minlength, args.aquatone)
