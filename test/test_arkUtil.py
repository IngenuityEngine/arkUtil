
import arkInit
arkInit.init()

import tryout
import arkUtil


class test(tryout.TestSuite):
	title = 'test/test_arkUtil.py'

	def pad(self):
		self.assertEqual(arkUtil.pad(1, 4), '0001')
		self.assertEqual(arkUtil.pad(15, 7), '0000015')
		self.assertEqual(arkUtil.pad(131, 2), '131')

	def varType(self):
		self.assertEqual(arkUtil.varType(4), 'int')
		self.assertEqual(arkUtil.varType('string'), 'str')
		self.assertEqual(arkUtil.varType([1,2,3]), 'list')

	# def parseJSON(self):
	# 	json = '["foo", {"bar":["baz", null, 1.0, 2]}]'
	# 	parsed = arkUtil.parseJSON(json, True)
	# 	print parsed
	# 	self.assertEqual(parsed[0], 'Foo')

	def postStrings(self):
		self.assertEqual(arkUtil.postString({'tea': 'pot', 'cat' : 'dog', 'wow': 'amaze'}), 'tea=pot&wow=amaze&cat=dog')

	def mergeDict(self):
		a = {'a': 'b', 'c': 'd'}
		b = {'e': 'f'}
		c = {'e': {'f':'g'}}
		d = {'e': {'h':'i'}}
		resultAB = {'a': 'b', 'c': 'd', 'e': 'f'}
		resultCD = {'e': {'f': 'g', 'h': 'i'}}
		self.assertEqual(arkUtil.mergeDict(a, b), resultAB)
		self.assertEqual(arkUtil.mergeDict(c, d), resultCD)
		self.assertEqual(arkUtil.mergeDict({1: 2}, {}), {1: 2})
		self.assertEqual(arkUtil.mergeDict({1: 2}, {}), {1: 2})

	def movieSafeDim(self):
		self.assertEqual(arkUtil.movieSafeDim(4), 4)
		self.assertEqual(arkUtil.movieSafeDim(3.9), 0)
		self.assertEqual(arkUtil.movieSafeDim(4.1), 4)
		self.assertEqual(arkUtil.movieSafeDim(11), 8)

	def safeFilename(self):
		self.assertEqual(arkUtil.safeFilename('mike.txt'), 'mike.txt')
		self.assertEqual(arkUtil.safeFilename('mike^^^.txt'), 'mike.txt')
		self.assertEqual(arkUtil.safeFilename('   &&&mike.txt^%&__'), 'mike.txt__')

	def randomHash(self):
		self.assertEqual(len(arkUtil.randomHash()), 16)
		self.assertEqual(len(arkUtil.randomHash(4)), 4)

	def makeArrayUnique(self):
		self.assertEqual(arkUtil.makeArrayUnique([1,2,4]), [1,2,4])
		self.assertEqual(arkUtil.makeArrayUnique([1,2,3,4,3]), [1,2,3,4])
		self.assertEqual(arkUtil.makeArrayUnique([1,2,4,4,4,4,4,4]), [1,2,4])
		self.assertEqual(arkUtil.makeArrayUnique([1,2,4,'a','b','c',1,2,4,'a','b','c']), [1,2,4, 'a','b','c'])

	def makeWebSafe(self):
		self.assertEqual(arkUtil.makeWebSafe('mike%is%cool'), 'mike_is_cool')
		self.assertEqual(arkUtil.makeWebSafe('mike1234'), 'mike1234')
		self.assertEqual(arkUtil.makeWebSafe('mike__1234'), 'mike_1234')
		self.assertEqual(arkUtil.makeWebSafe('    mike  1234^^  '), 'mike_1234')

	def parseCommaArray(self):
		self.assertEqual(arkUtil.parseCommaArray('Mike, is, cool'), ['Mike', 'is', 'cool'])
		self.assertEqual(arkUtil.parseCommaArray('like, comments'), ['like', 'comments'])
		self.assertEqual(arkUtil.parseCommaArray('        wow    ,       amaze      '), ['wow', 'amaze'])

	def appendOrSetArray(self):
		self.assertEqual(arkUtil.appendOrSetArray([1,2,3], 4), [1,2,3,4])
		self.assertEqual(arkUtil.appendOrSetArray(1, [1,2,3]), [1,2,3])
		self.assertEqual(arkUtil.appendOrSetArray(1, 3), [3])
		self.assertEqual(arkUtil.appendOrSetArray(None, None), [])

	def ensureArray(self):
		self.assertEqual(arkUtil.ensureArray([1,2,3]), [1,2,3])
		self.assertEqual(arkUtil.ensureArray(1), [1])
		self.assertEqual(arkUtil.ensureArray(None), [])

	def ensureNumber(self):
		self.assertEqual(arkUtil.ensureNumber(4), 4)
		self.assertEqual(arkUtil.ensureNumber(189.3), 189.3)
		self.assertEqual(arkUtil.ensureNumber('a'), 0)

	def omitObjectKeys(self):
		self.assertEqual(arkUtil.omitObjectKeys({1:2, 3:4, 5:6}, [1]), {3:4, 5:6})
		self.assertEqual(arkUtil.omitObjectKeys({1:2, 3:4, 5:6}, [3,5]), {1: 2})
		self.assertEqual(arkUtil.omitObjectKeys({1:2, 3:4, 5:6}, [4]), {1:2, 3:4, 5:6})

	def collectObjectKeys(self):
		self.assertEqual(arkUtil.collectObjectKeys({1:2, 3:4, 5:6}, [3, 5]), {3:4, 5:6})
		self.assertEqual(arkUtil.collectObjectKeys({1:2, 3:4, 5:6}, [1]), {1: 2})
		self.assertEqual(arkUtil.collectObjectKeys({1:2, 3:4, 5:6}, [4]), {})

	def parseInt(self):
		self.assertEqual(arkUtil.parseInt(4), 4)
		self.assertEqual(arkUtil.parseInt('4a'), 4)
		self.assertEqual(arkUtil.parseInt('4'), 4)
		self.assertEqual(arkUtil.parseInt('abc'), 0)

	def capitalize(self):
		self.assertEqual(arkUtil.capitalize('mike'), 'Mike')
		self.assertEqual(arkUtil.capitalize('Mike'), 'Mike')
		self.assertEqual(arkUtil.capitalize('MIKE'), 'MIKE')
		self.assertEqual(arkUtil.capitalize(' mike'), ' mike')
		self.assertEqual(arkUtil.capitalize('7mike'), '7mike')

	def capitalizeWords(self):
		self.assertEqual(arkUtil.capitalizeWords('mike is great'), 'Mike Is Great')
		self.assertEqual(arkUtil.capitalizeWords('   wow so nice'), '   Wow So Nice')
		self.assertEqual(arkUtil.capitalizeWords(' 7lo 5m2'), ' 7lo 5m2')

	def parseSort(self):
		self.assertEqual(arkUtil.parseSort("field:ASC", None), {'field' : 'field', 'order': 'ASC', 'combined' : 'field:ASC'})
		self.assertEqual(arkUtil.parseSort("field", 1), {'field' : 'field', 'order': 'ASC', 'combined' : 'field:ASC'})
		self.assertEqual(arkUtil.parseSort("field:descending", None), {'field' : 'field', 'order': 'DSC', 'combined' : 'field:DSC'})

	def stringCompare(self):
		self.assertEqual(arkUtil.stringCompare('a', 'b'), -1)
		self.assertEqual(arkUtil.stringCompare('not mike', 'mike'), 1)
		self.assertEqual(arkUtil.stringCompare('wow', 'wow'), 0)

	def getAlphaNumericOnly(self):
		self.assertEqual(arkUtil.getAlphaNumericOnly('mike'), 'mike')
		self.assertEqual(arkUtil.getAlphaNumericOnly('mike__123'), 'mike123')
		self.assertEqual(arkUtil.getAlphaNumericOnly('^$%@^#'), '')

	def getRegexMatches(self):
		self.assertEqual(arkUtil.getRegexMatches('sup yea sup', 'sup'), ['sup', 'sup'])
		self.assertEqual(arkUtil.getRegexMatches('word homey yea', 'sup'), [])
		self.assertEqual(arkUtil.getRegexMatches('1-2-3-4-5', '-[0-9]'), ['-2','-3','-4','-5'])

	def replaceAll(self):
		self.assertEqual(arkUtil.replaceAll('sup yea sup', 'sup', 'b'), 'b yea b')
		self.assertEqual(arkUtil.replaceAll('word homey yea', 'sup', 'yo'), 'word homey yea')
		self.assertEqual(arkUtil.replaceAll('1-2-3-4-5', '[0-9]', '*'), '*-*-*-*-*')

	def defaultFor(self):
		banana = None
		some = 'thing'
		self.assertEqual(arkUtil.defaultFor(banana, 'sup'), 'sup')
		self.assertEqual(arkUtil.defaultFor(some, 'sup'), 'thing')

	def isError(self):
		self.assertEqual(arkUtil.isError(Exception('sup')), True)
		self.assertEqual(arkUtil.isError('sup'), False)

	def isSubset(self):
		self.assertEqual(arkUtil.isSubset(['1'],['1','2']), True)
		self.assertEqual(arkUtil.isSubset(['1','2'],['1']), False)
		self.assertEqual(arkUtil.isSubset(['1','2'],['1', '2']), True)

	def joinUrl(self):
		self.assertEqual(arkUtil.joinUrl('this/','/sweet'),'this/sweet')
		self.assertEqual(arkUtil.joinUrl('this','/sweet'),'this/sweet')
		self.assertEqual(arkUtil.joinUrl('this/','sweet'),'this/sweet')
		self.assertEqual(arkUtil.joinUrl('this/','/sweet/','stuff'),'this/sweet/stuff')

if __name__ == '__main__':
	tryout.run(test)
