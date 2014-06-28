
// Vendor Modules
/////////////////////////
var _ = require('lodash')
// var debug = require('debug')
// debug = debug('helpers')
var crypto = require('crypto')

// Our Modules
/////////////////////////
// var constants = require('../constants')

// Main
/////////////////////////
var helpers = module.exports = {

// Variables
/////////////////////////
isClient: typeof window != 'undefined' && window.document,
isServer: typeof window == 'undefined',

// Methods
/////////////////////////

/*
	Method:  pad

	Pads a number, <num> with zeros so the resulting string is <padding> digits long.
*/
pad: function(num, padding)
{
	num = String(num)
	while (num.length < padding)
		num = '0' + num
	return num
},

/*
	Method: varType

	Returns variable type of value passed in.
*/
varType: function(val)
{
	return ({}).toString.call(val).match(/\s([a-zA-Z]+)/)[1].toLowerCase()
},

/*
	Method: utcTime

	Return current UTC time.
*/
utcTime: function()
{
	var d = new Date()
	return d.getTime() + d.getTimezoneOffset() + d.getTime()
},

/*
	Method: randomHash

	Returns random sha224 hash of given length.  Defaults to 16.
*/
randomHash: function(length)
{
	length = typeof length !== 'undefined' ? length : 16
	return crypto.createHash('sha224').update(crypto.randomBytes(10).toString()).digest('hex').substr(0, length)

},

/*
	Method: makeArrayUnique

	Returns given array with all unique elements.
*/
makeArrayUnique: function(val)
{
	return val.filter(function(value, index, self) {return self.indexOf(value) === index;})
},

/*
	Method: safeFilename

	Removes unsafe characters from file names.
*/
safeFilename: function(filename)
{
	var nameToReturn = ''
	var validChars = '-_.()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	for (var i = 0; i < filename.length; i += 1)
	{
		if (validChars.indexOf(filename[i]) > -1)
			nameToReturn = nameToReturn + filename[i]
	}
	return nameToReturn
},

/*
	Method: movieSafeDim

	Rounds number DOWN to the nearest multiple of 4.
*/
movieSafeDim: function(dim)
{
	return  parseInt(parseInt(dim, 10) * 0.25, 10) * 4
},
// fix: should be able to make these generic
// and just do clientOnly but arguments magic variable
// doesn't seem to work reliably with tests
clientTest: function(func)
{
	return function(description, callback)
	{
		if (helpers.isClient)
			func(description, callback)
	}
},
serverTest: function(func)
{
	return function(description, callback)
	{
		if (helpers.isServer)
			func(description, callback)
	}
},
// Method: collectRegexMatches
// collect all the matches in a string for a given regex object
collectRegexMatches: function(str, regex)
{
	var matches = []
	var match
	do {
		match = regex.exec(str)
		if (match !== null)
			matches.push(match)
	}
	while (match !== null);
	return matches
},

/*
	Method: makeWebSafe

	Takes a string and converts all non-alphanumeric characters to underscores.
	Makes all characters lowercase.
*/
makeWebSafe: function(str)
{
	if (!_.isString(str))
		throw Error('helpers.webSafe requires a string')
	// Everything not a letter or number becomes an underscore
	str = str.replace(/[^A-Za-z0-9]/g, '_')
	// Consecutive underscores become one dash
	// str = str.replace(/\_+/g, '_')
	// Leading underscores go away
	// str = str.replace(/^\_/, '')
	// Trailing underscores go away
	// str = str.replace(/\_$/, '')
	return str.toLowerCase()
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
	var c = {}
	for (var attrname in a) {c[attrname] = a[attrname]}
	for (attrname in b) {c[attrname] = b[attrname]}
	return c
},
/*
	Method: defaultFor

	Returns defaultValue is variable is undefined.
*/
defaultFor: function(variable, defaultValue)
{
	if (typeof variable === 'undefined')
		return defaultValue
	return variable
},
/*
	Method: checkDone

	Performs callback is remaining >= 0.
*/
checkDone: function(remaining, callback, err)
{
	if (!_.isNumber(remaining))
		throw new Error('helpers.checkDone -> Invalid remaining')
	if (err)
	{
		callback(err)
		return 0
	}
	remaining -= 1
	if (remaining <= 0)
	{
		callback(err)
		return 0
	}
	return remaining
},
/*
	Method: getExtensions

	Returns file extension all lowercase, with no whitespace.
*/
getExtension: function(filename)
{
	if (!_.contains(filename, '.'))
		return ''
	return '.' + filename.split('.').pop().toLowerCase().trim()
},
/*
	Method: normalizeExtension

	Returns file extension all lowercase with no whitespace, preceded by a period.
*/
normalizeExtension: function(extension)
{
	extension = extension.toLowerCase().trim()
	if (extension[0] != '.')
		return '.' + extension
	return extension
},
/*
	Method: removeExtension

	Removes extension from filename.
*/
removeExtension: function(filename)
{
	// no toLowerCase otherwise .JPG isn't removed properly
	var ext = '.' + filename.split('.').pop().trim()
	return filename.replace(ext, '')
},

/*
	Method: ensureExtension

	Checks that a given file has the given extension.  If not, appends the extension.
*/
ensureExtension: function(filename, extension)
{
	extension = helpers.normalizeExtension(extension)
	if (helpers.getExtension(filename) != extension)
		return filename + extension
	return filename
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
	return keys.map(function(s) { return s.trim() })
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
	return _.pick(object, function(val, key)
		{
			return (!_.contains(keysToOmit, helpers.parseInt(key)))
		})
},
/*
	Method: collectObjectKeys

	Given a dictionary, returns a dictionary with all entries with keys in keysToKeep.
*/
collectObjectKeys: function(object, keysToKeep)
{
	keysToKeep = helpers.ensureArray(keysToKeep)
	return _.pick(object, function(val, key)
		{
			return _.contains(keysToKeep, helpers.parseInt(key))
		})
},
/*	Method: parseJSON

	Parses given JSON if possible.  If val is a dict, return val.
	If val is a string that can't be parsed, return None.
	If val is not dictionary or string, return val.
*/
// fix: define how this should work and use consistently
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
	Method: parseSort

	Accepts sorts in form 'field:ASC', 'field:-1', or 'field','desc'
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
	Method: parseInt

	Behaves like javascripts parseInt.  Returns 0 if not a number.
*/
parseInt: function(val)
{
	return parseInt(val, 10) || 0
},
// stop an event from bubbling up
/* MOVE OUT */
stopBubble: function(e)
{
	if (!e)
		e = window.event
	//IE9 & Other Browsers
	if (e.stopPropagation)
		e.stopPropagation()
	//IE8 and Lower
	else
		e.cancelBubble = true
},
/*
	Method: capitalize

	Capitalizes first character in the given string.
*/
capitalize: function(str)
{
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
	return (str + '').replace(/^([a-z\u00E0-\u00FC])|\s+([a-z\u00E0-\u00FC])/g, function ($1) {
		return $1.toUpperCase()
	})
},
/* MOVE OUT */
parseQueryString: function(queryString)
{
	if (!_.isString(queryString))
		throw new Error('helpers.parseQueryString -> queryString is not a string: ' + queryString)

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
/* MOVE OUT */
isJQuery: function(obj)
{
	if (!helpers.jQuery)
		return false
	return obj instanceof helpers.jQuery
},
/* MOVE OUT */
isJQueryEvent: function(obj)
{
	if (!helpers.jQuery)
		return false
	return obj instanceof helpers.jQuery.Event
},
/* DELETE? */
isError: function(obj)
{
	return obj instanceof Error
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
callbackError: function(err, callback)
{
	if (callback)
		callback(err)
	return err
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

// Method: nodeStyleCallback
// Creates a node-style callback for backbone sync, fetch, and save calls
nodeStyleCallback: function(options)
{
	if (_.isFunction(options))
	{
		var callback = options
		options = {}
		// Place the success and error methods
		options.success = function success(model, response) {
			callback(null, response)
		}
		options.error = function error(model, response) {
			// Provide the response as the error.
			callback(response, null)
		}
	}
	return options || {}
},

/* MOVE OUT */
setDataAndAttribute: function(elem, key, val)
{
	elem.data(key, val).attr('data-' + key, val)
},

/*
	Method: joinURL

	Combines all string arguments to function.
*/
// fix: check for starting and trailing slashes
joinURL: function()
{
	if (arguments.length < 2)
		return arguments
	var combined = ''
	_.each(arguments, function(url)
	{
		if (_.isString(url))
			combined += url
	})
	return combined
},

/*
	Method: getAlphaNumericOnly

	Removes all non-alphanumeric characters from a string.
*/
_notAlphaNumeric: new RegExp(/[^a-zA-Z0-9_]/g),
getAlphaNumericOnly: function(val)
{
	return val.replace(helpers._notAlphaNumeric, '')
},

// end of module
}

helpers.jQuery = helpers.getGlobal('jQuery')
