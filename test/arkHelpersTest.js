// Vendor Modules
////////////////////////
// var _ = require('lodash')
var expect = require('expect.js')

var describe = global.describe
var it = global.it


describe('helpers', function() {

	var helpers

	it ('should load', function() {
		helpers = require('../arkHelpers/arkUtil.js')
	})

	it ('should pad', function() {
		expect(helpers.pad(42, 4)).to.be('0042')
		expect(helpers.pad(5, 6)).to.be('000005')
		expect(helpers.pad(123, 2)).to.be('123')
	})

	it ('should varType', function() {
		expect(helpers.varType(4)).to.be('number')
		expect(helpers.varType({1: 2})).to.be('object')
		expect(helpers.varType('abc')).to.be('string')
	})

	it ('should randomHash', function() {
		expect(helpers.randomHash().length).to.be(16)
		expect(helpers.randomHash(4).length).to.be(4)
	})

	it ('should makeArrayUnique', function() {
		expect(helpers.makeArrayUnique([1,2,3]).length).to.be([1,2,3].length)
		expect(helpers.makeArrayUnique([1,2,3,4,3]).length).to.be([1,2,3,4].length)
		expect(helpers.makeArrayUnique(['a','b','c','a','b','c']).length).to.be(['a','b','c'].length)
		expect(helpers.makeArrayUnique([1,'a','a',1]).length).to.be([1, 'a'].length)
	})

	it ('should safeFilename', function() {
		expect(helpers.safeFilename('m4#1%')).to.equal('m41')
		expect(helpers.safeFilename('mikke')).to.be('mikke')
		expect(helpers.safeFilename('&&&test!!!')).to.be('test')
	})

	it ('should movieSafeDim', function() {
		expect(helpers.movieSafeDim(4)).to.be(4)
		expect(helpers.movieSafeDim(7)).to.be(4)
		expect(helpers.movieSafeDim(8.1)).to.be(8)
		expect(helpers.movieSafeDim(11.99999)).to.be(8)
	})

	it ('should makeWebSafe', function() {
		expect(helpers.makeWebSafe('mike%is%cool')).to.be('mike_is_cool')
		expect(helpers.makeWebSafe('website')).to.be('website')
		expect(helpers.makeWebSafe('WEBSITE^^^IN^CAPS')).to.be('website___in_caps')
	})

	it ('should postString', function() {
		expect(helpers.postString({'a': 'b', 'cat': 'dog'})).to.be('a=b&cat=dog')
		expect(helpers.postString({123: 456, 'yolo': 'swag'})).to.be('123=456&yolo=swag')
	})

	it ('should mergeObject', function() {
		expect(String(helpers.mergeObject({1: 2}, {2: 3}))).to.equal(String({1: 2, 2: 3}))
		expect(String(helpers.mergeObject({'a': 'b', 1: 2}, {'c': 'd', 2: 1, 1: 3}))).to.equal(String({'a': 'b', 1: 3, 'c': 'd', 2: 1}))
	})

	it ('should parseCommaArray', function() {
		expect(helpers.parseCommaArray('like, comments')).to.contain('like')
		expect(helpers.parseCommaArray('like, comments')).to.contain('comments')
		expect(helpers.parseCommaArray('   wow   , so   , nice')).to.contain('wow')
		expect(helpers.parseCommaArray('   wow   , so   , nice')).to.contain('so')
		expect(helpers.parseCommaArray('   wow   , so   , nice')).to.contain('nice')
		expect(helpers.parseCommaArray('')).to.contain('')
	})

	it ('should appendOrSetArray', function() {
		expect(helpers.appendOrSetArray([1,2,3], 4)).to.contain(4)
		expect(helpers.appendOrSetArray(1, 3)).to.contain(3)
		expect(helpers.appendOrSetArray(1, [3])).to.contain(3)
		expect(helpers.appendOrSetArray(null, null).length).to.be(0)
	})

	it ('should ensureArray', function() {
		expect(helpers.ensureArray([1,2,3])).to.contain(1)
		expect(helpers.ensureArray([1,2,3])).to.contain(2)
		expect(helpers.ensureArray([1,2,3])).to.contain(3)
		expect(helpers.ensureArray(1)).to.contain(1)
		expect(helpers.ensureArray().length).to.be(0)
	})

	it ('should ensureNumber', function() {
		expect(helpers.ensureNumber(4)).to.be(4)
		expect(helpers.ensureNumber('a')).to.be(0)
		expect(helpers.ensureNumber('3a')).to.be(3)
		expect(helpers.ensureNumber('34')).to.be(34)
		expect(helpers.ensureNumber('4.2')).to.be(4.2)
	})

	it ('should omitObjectKeys', function() {
		var obj = {1: 2, 3: 4, 5: 6}
		expect(helpers.omitObjectKeys(obj, [1])).to.eql({3: 4, 5: 6})
		expect(helpers.omitObjectKeys(obj, [3, 5])).to.eql({1: 2})
		expect(helpers.omitObjectKeys(obj, 3)).to.eql({1: 2, 5: 6})
		expect(helpers.omitObjectKeys(obj, [4])).to.eql(obj)
	})

	it ('should collectObjectKeys', function() {
		var obj = {1: 2, 3: 4, 5: 6}
		expect(helpers.collectObjectKeys(obj, [1])).to.eql({1: 2})
		expect(helpers.collectObjectKeys(obj, [3, 5])).to.eql({3: 4, 5: 6})
		expect(helpers.collectObjectKeys(obj, 3)).to.eql({3: 4})
		expect(helpers.collectObjectKeys(obj, [4])).to.eql({})
	})

	it ('should parseJSON', function() {
		var obj = '{ "name": "Mike" }'
		var parsed = helpers.parseJSON(obj)
		expect(parsed.name).to.be("Mike")
	})

	it ('should parseSort', function() {
		expect(helpers.parseSort('field:ASC')).to.eql({'field': 'field', 'order': 'ASC', 'combined': 'field:ASC'})
		expect(helpers.parseSort('field:1')).to.eql({'field': 'field', 'order': 'ASC', 'combined': 'field:ASC'})
		expect(helpers.parseSort('field:descending')).to.eql({'field': 'field', 'order': 'DSC', 'combined': 'field:DSC'})
	})

	it ('should parseInt', function() {
		expect(helpers.parseInt(4)).to.be(4)
		expect(helpers.parseInt('3')).to.be(3)
		expect(helpers.parseInt('4b')).to.be(4)
		expect(helpers.parseInt('yolo')).to.be(0)
	})

	it ('should capitalize', function() {
		expect(helpers.capitalize('mike')).to.be('Mike')
		expect(helpers.capitalize('MIKE')).to.be('MIKE')
	})

	it ('should capitalizeWords', function() {
		expect(helpers.capitalizeWords('test this function')).to.be('Test This Function')
		expect(helpers.capitalizeWords('kevin van zonneveld')).to.be('Kevin Van Zonneveld')
		expect(helpers.capitalizeWords('   lots   OF .  spaCes')).to.be('   Lots   OF .  SpaCes')
	})

	it ('should stringCompare', function() {
		expect(helpers.stringCompare('a', 'b')).to.be(-1)
		expect(helpers.stringCompare('not mike', 'mike')).to.be(1)
		expect(helpers.stringCompare('oh hey', 'oh hey')).to.be(0)
	})

	it ('should joinURL', function() {
		expect(helpers.joinURL('url1', 'url2')).to.be('url1url2')
		expect(helpers.joinURL('url1', 54, 'url2')).to.be('url1url2')
	})

	it ('should getAlphaNumericOnly', function() {
		expect(helpers.getAlphaNumericOnly('Mike')).to.be('Mike')
		expect(helpers.getAlphaNumericOnly('Mike%%%1234')).to.be('Mike1234')
		expect(helpers.getAlphaNumericOnly('***Mike Wow***  ')).to.be('MikeWow')
	})

})