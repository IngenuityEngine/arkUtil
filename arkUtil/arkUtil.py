
# Standard modules
import os
import sys
import re
import time
import random
import hashlib
import commentjson
import types
from StringIO import StringIO
import traceback

# only need to do this once
random.seed(time.time())

REPLACEVARS = {
'#37;':'%',
'#38;':'&',
'#92;':'\\'
}


def pad(num, padding, padChar='0'):
	'''
	Pads a number, <num> with zeros so the resulting string is <padding> digits long.
	'''
	num = str(num)
	if len(num) >= padding:
		return num
	return padChar * (padding - len(num)) + num

def clamp(num, mininum, maximum):
	'''
	given a num, a min, and a max, ensures an output within that range.
	'''
	return min(max(num, mininum), maximum)

def varType(val):
	'''
	Returns variable type of value passed in.
	'''
	typeString = str(type(val))
	matches = re.findall("'([a-zA-Z_]+)'", typeString)
	if len(matches):
		return matches[0]
	return typeString

def parseJSON(options, ignoreErrors=False):
	'''
	Parses given JSON if possible.  If val is a dict, return val.
	If val is a string that can't be parsed, return None.
	If val is not dictionary or string, return {}.
	'''
	if not options:
		return {}
	if varType(options) == 'dict':
		return options
	elif varType(options) == 'str':
		try:
			parsed = commentjson.load(options)
			return unicodeToString(parsed)
		except:
			if not ignoreErrors:
				raise Exception('Failed to load options: ' + options)
			return {}
	return {}

def postString(args):
	'''
	Formats args object for a post request.
	'''
	data = ''
	for k,v in args.iteritems():
		data += '%s=%s&' % (k,str(v).replace('%','%25'))
	return data[:-1]

def mergeDict(a,b):
	'''
	Merges the items of two dictionaries.
	'''
	return dict(a.items() + b.items())

def movieSafeDim(dim):
	'''
	Rounds number DOWN to the nearest multiple of 4.
	'''
	return int(int(dim) * .25) * 4;

def safeFilename(filename):
	'''
	Removes unsafe characters from file names.
	'''
	validChars = '-_.()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	return ''.join(c for c in filename if c in validChars)


def utcNow():
	'''
	Returns current UTC time.
	'''
	return int(time.time() + time.timezone)

def randomHash(length=16):
	'''
	Returns random sha224 hash of given length.  Defaults to 16.
	'''
	return hashlib.sha224(str(random.random())).hexdigest()[:length]

def makeArrayUnique(val, transformFunc=None):
	'''
	Returns given array with all unique elements.
	'''
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

def makeWebSafe(val):
	'''
	Takes a string and converts all non-alphanumeric characters
	to underscores.	Makes all characters lowercase.
	'''
	val = str(val)
	# Everything not a letter or number becomes an underscore
	val = re.sub('[^A-Za-z0-9]', '_', val)
	# Consecutive underscores become one dash
	val = re.sub('\_+', '_', val)
	# Leading underscores go away
	val = re.sub('^\_', '', val)
	# Trailing underscores go away
	val = re.sub('\_$', '', val)
	return val.lower()
	# return ''.join([i if i.isalpha() or i.isdigit() else '_' for i in string]).lower()

def parseCommaArray(val):
	'''
	Turns 'likes, comments' into ['like', 'comments']
	'''
	return [i.strip() for i in val.split(',')]

def appendOrSetArray(obj, val):
	'''
	Appends val to obj if obj is an array.
	If obj is not, and val is not null, returns val as an array.
	If val is null, returns [].
	'''
	if isinstance(obj, list):
		obj.append(val)
		return obj
	if isinstance(val, list):
		return val
	if val != None:
		return [val]
	return []

def ensureArray(val):
	'''
	Returns val as an array.
	If val is null, returns [].
	'''
	if (isinstance(val, list)):
		return val
	if (val == None):
		return []
	return [val]

# fix: should check for NaN, etc
def ensureNumber(val):
	'''
	Returns float version of val if val is number or a string representing a number.
	Otherwise returns 0.
	'''
	try:
		return float(val)
	except:
		return 0

def omitObjectKeys(d, keysToOmit):
	'''
	Given a dictionary, returns a dictionary with all entries with keys in keysToOmit omitted.
	'''
	keysToOmit = ensureArray(keysToOmit)
	newDict = {}
	for k, v in d.iteritems():
		if k not in keysToOmit:
			newDict[k] = v
	return newDict

def collectObjectKeys(d, keysToKeep):
	'''
	Given a dictionary, returns a dictionary with all entries with keys in keysToKeep.
	'''
	keysToKeep = ensureArray(keysToKeep)
	newDict = {}
	for k, v in d.iteritems():
		if k in keysToKeep:
			newDict[k] = v
	return newDict

def parseInt(val):
	'''
	Behaves like javascripts parseInt.
	Returns 0 if not a number.
	'''
	match = re.search(r'^(\d+)[.,]?\d*?', str(val))
	if match:
		return int(match.groups()[-1])
	return 0

def capitalize(string):
	'''
	Capitalizes first character in the given string.
	'''
	if string:
		return string[0].upper() + string[1:]
	else:
		return ''

# fix: implementation should match javascript
def capitalizeWords(string):
	'''
	Capitalizes the first character in each word.
	'''
	return ' '.join([capitalize(w) for w in string.split(' ')])

def formalName(name):
	'''
	returns a capitalized version of the words
	'''
	formalName = name
	firstChar = name[0]
	if (firstChar == '_'):
		formalName = formalName[1:]

	formalName = capitalizeWords(formalName)

	if (firstChar == '_'):
		formalName = firstChar + formalName

	return formalName

def parseSort(field, order):
	'''
	Accepts sorts in form 'field:ASC', 'field:-1', or 'field','desc'
	Returns sort object.
	'''
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
	return {
		'field': parts[0],
		'order': order,
		'combined': parts[0] + ':' + order
	}

def stringCompare(a, b):
	'''
	Returns -1 if b > a, 1 if a > b, and 0 if a == b.
	'''
	a = a.lower()
	b = b.lower()
	if (b > a):
		return -1
	elif (a > b):
		return 1
	return 0

def getAlphaNumericOnly(val):
	'''
	Removes all non-alphanumeric values from a string.
	'''
	return ''.join([i for i in val if i.isalpha() or i.isdigit()])

def removeTrailingSlash(url):
	'''
	Ensures a trailing slash is omitted
	'''
	if url[-1] == '/':
		return url[:-1]
	return url

# purposefully omit random as python has a random library


def getRandomInteger(minimum, maximum=None):
	'''
	A wrapper around Python's random - ensures parity with helpers.js
	'''
	# if we skip max, just go from 0 to min
	if maximum is None:
		maximum = minimum
		minimum = 0
	return random.randint(minimum, maximum)

def getRandomFloat(minimum, maximum=None):
	'''
	A wrapper around Python's random - ensures parity with helpers.js
	'''
	# if we skip max, just go from 0 to min
	if maximum is None:
		maximum = minimum
		minimum = 0
	return random.uniform(minimum, maximum)

def getRandomIndex(var):
	'''
	Returns a random index number for a given array
	'''
	return getRandomInteger(len(var))

def getRandomIndexValue(var):
	'''
	Returns a random index value for a given array
	'''
	return var[getRandomIndex(var)]


def executePython(code, context={}):
	'''
	Execute python code
	'''
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

def executePythonFile(scriptPath, context={}):
	'''
	Execute a python file
	'''
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


def getRegexMatches(string, regex):
	return re.findall(regex, string)

def replaceAll(string, find, replace):
	return re.sub(find, replace, string)

def defaultFor(var, defaultValue):
	if var is None:
		return defaultValue
	return var

# fix: missing moveArrayItem
# def moveArrayItem(arr, from, to):

def isError(var):
	return isinstance(var, Exception)

def isSubset(test, allItems):
	subset = True
	for item in test:
		subset = subset and item in allItems
	return subset

def joinUrl(*args):
	combined = ''
	for url in args:
		if len(combined) and combined[-1] != '/':
			combined += '/'
		if url[0] == '/':
			url = url[1:]
		combined += url
	return combined

def unicodeToString(data):
	'''
	Replaces unicode with a regular string
	for a variety of data types
	'''
	inputType = type(data)
	if isinstance(data, types.StringTypes):
		return str(data)
	elif inputType == types.ListType:
		return [unicodeToString(x) for x in data]
	elif inputType == types.DictType:
		# fix: uncomment in Sublime 3
		# return {unicodeToString(x): unicodeToString(data[x]) for x in data}
		return dict([(unicodeToString(x), unicodeToString(data[x])) for x in data])
	else:
		return data
