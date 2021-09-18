#!/usr/bin/python

import getopt
import json
import random
import requests
import sys

class Switch:
	def __init__(self, variable):
		self.variable = variable
		self.comparator = lambda x, y: x == y

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		pass

	def case(self, expr):
		if self.comparator(self.variable, expr):
			return True
		else:
			return False

	def default(self):
		return self

def getJSONFromAPI(url):
    response = requests.get(url)
    json_data = response.json() if response and response.status_code == 200 else None
    return processContent(json_data)

def getJSONfromFile(file):
    with open(file) as file:
        db = json.load(file)
        return processContent(db)

def getType(fieldContent):
    fieldType = type(fieldContent)
    with Switch(fieldType) as s:
        if s.case(list):
            return ''
        if s.case(dict):
            return ''
        if s.case(str):
            return 'string'
        if s.case(int):
            return 'number'
        if s.case(float):
            return 'number'
        if s.case(bool):
            return 'boolean'
        if s.default():  
            return 'unknown'
                

def processContent(fieldContent, noListSeparator = False):
    if type(fieldContent) == list:
        return processList(fieldContent) + '[];\n'
    
    if type(fieldContent) == dict:
        closeObject = '}' if noListSeparator else '};\n'
        return '{\n' + processDict(fieldContent) + closeObject
    
    return ''

def processDict(data):
    format = ''
    for key in data:
        if getType(data[key]) != '':
            format += str(key) + ': ' + getType(data[key]) + ';\n'
        else: 
            format += str(key) + ': '
            format += processContent(data[key])
    return format

def processList(dataList):
    if len(dataList) > 0:
        index = random.randint(0,len(dataList) - 1)
        fieldType = getType(dataList[index])
        if fieldType != '':
            return fieldType
        
        if type(dataList[index]) == dict:
            return processContent(dataList[index], True)
        if type(dataList[index]) == list:
            return processContent(dataList[index])
    return ''

def help():
    print('Available commands: ')
    print('-h, --help: List of available commands')
    print('-u, --url: API url')
    print('-f, --file: Source JSON file')
    print('-o, --output: Output file name')
    print('Usage:')
    print('python ./jsonToTSInterface.py -f ./file.json')
    print('python ./jsonToTSInterface.py --file ./file.json')
    print('python ./jsonToTSInterface.py -url "https://some-api"')
    print('python ./jsonToTSInterface.py -u "https://some-api" -o "output-file-name.ts"')
    exit()

def main():
    if sys.argv[1] in ['--help', '-h']:
        help()

    options, args = getopt.getopt(sys.argv[1:], 'u:f:o:', ['url=', 'file=', 'output='])
    
    if len(options) == 0:
        print('Indicate the json source')
        print('or run --help for help.')
        exit()

    format = 'interface Interface '

    outputFile = 'output.ts'

    for opt, arg in options:
        if opt in ['-h', '--help']:
            help()
        elif opt in ['-u', '--url']:
            format += getJSONFromAPI(arg)
        elif opt in ['-f', '--file']:
            format += getJSONfromFile(arg)
            
        if opt in ['-o', '--output']:
            outputFile = arg

    format += '\n'
    
    with open(outputFile, 'w') as file:
        print('Creating interface...')
        file.write(format)
        print('Interface created.')

try: 
    main()
except:
    print('Run --help for help.')
    sys.exit(0)
