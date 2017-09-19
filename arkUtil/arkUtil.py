
# Standard modules
import os
import sys
import re
import time
import datetime
import random
import hashlib
import commentjson
import types
from StringIO import StringIO
import traceback

# only need to do this once
random.seed(time.time())

def sort(data):
	convert_lambda = lambda text: int(text) if text.isdigit() else text
	natural_sort_lambda = lambda text: [convert_lambda(text_fragment) for text_fragment in
			 re.split("([0-9]+)", text)]
	return sorted(data, key=natural_sort_lambda)

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
			parsed = commentjson.loads(options)
			return unicodeToString(parsed)
		except Exception as err:
			if not ignoreErrors:
				raise err
	elif varType(options) == 'file':
		try:
			parsed = commentjson.load(options)
			return unicodeToString(parsed)
		except Exception as err:
			if not ignoreErrors:
				raise err
			return {}
	return {}

def splitFrameRangeByChunk(frameRange, numChunks):
	'''
	Splits single frame range dict into a list of frameRange dicts
	'''
	numFrames = frameRange['endFrame'] - frameRange['startFrame'] + 1
	framesPerThread = int(numFrames / numChunks)

	frameRangeChunks = []
	startFrame = frameRange['startFrame']

	for i in range(numChunks):
		endFrame = startFrame + framesPerThread - 1

		if i == numChunks - 1:
			endFrame = frameRange['endFrame']

		frameRangeDict = {'startFrame': startFrame, 'endFrame': endFrame}
		frameRangeChunks.append(frameRangeDict)
		startFrame = endFrame + 1

	return frameRangeChunks

def postString(args):
	'''
	Formats args object for a post request.
	'''
	data = ''
	for k,v in args.iteritems():
		data += '%s=%s&' % (k,str(v).replace('%','%25'))
	return data[:-1]

def mergeDict(source, destination):
	'''
	Merges the items of two dictionaries.
	'''
	# return dict(a.items() + b.items())
	for key, value in destination.items():
		if type(value) == dict:
			# get node or create one
			node = source.setdefault(key, {})
			mergeDict(node, value)
		# fix: better list merging
		# elif type(value) == list:
		# 	node = source.setdefault(key, [])
		# 	if type(node) == list:
		# 		source[key] = value + node
		# 	else:
		# 		source[key] = value
		else:
			source[key] = value

	return source


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
	return val

def parseCommaArray(val):
	'''
	Turns 'likes, comments' into ['like', 'comments']
	'''
	return [i.strip() for i in val.split(',')]

def parseFrameRange(frameRanges):
	'''
	Turns '1-3,5' into [1,2,3,5]
	Turns '12-11' into [11, 12]
	'''

	if not frameRanges:
		return []
	elif type(frameRanges) is float:
		return [int(frameRanges)]
	elif type(frameRanges) is int:
		return [frameRanges]

	frameRanges = frameRanges.replace(' ', '')
	frameRanges = frameRanges.split(',')
	frames = []
	for frameRange in frameRanges:
		parts = frameRange.split('-')
		if len(parts) == 2:
			start = parseInt(parts[0])
			end = parseInt(parts[1])
			if end > start:
				frames += range(start, end + 1)
			else:
				frames += range(end, start + 1)
		elif len(parts) == 1:
			frames.append(parseInt(parts[0]))

	frames = makeArrayUnique(frames)
	frames.sort()
	return frames

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
	if isinstance(val, tuple) or isinstance(val, set):
		return list(val)
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

# expand takes in a string and replaces patterns like {dd}
# with information.
# specialFunction allows a specific class to augment stringTemplate's
# functionality with class-specific replacment possibilities. See server/scripts/osOperations realPath
# method for a case of this in practice.
def expand(template, replacements={}):

	bracketedComponents = getRegexMatches(template, '{.*?\}')

	if not len(bracketedComponents):
		return template

	string = template
	for component in bracketedComponents:
		replacement = component[1:-1]
		if replacement.upper() in ['DD', 'MM', 'YY', 'YYYY']:
			replacement = getDateComponent(replacement)
		elif replacement in replacements:
			replacement = replacements[replacement]
		else:
			# otherwise keep bracketed components the same
			continue

		string = string.replace(component, replacement)

	return string

def getDateComponent(pattern):
	def datePad(dateComponent):
		return pad(dateComponent, 2)

	date = datetime.datetime.now()
	pattern = pattern.upper()

	if pattern == 'DD':
		return datePad(date.day)
	elif pattern == 'MM':
		return datePad(date.month)
	elif pattern == 'YY':
		return datePad(date.year % 100)
	elif pattern == 'YYYY':
		return str(date.year)

# formats a template to be used as a regex:
# adds capture groups around brackets
# surrounds characters around pipes with brackets, ie. [A|a] (case-insensitive options)
# escapes periods
# assumes template will start at beginning and end at end
def regexFromTemplate(template):
	if not template:
		raise ValueError('template undefined')
	regex = template
	regex = re.sub('\.', '\.', regex)
	regex = re.sub('\{[\w\d%_-]*\}', '([\w\d%_-]*)', regex)
	regex = '^' + regex + '$'
	return regex

# given a template with brackets, parses a string by extracting portions that match template
# returns as data dict
# '{a}and{b}', '1234and5' -> {a: '1234', b: '5'}
def parse(template, str):
	if not template:
		return {}

	fields = re.findall('\{([\w\d%_-]*)\}', template)
	regex = regexFromTemplate(template)

	parsed = re.match(regex, str)
	if not parsed:
		raise ValueError('could not parse string ' + str + ' with template ' + template)
	parsed = parsed.groups()
	data = dict(zip(fields, parsed))
	return data

def matchesData(template, data):
	if not template:
		raise ValueError('template undefined')
	fields = re.findall('\{([\w\d%_-]*)\}', template)
	return all([k in data.keys() for k in fields])

# needs to match to the end of the text ({asdf}/ won't match test/etc)
def matchesText(template, str):
	if not template:
		raise ValueError('template undefined')
	return bool(re.match(regexFromTemplate(template), str))


# print getPadding('%04d')
# print getPadding('.$F.')
# print getPadding('.1.')
# print getPadding('#####')
