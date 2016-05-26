
import os
import sys

sys.path.insert(0,
	os.path.abspath(
		os.path.join(
			os.path.dirname(os.path.realpath(__file__)),
			'..')
		)
	)
import arkUtil

sys.path.append('c:/ie/tryout')
import tryout


class test(tryout.TestSuite):
	title = 'test/test_arkUtil.py'

	def test_pad(self):
		self.assertEqual(arkUtil.pad(1, 4), '0001')
		self.assertEqual(arkUtil.pad(15, 7), '0000015')
		self.assertEqual(arkUtil.pad(131, 2), '131')

	def test_varType(self):
		self.assertEqual(arkUtil.varType(4), 'int')
		self.assertEqual(arkUtil.varType('string'), 'str')
		self.assertEqual(arkUtil.varType([1,2,3]), 'list')

	# def test_parseJSON(self):
	# 	json = '["foo", {"bar":["baz", null, 1.0, 2]}]'
	# 	parsed = arkUtil.parseJSON(json, True)
	# 	print parsed
	# 	self.assertEqual(parsed[0], 'Foo')

	def test_postStrings(self):
		self.assertEqual(arkUtil.postString({'tea': 'pot', 'cat' : 'dog', 'wow': 'amaze'}), 'tea=pot&wow=amaze&cat=dog')

	def test_mergeDict(self):
		self.assertEqual(arkUtil.mergeDict({'a': 'b', 'c': 'd'} , {'e': 'f'}), {'a': 'b', 'c': 'd', 'e': 'f'})
		self.assertEqual(arkUtil.mergeDict({1: 2}, {}), {1: 2})

	def test_movieSafeDim(self):
		self.assertEqual(arkUtil.movieSafeDim(4), 4)
		self.assertEqual(arkUtil.movieSafeDim(3.9), 0)
		self.assertEqual(arkUtil.movieSafeDim(4.1), 4)
		self.assertEqual(arkUtil.movieSafeDim(11), 8)

	def test_safeFilename(self):
		self.assertEqual(arkUtil.safeFilename('mike.txt'), 'mike.txt')
		self.assertEqual(arkUtil.safeFilename('mike^^^.txt'), 'mike.txt')
		self.assertEqual(arkUtil.safeFilename('   &&&mike.txt^%&__'), 'mike.txt__')

	def test_randomHash(self):
		self.assertEqual(len(arkUtil.randomHash()), 16)
		self.assertEqual(len(arkUtil.randomHash(4)), 4)

	def test_makeArrayUnique(self):
		self.assertEqual(arkUtil.makeArrayUnique([1,2,4]), [1,2,4])
		self.assertEqual(arkUtil.makeArrayUnique([1,2,3,4,3]), [1,2,3,4])
		self.assertEqual(arkUtil.makeArrayUnique([1,2,4,4,4,4,4,4]), [1,2,4])
		self.assertEqual(arkUtil.makeArrayUnique([1,2,4,'a','b','c',1,2,4,'a','b','c']), [1,2,4, 'a','b','c'])

	def test_makeWebSafe(self):
		self.assertEqual(arkUtil.makeWebSafe('mike%is%cool'), 'mike_is_cool')
		self.assertEqual(arkUtil.makeWebSafe('mike1234'), 'mike1234')
		self.assertEqual(arkUtil.makeWebSafe('mike__1234'), 'mike__1234')
		self.assertEqual(arkUtil.makeWebSafe('    mike  1234^^  '), '____mike__1234____')

	def test_parseCommaArray(self):
		self.assertEqual(arkUtil.parseCommaArray('Mike, is, cool'), ['Mike', 'is', 'cool'])
		self.assertEqual(arkUtil.parseCommaArray('like, comments'), ['like', 'comments'])
		self.assertEqual(arkUtil.parseCommaArray('           wow           ,           amaze            '), ['wow', 'amaze'])

	def test_appendOrSetArray(self):
		self.assertEqual(arkUtil.appendOrSetArray([1,2,3], 4), [1,2,3,4])
		self.assertEqual(arkUtil.appendOrSetArray(1, [1,2,3]), [1,2,3])
		self.assertEqual(arkUtil.appendOrSetArray(1, 3), [3])
		self.assertEqual(arkUtil.appendOrSetArray(None, None), [])

	def test_ensureArray(self):
		self.assertEqual(arkUtil.ensureArray([1,2,3]), [1,2,3])
		self.assertEqual(arkUtil.ensureArray(1), [1])
		self.assertEqual(arkUtil.ensureArray(None), [])

	def test_ensureNumber(self):
		self.assertEqual(arkUtil.ensureNumber(4), 4)
		self.assertEqual(arkUtil.ensureNumber(189.3), 189.3)
		self.assertEqual(arkUtil.ensureNumber('a'), 0)

	def test_omitObjectKeys(self):
		self.assertEqual(arkUtil.omitObjectKeys({1:2, 3:4, 5:6}, [1]), {3:4, 5:6})
		self.assertEqual(arkUtil.omitObjectKeys({1:2, 3:4, 5:6}, [3,5]), {1: 2})
		self.assertEqual(arkUtil.omitObjectKeys({1:2, 3:4, 5:6}, [4]), {1:2, 3:4, 5:6})

	def test_collectObjectKeys(self):
		self.assertEqual(arkUtil.collectObjectKeys({1:2, 3:4, 5:6}, [3, 5]), {3:4, 5:6})
		self.assertEqual(arkUtil.collectObjectKeys({1:2, 3:4, 5:6}, [1]), {1: 2})
		self.assertEqual(arkUtil.collectObjectKeys({1:2, 3:4, 5:6}, [4]), {})

	def test_parseInt(self):
		self.assertEqual(arkUtil.parseInt(4), 4)
		self.assertEqual(arkUtil.parseInt('4a'), 4)
		self.assertEqual(arkUtil.parseInt('4'), 4)
		self.assertEqual(arkUtil.parseInt('abc'), 0)

	def test_capitalize(self):
		self.assertEqual(arkUtil.capitalize('mike'), 'Mike')
		self.assertEqual(arkUtil.capitalize('Mike'), 'Mike')
		self.assertEqual(arkUtil.capitalize('MIKE'), 'MIKE')
		self.assertEqual(arkUtil.capitalize(' mike'), ' mike')
		self.assertEqual(arkUtil.capitalize('7mike'), '7mike')

	def test_capitalizeWords(self):
		self.assertEqual(arkUtil.capitalizeWords('mike is great'), 'Mike Is Great')
		self.assertEqual(arkUtil.capitalizeWords('   wow so nice'), '   Wow So Nice')
		self.assertEqual(arkUtil.capitalizeWords(' 7lo 5m2'), ' 7lo 5m2')

	def test_parseSort(self):
		self.assertEqual(arkUtil.parseSort("field:ASC", None), {'field' : 'field', 'order': 'ASC', 'combined' : 'field:ASC'})
		self.assertEqual(arkUtil.parseSort("field", 1), {'field' : 'field', 'order': 'ASC', 'combined' : 'field:ASC'})
		self.assertEqual(arkUtil.parseSort("field:descending", None), {'field' : 'field', 'order': 'DSC', 'combined' : 'field:DSC'})

	def test_stringCompare(self):
		self.assertEqual(arkUtil.stringCompare('a', 'b'), -1)
		self.assertEqual(arkUtil.stringCompare('not mike', 'mike'), 1)
		self.assertEqual(arkUtil.stringCompare('wow', 'wow'), 0)

	def test_getAlphaNumericOnly(self):
		self.assertEqual(arkUtil.getAlphaNumericOnly('mike'), 'mike')
		self.assertEqual(arkUtil.getAlphaNumericOnly('mike__123'), 'mike123')
		self.assertEqual(arkUtil.getAlphaNumericOnly('^$%@^#'), '')



if __name__ == '__main__':
	tryout.run(test)
