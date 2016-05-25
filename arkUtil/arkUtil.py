
import os
import sys
import re
import time
import random
import hashlib
import json
# import math
from StringIO import StringIO
import traceback

# only need to do this once
random.seed(time.time())

REPLACEVARS = {
'#37;':'%',
'#38;':'&',
'#92;':'\\'
}


'''
	Pads a number, <num> with zeros so the resulting string is <padding> digits long.
'''
def pad(num,padding):
	num = str(num)
	return '0'*(padding-len(num)) + num

'''
	given a num, a min, and a max, ensures an output within that range.
'''
def clamp(num, mininum, maximum):
	return min(max(num, mininum), maximum)

'''
	Returns variable type of value passed in.
'''
def varType(val):
	typeString = str(type(val))
	variableType = re.search("'([a-z]+)'",typeString)
	if variableType:
		return variableType.group(1)
	return typeString

# def defaultStringReplace(str):
# 	try:
# 		for k,v in REPLACEVARS.items():
# 			str = str.replace(k,v)
# 	except:
# 		pass
# 	return str

# def defaultStringInsert(str):
# 	try:
# 		for k,v in REPLACEVARS.items():
# 			str = str.replace(v,k)
# 	except:
# 		pass
# 	return str

def defaultStringReplace(str):
	try:
		for k,v in REPLACEVARS.items():
			str = str.replace(k,v)
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
		options[args[i].replace('-','').replace(':', '')] = args[i + 1]
		i += 2
	return options

'''
	Parses given JSON if possible.  If val is a dict, return val.
	If val is a string that can't be parsed, return None.
	If val is not dictionary or string, return {}.
'''
def parseJSON(options, debug=True):
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

'''
	Formats args object for a post request.
'''
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
'''
	Merges the items of two dictionaries.
'''
def mergeDict(a,b):
	return dict(a.items() + b.items())

'''
	Rounds number DOWN to the nearest multiple of 4.
'''
def movieSafeDim(dim):
	return int(int(dim) * .25) * 4;

'''
	Removes unsafe characters from file names.
'''
def safeFilename(filename):
	"""Return a filename with only file safe characters"""
	validChars = '-_.()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	return ''.join(c for c in filename if c in validChars)

'''
	Method defaultStringInsert

	Replaces a set of common SQL variables with "safe" versions
'''
def defaultStringInsert(str):
	try:
		for k,v in REPLACEVARS.items():
			str = str.replace(v,k)
	except:
		pass
	return str

'''
	Method utcNow

	Returns current UTC time.
'''
def utcNow():
	return int(time.time() + time.timezone)

'''
	Returns random sha224 hash of given length.  Defaults to 16.
'''
def randomHash(length=16):
	return hashlib.sha224(str(random.random())).hexdigest()[:length]

'''
	Returns given array with all unique elements.
'''
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

def makeWebSafe(string):
	'''
		Takes a string and converts all non-alphanumeric characters to underscores.
		Makes all characters lowercase.
	'''
	return ''.join([i if i.isalpha() or i.isdigit() else '_' for i in string]).lower()

'''
	Turns 'likes, comments' into ['like', 'comments']
'''
def parseCommaArray(val):
	return [i.strip() for i in val.split(',')]

'''
	Appends val to obj if obj is an array.
	If obj is not, and val is not null, returns val as an array.
	If val is null, returns [].
'''
def appendOrSetArray(obj, val):
	if (isinstance(obj, list)):
		obj.append(val)
		return obj
	if (isinstance(val, list)):
		return val
	if (val != None):
		return [val]
	return []

'''
	Returns val as an array.
	If val is null, returns [].
'''
def ensureArray(val):
	if (isinstance(val, list)):
		return val
	if (val == None):
		return []
	return [val]

'''
	Returns float version of val if val is number or a string representing a number.
	Otherwise returns 0.
'''
def ensureNumber(val):
	try:
		return float(val)
	except:
		return 0

'''
	Given a dictionary, returns a dictionary with all entries with keys in keysToOmit omitted.
'''
def omitObjectKeys(d, keysToOmit):
	keysToOmit = ensureArray(keysToOmit)
	dictToReturn = {}
	for k, v in d.iteritems():
		if k not in keysToOmit:
			dictToReturn[k] = v
	return dictToReturn

'''
	Given a dictionary, returns a dictionary with all entries with keys in keysToKeep.
'''
def collectObjectKeys(d, keysToKeep):
	keysToKeep = ensureArray(keysToKeep)
	dictToReturn = {}
	for k, v in d.iteritems():
		if k in keysToKeep:
			dictToReturn[k] = v
	return dictToReturn

'''
	Behaves like javascripts parseInt.  Returns 0 if not a number.
'''
def parseInt(val):
  m = re.search(r'^(\d+)[.,]?\d*?', str(val))
  intToReturn = int(m.groups()[-1]) if m and not callable(val) else None
  if (intToReturn):
  	return intToReturn
  return 0

'''
	Capitalizes first character in the given string.
'''
def capitalize(string):
	if (string):
		return string[0].upper() + string[1:]
	else:
		return ''

'''
	Capitalizes the first character in each word.
'''
def capitalizeWords(string):
	return ' '.join([capitalize(w) for w in string.split(' ')])

'''
	returns a capitalized version of the words
'''
def formalName(name):
	formalName = name
	firstChar = name[0]
	if (firstChar == '_'):
		formalName = formalName[1:]

	formalName = capitalizeWords(formalName)

	if (firstChar == '_'):
		formalName = firstChar + formalName

	return formalName

'''
	Accepts sorts in form 'field:ASC', 'field:-1', or 'field','desc'
	Returns sort object.
'''
def parseSort(field, order):
	parts = field.split(':')
	if len(parts) > 1:
		order = parts[1]
	else:
		order = order
	order = str(order).lower().strip()[0]
	if (order == 'd' or order == '-'):
		order = 'DSC'
	else:
		order = 'ASC'
	return {'field': parts[0], 'order': order, 'combined': parts[0] + ':' + order}

'''
	Returns -1 if b > a, 1 if a > b, and 0 if a == b.
'''
def stringCompare(a, b):
	a = a.lower()
	b = b.lower()
	if (b > a):
		return -1
	elif (a > b):
		return 1
	return 0

'''
	Removes all non-alphanumeric values from a string.
'''
def getAlphaNumericOnly(val):
	return ''.join([i for i in val if i.isalpha() or i.isdigit()])

'''
	Method:removeTrailingSlash

	Ensures a trailing slash is omitted
'''
def removeTrailingSlash(url):
	if url[-1] == '/':
		return url[:-1]
	return url

'''
	A wrapper around Python's random - ensures parity with helpers.js
'''
def getRandomInteger(minimum, maximum):
	return random.randint(minimum, maximum)

'''
	Execute python code
'''
def executePython(code, context={}):
	# fix syntax error if last line is a comment with no new line
	if not code.endswith('\n'):
		code = code + '\n'

	# compile
	try:
		scriptType = 'exec'
		if code.count('\n') == 1:
			scriptType = 'single'
		compiled = compile(code, '<string>', scriptType)
	except Exception:
		return traceback.format_exc()

	oldStdOut = sys.stdout

	# override stdout to capture exec results
	outBuffer = StringIO()
	sys.stdout = outBuffer

	try:
		context.update(globals())
		exec(compiled, context)
	except Exception:
		# remove refernces to this command and the calling scripteditor host
		# script from the traceback output
		formatted_lines = traceback.format_exc().splitlines()
		formatted_lines.pop(2)
		formatted_lines.pop(1)
		result = '\n'.join(formatted_lines)
	else:
		result = outBuffer.getvalue()

	sys.stdout = oldStdOut
	return result

'''
	Execute a python file
'''
def executePythonFile(scriptPath, context={}):
	try:
		with open(scriptPath) as f:
			code = f.read()
	except Exception:
		return traceback.format_exc()

	# set expected python magic variables
	context['__file__'] = scriptPath
	context['__name__'] = '__main__'
	sys.argv = [scriptPath]

	# append the dirname to path so we can require files like normal
	sys.path.append(os.path.dirname(scriptPath))
	return executePython(code, context)
