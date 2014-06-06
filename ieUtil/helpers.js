
// Vendor Modules
/////////////////////////
var _ = require('lodash')
var debug = require('debug')
debug = debug('helpers')

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
defaultFor: function(variable, defaultValue)
{
	if (typeof variable === 'undefined')
		return defaultValue
	return variable
},
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
getExtension: function(filename)
{
	if (!_.contains(filename, '.'))
		return ''
	return '.' + filename.split('.').pop().toLowerCase().trim()
},
normalizeExtension: function(extension)
{
	extension = extension.toLowerCase().trim()
	if (extension[0] != '.')
		return '.' + extension
	return extension
},
removeExtension: function(filename)
{
	// no toLowerCase otherwise .JPG isn't removed properly
	var ext = '.' + filename.split('.').pop().trim()
	return filename.replace(ext, '')
},

// Method: ensureExtension
// Ensures a filename has a given extension
// ex: test.this would become test.this.jpg
ensureExtension: function(filename, extension)
{
	extension = helpers.normalizeExtension(extension)
	if (helpers.getExtension(filename) != extension)
		return filename + extension
	return filename
},
// Method: parseCommaArray
// Turns 'likes, comments' into ['likes', 'comments']
parseCommaArray: function(val)
{
	// if (!_.isString(val))
	// 	throw new Error('helpers.parseCommaArray -> val must be a string, got:' + val)
	var keys = val.split(',')
	// trim each key
	return keys.map(function(s) { return s.trim() })
},
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
ensureArray: function(val)
{
	if (_.isArray(val))
		return val
	if (_.isUndefined(val))
		return []
	return [val]
},
ensureNumber: function(val)
{
	val = parseFloat(val)
	if (isNaN(val))
		return 0
	return val
},
omitObjectKeys: function(object, keysToOmit)
{
	keysToOmit = helpers.ensureArray(keysToOmit)
	return _.pick(object, function(val, key)
		{
			return !_.contains(keysToOmit, key)
		})
},
collectObjectKeys: function(object, keysToKeep)
{
	keysToKeep = helpers.ensureArray(keysToKeep)
	return _.pick(object, function(val, key)
		{
			return _.contains(keysToKeep, key)
		})
},
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
parseInt: function(val)
{
	return parseInt(val, 10) || 0
},
// stop an event from bubbling up
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
capitalize: function(str)
{
	return str.charAt(0).toUpperCase() + str.slice(1)
},
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
isJQuery: function(obj)
{
	if (!helpers.jQuery)
		return false
	return obj instanceof helpers.jQuery
},
isJQueryEvent: function(obj)
{
	if (!helpers.jQuery)
		return false
	return obj instanceof helpers.jQuery.Event
},
isError: function(obj)
{
	return obj instanceof Error
},
getGlobal: function(key)
{
	if (!_.isUndefined(global))
		return global[key]
	else if (!_.isUndefined(window))
		return window[key]
	return undefined
},
setGlobal: function(key, val)
{
	if (!_.isUndefined(global))
		global[key] = val
	else if (!_.isUndefined(window))
		window[key] = val
},
createHash: function(length)
{
	return Math.random().toString(36).substring(length)
},
callbackError: function(err, callback)
{
	if (callback)
		callback(err)
	return err
},
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

setDataAndAttribute: function(elem, key, val)
{
	elem.data(key, val).attr('data-' + key, val)
},

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
_notAlphaNumeric: new RegExp(/[^a-z0-9_]/g),
getAlphaNumericOnly: function(val)
{
	return val.replace(helpers._notAlphaNumeric, '')
},

// end of module
}

helpers.jQuery = helpers.getGlobal('jQuery')
