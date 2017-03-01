// Vendor Modules
////////////////////////
// var _ = require('lodash')
var expect = require('expect.js')

var describe = global.describe
var it = global.it


describe('arkUtil', function() {

	var arkUtil

	it ('should load', function() {
		arkUtil = require('../arkUtil/arkUtil.js')
	})

	it ('isServer and isClient', function() {
		expect(arkUtil.isServer).to.be(true)
		expect(arkUtil.isClient).to.be(false)
	})

	it ('should pad', function() {
		expect(arkUtil.pad(42, 4)).to.be('0042')
		expect(arkUtil.pad(5, 6)).to.be('000005')
		expect(arkUtil.pad(123, 2)).to.be('123')
	})

	it ('should varType', function() {
		expect(arkUtil.varType(4)).to.be('number')
		expect(arkUtil.varType({1: 2})).to.be('object')
		expect(arkUtil.varType('abc')).to.be('string')
	})

	it ('should makeArrayUnique', function() {
		expect(arkUtil.makeArrayUnique([1,2,3]).length).to.be([1,2,3].length)
		expect(arkUtil.makeArrayUnique([1,2,3,4,3]).length).to.be([1,2,3,4].length)
		expect(arkUtil.makeArrayUnique(['a','b','c','a','b','c']).length).to.be(['a','b','c'].length)
		expect(arkUtil.makeArrayUnique([1,'a','a',1]).length).to.be([1, 'a'].length)
	})

	it ('should safeFilename', function() {
		expect(arkUtil.safeFilename('m4#1%')).to.equal('m41')
		expect(arkUtil.safeFilename('mikke')).to.be('mikke')
		expect(arkUtil.safeFilename('&&&test!!!')).to.be('test')
	})

	it ('should movieSafeDim', function() {
		expect(arkUtil.movieSafeDim(4)).to.be(4)
		expect(arkUtil.movieSafeDim(7)).to.be(4)
		expect(arkUtil.movieSafeDim(8.1)).to.be(8)
		expect(arkUtil.movieSafeDim(11.99999)).to.be(8)
	})

	it ('should makeWebSafe', function() {
		expect(arkUtil.makeWebSafe('mike%is%cool')).to.be('mike_is_cool')
		expect(arkUtil.makeWebSafe('website')).to.be('website')
		expect(arkUtil.makeWebSafe('WEBSITE^^^IN^CAPS')).to.be('website_in_caps')
	})

	it ('should postString', function() {
		expect(arkUtil.postString({'a': 'b', 'cat': 'dog'})).to.be('a=b&cat=dog')
		expect(arkUtil.postString({123: 456, 'yolo': 'swag'})).to.be('123=456&yolo=swag')
	})

	it ('should mergeObject', function() {
		expect(String(arkUtil.mergeObject({1: 2}, {2: 3}))).to.equal(String({1: 2, 2: 3}))
		expect(String(arkUtil.mergeObject({'a': 'b', 1: 2}, {'c': 'd', 2: 1, 1: 3}))).to.equal(String({'a': 'b', 1: 3, 'c': 'd', 2: 1}))
	})

	it ('should parseCommaArray', function() {
		expect(arkUtil.parseCommaArray('like, comments')).to.contain('like')
		expect(arkUtil.parseCommaArray('like, comments')).to.contain('comments')
		expect(arkUtil.parseCommaArray('   wow   , so   , nice')).to.contain('wow')
		expect(arkUtil.parseCommaArray('   wow   , so   , nice')).to.contain('so')
		expect(arkUtil.parseCommaArray('   wow   , so   , nice')).to.contain('nice')
		expect(arkUtil.parseCommaArray('')).to.contain('')
	})

	it ('should parseFrameRange', function() {
		var parsed = arkUtil.parseFrameRange('1-10')
		console.log(parsed)
		expect(parsed.length).to.be(10)
		expect(parsed).to.contain(1)
		expect(parsed).to.contain(10)

		parsed = arkUtil.parseFrameRange('1-3,5,12')
		console.log(parsed)
		expect(parsed.length).to.be(5)
		expect(parsed).to.contain(1)
		expect(parsed).to.not.contain(4)
		expect(parsed).to.contain(5)
		expect(parsed).to.contain(12)

		parsed = arkUtil.parseFrameRange('12')
		console.log(parsed)
		expect(parsed.length).to.be(1)
		expect(parsed).to.contain(12)

		parsed = arkUtil.parseFrameRange(12)
		console.log(parsed)
		expect(parsed.length).to.be(1)
		expect(parsed).to.contain(12)

		parsed = arkUtil.parseFrameRange(12.1)
		console.log(parsed)
		expect(parsed.length).to.be(1)
		expect(parsed).to.contain(12)

		parsed = arkUtil.parseFrameRange('1001-1001')
		console.log(parsed)
		expect(parsed.length).to.be(1)
		expect(parsed).to.contain(1001)
	})

	it ('should appendOrSetArray', function() {
		expect(arkUtil.appendOrSetArray([1,2,3], 4)).to.contain(4)
		expect(arkUtil.appendOrSetArray(1, 3)).to.contain(3)
		expect(arkUtil.appendOrSetArray(1, [3])).to.contain(3)
		expect(arkUtil.appendOrSetArray(null, null).length).to.be(0)
	})

	it ('should ensureArray', function() {
		expect(arkUtil.ensureArray([1,2,3])).to.contain(1)
		expect(arkUtil.ensureArray([1,2,3])).to.contain(2)
		expect(arkUtil.ensureArray([1,2,3])).to.contain(3)
		expect(arkUtil.ensureArray(1)).to.contain(1)
		expect(arkUtil.ensureArray().length).to.be(0)
	})

	it ('should ensureNumber', function() {
		expect(arkUtil.ensureNumber(4)).to.be(4)
		expect(arkUtil.ensureNumber('a')).to.be(0)
		expect(arkUtil.ensureNumber('3a')).to.be(3)
		expect(arkUtil.ensureNumber('34')).to.be(34)
		expect(arkUtil.ensureNumber('4.2')).to.be(4.2)
	})

	it ('should omitObjectKeys', function() {
		var obj = {1: 2, 3: 4, 5: 6}
		expect(arkUtil.omitObjectKeys(obj, [1])).to.eql({3: 4, 5: 6})
		expect(arkUtil.omitObjectKeys(obj, [3, 5])).to.eql({1: 2})
		expect(arkUtil.omitObjectKeys(obj, 3)).to.eql({1: 2, 5: 6})
		expect(arkUtil.omitObjectKeys(obj, [4])).to.eql(obj)
	})

	it ('should collectObjectKeys', function() {
		var obj = {1: 2, 3: 4, 5: 6}
		expect(arkUtil.collectObjectKeys(obj, [1])).to.eql({1: 2})
		expect(arkUtil.collectObjectKeys(obj, [3, 5])).to.eql({3: 4, 5: 6})
		expect(arkUtil.collectObjectKeys(obj, 3)).to.eql({3: 4})
		expect(arkUtil.collectObjectKeys(obj, [4])).to.eql({})
	})

	it ('should parseJSON', function() {
		var obj = '{ "name": "Mike" }'
		var parsed = arkUtil.parseJSON(obj)
		expect(parsed.name).to.be("Mike")
	})

	it ('should parseSort', function() {
		expect(arkUtil.parseSort('field:ASC')).to.eql({'field': 'field', 'order': 'ASC', 'combined': 'field:ASC'})
		expect(arkUtil.parseSort('field:1')).to.eql({'field': 'field', 'order': 'ASC', 'combined': 'field:ASC'})
		expect(arkUtil.parseSort('field:descending')).to.eql({'field': 'field', 'order': 'DSC', 'combined': 'field:DSC'})
	})

	it ('should parseInt', function() {
		expect(arkUtil.parseInt(4)).to.be(4)
		expect(arkUtil.parseInt('3')).to.be(3)
		expect(arkUtil.parseInt('4b')).to.be(4)
		expect(arkUtil.parseInt('yolo')).to.be(0)
	})

	it ('should capitalize', function() {
		expect(arkUtil.capitalize('mike')).to.be('Mike')
		expect(arkUtil.capitalize('MIKE')).to.be('MIKE')
	})

	it ('should capitalizeWords', function() {
		expect(arkUtil.capitalizeWords('test this function')).to.be('Test This Function')
		expect(arkUtil.capitalizeWords('kevin van zonneveld')).to.be('Kevin Van Zonneveld')
		expect(arkUtil.capitalizeWords('   lots   OF .  spaCes')).to.be('   Lots   OF .  SpaCes')
	})

	it ('should stringCompare', function() {
		expect(arkUtil.stringCompare('a', 'b')).to.be(-1)
		expect(arkUtil.stringCompare('not mike', 'mike')).to.be(1)
		expect(arkUtil.stringCompare('oh hey', 'oh hey')).to.be(0)
	})

	it ('should joinURL', function() {
		expect(arkUtil.joinUrl('url1', 'url2')).to.be('url1/url2')
		expect(arkUtil.joinUrl('url1', 54, 'url2')).to.be('url1/54/url2')
	})

	it ('should getAlphaNumericOnly', function() {
		expect(arkUtil.getAlphaNumericOnly('Mike')).to.be('Mike')
		expect(arkUtil.getAlphaNumericOnly('Mike%%%1234')).to.be('Mike1234')
		expect(arkUtil.getAlphaNumericOnly('***Mike Wow***  ')).to.be('MikeWow')
	})

	it ('should verify valid ips', function() {
		expect(arkUtil.isValidIP('::ffff:127.0.0.1')).to.be(true)
		expect(arkUtil.isValidIP('127.0.0.1')).to.be(true)
		expect(arkUtil.isValidIP('192.168.0.12')).to.be(true)
		expect(arkUtil.isValidIP('107.168.0.12')).to.be(true)
		expect(arkUtil.isValidIP('18.168.0.12')).to.be(true)
		expect(arkUtil.isValidIP('::ffff:10.168.0.12')).to.be(true)
	})

	it ('should verify local ips', function() {
		expect(arkUtil.isLocalIP('::ffff:127.0.0.1')).to.be(true)
		expect(arkUtil.isLocalIP('127.0.0.1')).to.be(true)
		expect(arkUtil.isLocalIP('192.168.0.12')).to.be(true)
		expect(arkUtil.isLocalIP('107.168.0.12')).to.be(false)
		expect(arkUtil.isLocalIP('18.168.0.12')).to.be(false)
		expect(arkUtil.isLocalIP('::ffff:10.168.0.12')).to.be(true)
	})

})