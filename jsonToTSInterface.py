#!/usr/bin/python

import sys
import requests
import json
import random

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
    print('--help, -h: list of available commands')
    print('--url, -u: api url from where to get the data')
    print('--file, -f: gets the data from a file')
    print('example 1: python jsonToTSInterface.py -fromFile ./file.json')
    print('example 2: python jsonToTSInterface.py -url "https://some-api"')
    print('example 3: python jsonToTSInterface.py -url "https://some-api" "output-file-name.ts"')

def main():
    if len(sys.argv) < 2:
        print('Indicate where to get the json data')
        print('or run python dataTypesFromJson.py --help')
        exit()

    command = sys.argv[1]
    data_source = sys.argv[2]

    if command == '--help' or command == '-h':
        help()

    format = 'interface Interface '
    
    if command == '--url':
        format += getJSONFromAPI(data_source)

    if command == '--file':
        format += getJSONfromFile(data_source)
    
    format += '\n'

    print('Creating interface...')

    outputFile = 'output.ts'

    if len(sys.argv) >= 4:
        outputFile = sys.argv[3]
    
    with open(outputFile, 'w') as file:
        file.write(format)
    
    print('Interface created')

try: 
    main()
except:
    print('See how to run it with --help')
    sys.exit(0)
