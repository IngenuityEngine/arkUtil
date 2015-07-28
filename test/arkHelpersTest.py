import sys, os

sys.path.append(os.path.abspath('../ieUtil/'))
import arkHelpers

import ieInit
ieInit.init()

import unittest

class arkHelpersTest(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_pad(self):
		self.assertEqual(arkHelpers.pad(1, 4), '0001')
		self.assertEqual(arkHelpers.pad(15, 7), '0000015')
		self.assertEqual(arkHelpers.pad(131, 2), '131')

	def test_varType(self):
		self.assertEqual(arkHelpers.varType(4), 'int')
		self.assertEqual(arkHelpers.varType('string'), 'str')
		self.assertEqual(arkHelpers.varType([1,2,3]), 'list')

	# def test_parseJSON(self):
	# 	json = '["foo", {"bar":["baz", null, 1.0, 2]}]'
	# 	parsed = arkHelpers.parseJSON(json, True)
	# 	print parsed
	# 	self.assertEqual(parsed[0], 'Foo')

	def test_postStrings(self):
		self.assertEqual(arkHelpers.postString({'tea': 'pot', 'cat' : 'dog', 'wow': 'amaze'}), 'tea=pot&wow=amaze&cat=dog')

	def test_mergeDict(self):
		self.assertEqual(arkHelpers.mergeDict({'a': 'b', 'c': 'd'} , {'e': 'f'}), {'a': 'b', 'c': 'd', 'e': 'f'})
		self.assertEqual(arkHelpers.mergeDict({1: 2}, {}), {1: 2})

	def test_movieSafeDim(self):
		self.assertEqual(arkHelpers.movieSafeDim(4), 4)
		self.assertEqual(arkHelpers.movieSafeDim(3.9), 0)
		self.assertEqual(arkHelpers.movieSafeDim(4.1), 4)
		self.assertEqual(arkHelpers.movieSafeDim(11), 8)

	def test_safeFilename(self):
		self.assertEqual(arkHelpers.safeFilename('mike.txt'), 'mike.txt')
		self.assertEqual(arkHelpers.safeFilename('mike^^^.txt'), 'mike.txt')
		self.assertEqual(arkHelpers.safeFilename('   &&&mike.txt^%&__'), 'mike.txt__')

	def test_randomHash(self):
		self.assertEqual(len(arkHelpers.randomHash()), 16)
		self.assertEqual(len(arkHelpers.randomHash(4)), 4)

	def test_makeArrayUnique(self):
		self.assertEqual(arkHelpers.makeArrayUnique([1,2,4]), [1,2,4])
		self.assertEqual(arkHelpers.makeArrayUnique([1,2,3,4,3]), [1,2,3,4])
		self.assertEqual(arkHelpers.makeArrayUnique([1,2,4,4,4,4,4,4]), [1,2,4])
		self.assertEqual(arkHelpers.makeArrayUnique([1,2,4,'a','b','c',1,2,4,'a','b','c']), [1,2,4, 'a','b','c'])

	def test_makeWebSafe(self):
		self.assertEqual(arkHelpers.makeWebSafe('mike%is%cool'), 'mike_is_cool')
		self.assertEqual(arkHelpers.makeWebSafe('mike1234'), 'mike1234')
		self.assertEqual(arkHelpers.makeWebSafe('mike__1234'), 'mike__1234')
		self.assertEqual(arkHelpers.makeWebSafe('    mike  1234^^  '), '____mike__1234____')

	def test_getExtension(self):
		self.assertEqual(arkHelpers.getExtension('mike.txt'), '.txt')
		self.assertEqual(arkHelpers.getExtension('/path/to/file.yolo'), '.yolo')
		self.assertEqual(arkHelpers.getExtension('path/to/file'), '')

	def test_normalizeExtension(self):
		self.assertEqual(arkHelpers.normalizeExtension('.TXT'), '.txt')
		self.assertEqual(arkHelpers.normalizeExtension('png'), '.png')
		self.assertEqual(arkHelpers.normalizeExtension('Yolo'), '.yolo')

	def test_removeExtension(self):
		self.assertEqual(arkHelpers.removeExtension('mike.txt'), 'mike')
		self.assertEqual(arkHelpers.removeExtension('path/to/file.psd'), 'path/to/file')
		self.assertEqual(arkHelpers.removeExtension('mike'), 'mike')

	def test_ensureExtension(self):
		self.assertEqual(arkHelpers.ensureExtension('Mike.txt', '.txt'), 'Mike.txt')
		self.assertEqual(arkHelpers.ensureExtension('Mike', '.txt'), 'Mike.txt')
		self.assertEqual(arkHelpers.ensureExtension('Mike.txt', '.mb'), 'Mike.txt.mb')

	def test_parseCommaArray(self):
		self.assertEqual(arkHelpers.parseCommaArray('Mike, is, cool'), ['Mike', 'is', 'cool'])
		self.assertEqual(arkHelpers.parseCommaArray('like, comments'), ['like', 'comments'])
		self.assertEqual(arkHelpers.parseCommaArray('           wow           ,           amaze            '), ['wow', 'amaze'])

	def test_appendOrSetArray(self):
		self.assertEqual(arkHelpers.appendOrSetArray([1,2,3], 4), [1,2,3,4])
		self.assertEqual(arkHelpers.appendOrSetArray(1, [1,2,3]), [1,2,3])
		self.assertEqual(arkHelpers.appendOrSetArray(1, 3), [3])
		self.assertEqual(arkHelpers.appendOrSetArray(None, None), [])

	def test_ensureArray(self):
		self.assertEqual(arkHelpers.ensureArray([1,2,3]), [1,2,3])
		self.assertEqual(arkHelpers.ensureArray(1), [1])
		self.assertEqual(arkHelpers.ensureArray(None), [])

	def test_ensureNumber(self):
		self.assertEqual(arkHelpers.ensureNumber(4), 4)
		self.assertEqual(arkHelpers.ensureNumber(189.3), 189.3)
		self.assertEqual(arkHelpers.ensureNumber('a'), 0)

	def test_omitObjectKeys(self):
		self.assertEqual(arkHelpers.omitObjectKeys({1:2, 3:4, 5:6}, [1]), {3:4, 5:6})
		self.assertEqual(arkHelpers.omitObjectKeys({1:2, 3:4, 5:6}, [3,5]), {1: 2})
		self.assertEqual(arkHelpers.omitObjectKeys({1:2, 3:4, 5:6}, [4]), {1:2, 3:4, 5:6})

	def test_collectObjectKeys(self):
		self.assertEqual(arkHelpers.collectObjectKeys({1:2, 3:4, 5:6}, [3, 5]), {3:4, 5:6})
		self.assertEqual(arkHelpers.collectObjectKeys({1:2, 3:4, 5:6}, [1]), {1: 2})
		self.assertEqual(arkHelpers.collectObjectKeys({1:2, 3:4, 5:6}, [4]), {})

	def test_parseInt(self):
		self.assertEqual(arkHelpers.parseInt(4), 4)
		self.assertEqual(arkHelpers.parseInt('4a'), 4)
		self.assertEqual(arkHelpers.parseInt('4'), 4)
		self.assertEqual(arkHelpers.parseInt('abc'), 0)

	def test_capitalize(self):
		self.assertEqual(arkHelpers.capitalize('mike'), 'Mike')
		self.assertEqual(arkHelpers.capitalize('Mike'), 'Mike')
		self.assertEqual(arkHelpers.capitalize('MIKE'), 'MIKE')
		self.assertEqual(arkHelpers.capitalize(' mike'), ' mike')
		self.assertEqual(arkHelpers.capitalize('7mike'), '7mike')

	def test_capitalizeWords(self):
		self.assertEqual(arkHelpers.capitalizeWords('mike is great'), 'Mike Is Great')
		self.assertEqual(arkHelpers.capitalizeWords('   wow so nice'), '   Wow So Nice')
		self.assertEqual(arkHelpers.capitalizeWords(' 7lo 5m2'), ' 7lo 5m2')

	def test_parseSort(self):
		self.assertEqual(arkHelpers.parseSort("field:ASC", None), {'field' : 'field', 'order': 'ASC', 'combined' : 'field:ASC'})
		self.assertEqual(arkHelpers.parseSort("field", 1), {'field' : 'field', 'order': 'ASC', 'combined' : 'field:ASC'})
		self.assertEqual(arkHelpers.parseSort("field:descending", None), {'field' : 'field', 'order': 'DSC', 'combined' : 'field:DSC'})

	def test_stringCompare(self):
		self.assertEqual(arkHelpers.stringCompare('a', 'b'), -1)
		self.assertEqual(arkHelpers.stringCompare('not mike', 'mike'), 1)
		self.assertEqual(arkHelpers.stringCompare('wow', 'wow'), 0)

	def test_getAlphaNumericOnly(self):
		self.assertEqual(arkHelpers.getAlphaNumericOnly('mike'), 'mike')
		self.assertEqual(arkHelpers.getAlphaNumericOnly('mike__123'), 'mike123')
		self.assertEqual(arkHelpers.getAlphaNumericOnly('^$%@^#'), '')

if __name__ == '__main__':
	unittest.main()