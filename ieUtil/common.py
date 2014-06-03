import sys
import re
import time
import random
import hashlib
import json
from itertools import izip

# only need to do this once
random.seed(time.time())

REPLACEVARS = {
'#37;':'%',
'#38;':'&',
'#92;':'\\'
}

def pad(num,padding):
	num = str(num)
	return '0'*(padding-len(num)) + num

# currently only used in shepherd/JobTypes
def checkNumParam(param,default):
	if param == '':
		return default
	try:
		param = defaultStringReplace(str(int(param)))
	except:
		param = str(default)
	return param

def listToDict(val):
	i = iter(val)
	return dict(izip(i, i))

def varType(val):
	typeString = str(type(val))
	variableType = re.search("'([a-z]+)'",typeString)
	if variableType:
		return variableType.group(1)
	return typeString

def defaultStringReplace(str):
	try:
		for k,v in REPLACEVARS.items():
			str = str.replace(k,v)
	except:
		pass
	return str

def defaultStringInsert(str):
	try:
		for k,v in REPLACEVARS.items():
			str = str.replace(v,k)
	except:
		pass
	return str

# fix: breaks on single dash arguments, improve
def getArgs(args=None):
	i = 1
	if not args:
		args = sys.argv
	options = {'__file__':args[0]}
	while (i < sys.argv.__len__() - 1):
		options[args[i].replace('-','')] = args[i + 1]
		i += 2
	return options

def getJSONOptions(options, debug=True):
	if not options:
		return {}
	if varType(options) == 'dict':
		return options
	elif varType(options) == 'string':
		try:
			return json.loads(options)
		except:
			if debug: raise Exception('Failed to load options: ' + options)
			return {}
	return {}

def uriReplace(v):
  return v.replace('%','%25')

def postString(args):
  data = ''
  for k,v in args.iteritems():
	data += '%s=%s&' % (k,uriReplace(str(v)))
  return data[:-1]

# fix: shouldn't be using dictToAndFrom
def dictToAndFrom(val):
	if varType(val) == 'dict':
		invDict = {}
		for k,v in val.iteritems():
			invDict[v] = k
		return dict(val.items() + invDict.items())

def mergeDict(a,b):
	return dict(a.items() + b.items())

def movieSafeDim(dim):
	return int(int(dim) * .25) * 4;

def safeFilename(filename):
	"""Return a filename with only file safe characters"""
	validChars = '-_.()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	return ''.join(c for c in filename if c in validChars)

def utcNow():
	return int(time.time() + time.timezone)

def randomHash(length=16):
	return hashlib.sha224(str(random.random())).hexdigest()[:length]

def makeArrayUnique(val, transformFunc=None):
	def makeUnique(val, transformFunc):
		seen = set()
		if transformFunc is None:
			for x in val:
				if x in seen:
					continue
				seen.add(x)
				yield x
		else:
			for x in val:
				x = transformFunc(x)
				if x in seen:
					continue
				seen.add(x)
				yield x
	return list(makeUnique(val, transformFunc))

