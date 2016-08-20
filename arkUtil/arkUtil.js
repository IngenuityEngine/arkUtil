
// Vendor Modules
/////////////////////////
var _ = require('lodash')
var _s = require('underscore.string')
var debug = require('debug')
debug = debug('helpers')

// Our Modules
/////////////////////////
// var constants = require('../constants')


// Constants
/////////////////////////
var seed = 156
var notAlphaNumeric = new RegExp(/[^a-z0-9_]/ig)
var validIP = new RegExp(/^(([1-9]?\d|1\d\d|2[0-5][0-5]|2[0-4]\d)\.){3}([1-9]?\d|1\d\d|2[0-5][0-5]|2[0-4]\d)$/)
var localIP = new RegExp(/(^127\.)|(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^192\.168\.)/)

// Main
/////////////////////////
var helpers = module.exports = {

// Variables
/////////////////////////
isClient: typeof window != 'undefined' &&
	window.document !== undefined,
isServer: typeof process != 'undefined' &&
	process.pid !== undefined,

// Methods
/////////////////////////

pad: function(num, padding, padChar)
{
	padChar = padChar || '0'
	num = num + ''
	if (num.length >= padding)
		return num
	return new Array(padding - num.length + 1).join(padChar) + num
},

clamp: function(num, min, max)
{
  return Math.min(Math.max(num, min), max)
},

/*
Method: varType

Returns variable type of value passed in.
*/
varType: function(val)
{
	return ({})
		.toString
		.call(val)
		.match(/\s([a-zA-Z]+)/)[1]
		.toLowerCase()
},


/*
Method: parseJSON

Parses given JSON if possible.  If val is a dict, return val.
If val is a string that can't be parsed, return None.
If val is not dictionary or string, return val.
*/
parseJSON: function(val)
{
	if (_.isObject(val))
	{
		return val
	}
	else if (_.isString(val))
	{
		try {
			return JSON.parse(val)
		} catch (e) {
			return null
		}
	}
	return val
},


/*
	Method: postString

	Formats args object for a post request.
*/
postString: function(args)
{
	var data = ''
	for (var propt in args)
	{
		if (args.hasOwnProperty(propt))
		{
			data = data + String(propt) + '=' + String(args[propt]) + '&'
		}
	}
	return data.slice(0, -1)
},

/*
	Method: mergeObject

	Merges the items of two objects.
*/
mergeObject: function(a, b)
{
	return _.extend(a,b)
},

/*
	Method: movieSafeDim

	Rounds number DOWN to the nearest multiple of 4.
*/
movieSafeDim: function(dim)
{
	return  parseInt(parseInt(dim, 10) * 0.25, 10) * 4
},

/*
	Method: safeFilename

	Removes unsafe characters from file names.
*/
safeFilename: function(filename)
{
	var newName = ''
	var validChars = '-_.()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	for (var i = 0; i < filename.length; i += 1)
	{
		if (validChars.indexOf(filename[i]) > -1)
			newName = newName + filename[i]
	}
	return newName
},

/*
	Method: utcNow

	Return current UTC time.
*/
utcNow: function()
{
	var d = new Date()
	return d.getTime() + d.getTimezoneOffset()
},

randomHash: function(length)
{
	return Math.random().toString(36).substring(length)
},


// fix: missing randomHash


/*
	Method: makeArrayUnique

	Returns given array with all unique elements.
*/
makeArrayUnique: function(val)
{
	// indexOf returns the first occurance of a value
	// so if indexOf value isn't equal to index
	// then the value isn't unique so trash it
	return val.filter(function(value, index, self)
		{
			return self.indexOf(value) === index
		})
},

makeWebSafe: function(val)
{
	val = String(val)
	// Everything not a letter or number becomes an underscore
	val = val.replace(/[^A-Za-z0-9]/g, '_')
	// Consecutive underscores become one dash
	val = val.replace(/\_+/g, '_')
	// Leading underscores go away
	val = val.replace(/^\_/, '')
	// Trailing underscores go away
	val = val.replace(/\_$/, '')
	return val.toLowerCase()
},

/*
	Method: parseCommaArray

	Turns 'like, comments' into ['like', 'comments']
*/
parseCommaArray: function(val)
{
	// if (!_.isString(val))
	// 	throw new Error('helpers.parseCommaArray -> val must be a string, got:' + val)
	var keys = val.split(',')
	// trim each key
	return _.map(keys, function(s)
		{
			return s.trim()
		})
},
/*
	Method: parseFrameRange

	Turns '1-3,5' into [1,2,3,5]
	Turns '12-11' into [11, 12]
*/
parseFrameRange: function(frameRanges)
{
	if (!frameRanges)
		return []
	else if (_.isNumber(frameRanges))
		return [helpers.parseInt(frameRanges)]

	frameRanges = frameRanges.split(',')
	var frames = []
	var parts, start, end
	_.each(frameRanges, function(frameRange)
	{
		parts = frameRange.split('-')
		if (parts.length == 2)
		{
			start = helpers.parseInt(parts[0])
			end = helpers.parseInt(parts[1])
			if (end > start)
				frames = frames.concat(_.range(start, end + 1))
			else
				frames = frames.concat(_.range(end, start + 1))
		}
		else if (parts.length == 1)
		{
			frames.push(helpers.parseInt(parts[0]))
		}
	})

	return _.sortBy(helpers.makeArrayUnique(frames))
},
/*
	Method: appendOrSetArray

	Appends val to obj if obj is an array.
	If obj is not, and val is not null, returns val as an array.
	If val is null, returns [].
*/
appendOrSetArray: function(obj, val)
{
	if (_.isArray(obj))
		return obj.concat(val)
	else if (_.isArray(val))
		return val
	else if (!_.isUndefined(val) && !_.isNull(val))
		return [val]
	else
		return []
},
/*
	Method: ensureArray

	Returns val as an array.
	If val is null, returns [].
*/
ensureArray: function(val)
{
	if (_.isArray(val))
		return val
	if (_.isUndefined(val))
		return []
	return [val]
},
/*
	Method: ensureNumber

	Returns int version of val if val is int or a string representing a int.
	Otherwise returns 0.
*/
ensureNumber: function(val)
{
	val = parseFloat(val)
	if (isNaN(val))
		return 0
	return val
},
/*
	Method: omitObjectKeys

	Given a dictionary, returns a dictionary with all entries with keys in keysToOmit omitted.
*/
omitObjectKeys: function(object, keysToOmit)
{
	keysToOmit = helpers.ensureArray(keysToOmit)
	// the keys need to be strings or lodash isn't in to it
	keysToOmit = _.map(keysToOmit, function(key)
	{
		return String(key)
	})
	return _.pickBy(object, function(val, key)
		{
			return !_.includes(keysToOmit, String(key))
		})
},
/*
	Method: collectObjectKeys

	Given a dictionary, returns a dictionary with all entries with keys in keysToKeep.
*/
collectObjectKeys: function(object, keysToKeep)
{
	keysToKeep = helpers.ensureArray(keysToKeep)
	// the keys need to be strings or lodash isn't in to it
	keysToKeep = _.map(keysToKeep, function(key)
	{
		return String(key)
	})
	return _.pickBy(object, function(val, key)
		{
			return _.includes(keysToKeep, key)
		})
},

/*
	Method: parseInt

	Behaves like javascripts parseInt.
	Returns 0 if not a number.
*/
parseInt: function(val)
{
	return parseInt(val, 10) || 0
},


/*
	Method: capitalize

	Capitalizes first character in the given string.
*/
capitalize: function(str)
{
	if (str)
	return str.charAt(0).toUpperCase() + str.slice(1)
},
/*
	Method: capitalizeWords

	Capitalizes the first character in each word.
*/
capitalizeWords: function(str)
{
	// http://kevin.vanzonneveld.net
	// +   original by: Jonas Raoni Soares Silva (http://www.jsfromhell.com)
	// +   improved by: Waldo Malqui Silva
	// +   bugfixed by: Onno Marsman
	// +   improved by: Robin
	// +      input by: James (http://www.james-bell.co.uk/)
	// +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
	// *     example 1: capitalizeWords('kevin van  zonneveld');
	// *     returns 1: 'Kevin Van  Zonneveld'
	// *     example 2: capitalizeWords('HELLO WORLD');
	// *     returns 2: 'HELLO WORLD'
	return (str + '')
		.replace(/^([a-z\u00E0-\u00FC])|\s+([a-z\u00E0-\u00FC])/g,
			function (word)
			{
				return word.toUpperCase()
			})
},
formalName: function(name)
{
	var formalName = name
	var firstChar = name[0]
	// slice off the 1st character
	if (firstChar == '_')
		formalName = formalName.slice(1)

	formalName = _s.humanize(formalName)
	formalName = helpers.capitalizeWords(formalName)

	// add it back on
	if (firstChar == '_')
		formalName = firstChar + formalName
	return formalName
},

/*
	Method: parseSort

	Accepts sorts in form 'field:ASC', 'field:-1',
	or 'field','desc'
	Returns sort object.
*/
parseSort: function(field, order)
{
	var parts = field.split(':')

	order = parts[1] || order
	order = String(order)[0].toLowerCase().trim()[0]
	// default to ASC
	if (order == 'd' || order == '-')
		order = 'DSC'
	else
		order = 'ASC'

	return {
		field: parts[0],
		order: order,
		combined: parts[0] + ':' + order
	}
},

/*
	Method: stringCompare

	Returns -1 if b > a, 1 if a > b, and 0 if a == b.
*/
stringCompare: function(valA, valB, localeCompare)
{
	if (localeCompare)
		return valA.toLowerCase().localeCompare(valB.toLowerCase())

	valA = valA.toLowerCase()
	valB = valB.toLowerCase()
	return valA < valB ? -1: (valA > valB ? 1: 0)
},

/*
	Method: getAlphaNumericOnly

	Removes all non-alphanumeric characters from a string.
*/
getAlphaNumericOnly: function(val)
{
	return val.replace(notAlphaNumeric, '')
},

removeTrailingSlash: function(url)
{
	// remove trailing slashes
	if (url[url.length-1] == '/')
		return url.slice(0,-1)
	return url
},

// Method: random
// Returns a random float between 0 and 1.
// Slight bias towards 0 and 1.
random: function()
{
	seed += 1
	var x = Math.sin(seed) * 10000;
	return x - Math.floor(x);
},
// Method: getRandomInteger
// Returns a random integer between min and max inclusive.
getRandomInteger: function(min, max)
{
	// if we skip max, just go from 0 to min
	if (max === undefined)
	{
		max = min
		min = 0
	}
	return Math.floor(helpers.random() * (max - min + 1)) + min
},

// Method: getRandomFloat
// Returns a random float between min and max exclusive.
getRandomFloat: function(min, max)
{
	// if we skip max, just go from 0 to min
	if (max === undefined)
	{
		max = min
		min = 0
	}
	return helpers.random() * (max - min) + min
},

// Method: getRandomIndex
// Returns a random index number for a given array
getRandomIndex: function(arr)
{
	return helpers.getRandomInteger(arr.length)
},

// Method: getRandomIndexValue
// Returns a random index value for a given array
getRandomIndexValue: function(arr)
{
	return arr[helpers.getRandomIndex(arr)]
},

// purposefully skip executePython

// purposefully skip executePythonFile

// collect all the matches in a string for a given
// regex object note: /g flag must be set
// on RegExp(regex, 'g') or /regex/g
getRegexMatches: function(str, regex)
{
	var matches = []
	var match
	do {
		match = regex.exec(str)
		if (match !== null)
			matches.push(match)
	}
	while (match !== null)
	return matches
},
replaceAll: function(str, find, replace)
{
	return str.replace(new RegExp(find, 'g'), replace)
},
defaultFor: function(variable, defaultValue)
{
	if (variable === undefined)
		return defaultValue
	return variable
},
moveArrayItem: function(arr, from, to)
{
	if (from < 0)
		from = arr.length + from
	var element = arr[from]
	arr.splice(from, 1)
	arr.splice(to, 0, element)
	return arr
},

isError: function(obj)
{
	return obj instanceof Error
},

isSubset: function(test, all)
{
	var subset = true
	_.each(test, function(val)
	{
		subset = subset && _.includes(all, val)
	})
	return subset
},

/*
	Method: joinURL

	Combines all string arguments to function.
*/
joinUrl: function()
{
	if (arguments.length < 2)
		return arguments
	var combined = ''
	_.each(arguments, function(url)
	{
		if (combined.length &&
			combined.slice(-1) != '/')
			combined += '/'
		if (url[0] == '/')
			url = url.slice(1)
		combined += url
	})
	return combined
},

// Skipped unicodeToString, not needed in javascript




// Javascript only
//////////////////////////////////////////////////

// fix: should be able to make these generic
// and just do clientOnly but arguments magic variable
// doesn't seem to work reliably with tests
clientOnly: function(func, context)
{
	return function()
	{
		if (helpers.isClient)
			func.apply(context, arguments)
	}
},
serverOnly: function(func, context)
{
	return function()
	{
		if (helpers.isServer)
			func.apply(context, arguments)
	}
},

parseQueryString: function(queryString)
{
	// lob off the '?' at the head
	queryString = queryString.substring( queryString.indexOf('?') + 1 )

	var params = {}
	var queryParts = decodeURI(queryString).split(/&/g)
	_.each(queryParts, function(val)
		{
			var parts = val.split('=')
			if (parts.length >= 1)
			{
				val = undefined
				if (parts.length == 2)
					val = parts[1]
				params[parts[0]] = val
			}
		})
	return params
},

/*
	Method: getGlobal

	Gets a global given a key.
*/
getGlobal: function(key)
{
	if (!_.isUndefined(global))
		return global[key]
	else if (!_.isUndefined(window))
		return window[key]
	return undefined
},
/*
	Method: setGlobal

	Sets a global given a key/value pair.
*/
setGlobal: function(key, val)
{
	if (!_.isUndefined(global))
		global[key] = val
	else if (!_.isUndefined(window))
		window[key] = val
},

/*
	Method: isValidIP

	Tests if an IP is a valid local IP
*/
isValidIP: function(ip)
{
	// split off ipv6 for now
	ip = ip.split(':').slice(-1)
	return validIP.test(ip)
},
/*
	Method: isLocalIP

	Tests if an IP is a valid local IP
*/
isLocalIP: function(ip)
{
	if (!helpers.isValidIP(ip))
		return false

	// split off ipv6 for now
	ip = ip.split(':').slice(-1)
	return localIP.test(ip)
},

// end of module
}

helpers.jQuery = helpers.getGlobal('jQuery')

