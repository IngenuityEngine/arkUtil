
// Vendor Modules
/////////////////////////
var _ = require('lodash')
var _s = require('underscore.string')
var debug = require('debug')
debug = debug('helpers')

// Our Modules
/////////////////////////
// var constants = require('../constants')
var seed = 156
var clientTest = (typeof process != 'undefined' && process.env.isClient) ||
					(typeof window != 'undefined' && window.document)

// Main
/////////////////////////
var helpers = module.exports = {

// Variables
/////////////////////////
// fix: hax to run in client mode on the server
isClient: clientTest,
isServer: !clientTest,

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
loadLazyImages: function()
{
	var lazyImages = document.getElementsByTagName('img')
	for (var i=0; i<lazyImages.length; i+=1)
	{
		if (lazyImages[i].getAttribute('data-src'))
			lazyImages[i].setAttribute('src', lazyImages[i].getAttribute('data-src'))
	}
},
clamp: function(num, min, max)
{
  return Math.min(Math.max(num, min), max)
},
getSiteRoot: function(coren)
{
	if (helpers.isClient)
		return location.origin
	else if (coren)
		return 'http://127.0.0.1:' + coren.options.basics.port
	return 'http://127.0.0.1'
},
// collect all the matches in a string for a given regex object
// note: /g flag must be set on RegExp(regex, 'g') or /regex/g
collectRegexMatches: function(str, regex)
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
makeWebSafe: function(str)
{
	if (!_.isString(str))
		throw Error('helpers.webSafe requires a string')
	// Everything not a letter or number becomes an underscore
	str = str.replace(/[^A-Za-z0-9]/g, '_')
	// Consecutive underscores become one dash
	str = str.replace(/\_+/g, '_')
	// Leading underscores go away
	str = str.replace(/^\_/, '')
	// Trailing underscores go away
	str = str.replace(/\_$/, '')
	return str.toLowerCase()
},
isSubset: function(test, all)
{
	return test.length === _.intersection(test, all).length
},
pad: function(num, padding, padChar)
{
	padChar = padChar || '0'
	num = num + ''
	if (num.length >= padding)
		return num
	return new Array(padding - num.length + 1).join(padChar) + num
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
removeTrailingSlash: function(url)
{
	// remove trailing slashes
	if (url[url.length-1] == '/')
		return url.slice(0,-1)
	return url
},
// Method: removeClass
// Removes a class from a space-seprated class list
removeClass: function(classes, classToRemove)
{
	if (!classes)
		return ''
	var newClasses = _.without(classes.split(' '), classToRemove)
	if (!newClasses.length)
		return ''
	else if (newClasses.length == 1)
		return newClasses[0]
	return newClasses.join(' ')
},
// Method: addClass
// Adds a class to a space-seprated class list
addClass: function(spaceList, item)
{
	// if there's no existing list
	// just return the item to add
	if (!spaceList || !spaceList.length)
	{
		return item || ''
	}
	// if there's nothing to add,
	// just return the original list
	if (!item || !item.length)
		return spaceList
	return spaceList + ' ' + item
},

// Method: getCSS
// Gets the full css for a given jquery element
getCSS: function(elem)
{
	var sheets = document.styleSheets
	var cssObject = {}
	var r

	function CSSToJSON(css)
	{
		var s = {}
		var i
		if (!css) return s
		if (typeof css == 'string')
		{
			css = css.split(' ')
			for (i in css)
			{
				var l = css[i].split(': ')
				s[l[0].toLowerCase()] = (l[1])
			}
		}
		else
		{
			for (i in css)
			{
				if ((css[i]).toLowerCase)
				{
					s[(css[i]).toLowerCase()] = (css[css[i]])
				}
			}
		}
		return s
	}

	for (var i in sheets)
	{
		var rules = sheets[i].rules || sheets[i].cssRules
		for (r in rules)
		{
			if (elem.is(rules[r].selectorText))
			{
				cssObject = _.extend(cssObject, CSSToJSON(rules[r].style), CSSToJSON(elem.attr('style')))
			}
		}
	}
	return cssObject
},

copyCSS: function(clone, original)
{
	var children
	for (var i = 0; i < original.length; i += 1)
	{
		clone.eq(i).css(helpers.getCSS(original.eq(i)))
		children = clone.eq(i).children()
		if (children.length)
			helpers.copyCSS(children, original.eq(i).children())
	}
},
// Method: cloneWithCSS
// Clone a jquery element with all it's css
cloneWithCSS: function(elem, deep)
{
	var clone = elem.clone(deep)
	helpers.copyCSS(clone, elem)
	return clone
},

// Method: wrapWithEmptyParents
// Wrap a jquery element with it's emptied parents
// typically for the purpose of keeping CSS styles
wrapWithEmptyParents: function(elem, parentSource, levelsToWrap, deep)
{
	var wrapper = parentSource.parent()
	_.each(_.range(levelsToWrap), function()
	{
		elem.wrap(wrapper.clone(deep).empty())
		elem = elem.parent()
		wrapper = wrapper.parent()
	})
	return elem
},

// Method: cloneWithEmptyParents
// Clone a jquery element with it's emptied parents
// typically for the purpose of keeping CSS styles
cloneWithEmptyParents: function(elem, levels, deep)
{
	return helpers
		.wrapWithEmptyParents(elem.clone(deep), elem, levels, deep)
},

// helper for printing comma seperated in logic-less
// template languages
setLastArray: function(arr)
{
	if (_.isObject(arr[arr.length-1]) &&
		!_.has(arr[arr.length-1], 'last'))
		arr[arr.length-1].last = true
	return arr
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
	return _.pickBy(object, function(val, key)
		{
			return !_.includes(keysToOmit, key)
		})
},
/*
	Method: collectObjectKeys

	Given a dictionary, returns a dictionary with all entries with keys in keysToKeep.
*/
collectObjectKeys: function(object, keysToKeep)
{
	keysToKeep = helpers.ensureArray(keysToKeep)
	return _.pickBy(object, function(val, key)
		{
			return _.includes(keysToKeep, key)
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
formalName: function(name)
{
	if (!_.isString(name))
		throw new Error('helpers.formalName -> ' +
			'name is not a string: ' + name)

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
createHash: function(length)
{
	return Math.random().toString(36).substring(length)
},
// Method: random
// Returns a random float between 0 and 1.  Slight bias towards 0 and 1.
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
	return Math.floor(helpers.random() * (max - min + 1)) + min
},

// Method: getRandomFloat
// Returns a random float between min and max exclusive.
getRandomFloat: function(min, max)
{
	return helpers.random() * (max - min) + min
},

// Method: getRandomIndex
// Returns a random index number for a given array
getRandomIndex: function(arr)
{
	return Math.floor(helpers.random() * arr.length)
},

// Method: getRandomIndexValue
// Returns a random index value for a given array
getRandomIndexValue: function(arr)
{
	return arr[helpers.getRandomIndex(arr)]
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

setDataAndAttribute: function(elem, key, val)
{
	elem.data(key, val).attr('data-' + key, val)
},
removeDataAndAttribute: function(elem, key)
{
	elem.removeData(key).attr('data-' + key)
},
replaceAll: function(str, find, replace)
{
	return str.replace(new RegExp(find, 'g'), replace)
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
_notAlphaNumeric: new RegExp(/[^a-z0-9_]/g),
getAlphaNumericOnly: function(val)
{
	return val.replace(helpers._notAlphaNumeric, '')
},


// Methods
/////////////////////////

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


// end of module
}

helpers.jQuery = helpers.getGlobal('jQuery')
