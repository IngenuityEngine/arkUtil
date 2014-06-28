import sys, os

sys.path.append(os.path.abspath('../ieUtil/'))
import common

import ieInit
ieInit.init()

import unittest

class commonTest(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_pad(self):
		self.assertEqual(common.pad(1, 4), '0001')
		self.assertEqual(common.pad(15, 7), '0000015')
		self.assertEqual(common.pad(131, 2), '131')

	def test_varType(self):
		self.assertEqual(common.varType(4), 'int')
		self.assertEqual(common.varType('string'), 'str')
		self.assertEqual(common.varType([1,2,3]), 'list')

	# def test_parseJSON(self):
	# 	json = '["foo", {"bar":["baz", null, 1.0, 2]}]'
	# 	parsed = common.parseJSON(json, True)
	# 	print parsed
	# 	self.assertEqual(parsed[0], 'Foo')

	def test_postStrings(self):
		self.assertEqual(common.postString({'tea': 'pot', 'cat' : 'dog', 'wow': 'amaze'}), 'tea=pot&wow=amaze&cat=dog')

	def test_mergeDict(self):
		self.assertEqual(common.mergeDict({'a': 'b', 'c': 'd'} , {'e': 'f'}), {'a': 'b', 'c': 'd', 'e': 'f'})
		self.assertEqual(common.mergeDict({1: 2}, {}), {1: 2})

	def test_movieSafeDim(self):
		self.assertEqual(common.movieSafeDim(4), 4)
		self.assertEqual(common.movieSafeDim(3.9), 0)
		self.assertEqual(common.movieSafeDim(4.1), 4)
		self.assertEqual(common.movieSafeDim(11), 8)

	def test_safeFilename(self):
		self.assertEqual(common.safeFilename('mike.txt'), 'mike.txt')
		self.assertEqual(common.safeFilename('mike^^^.txt'), 'mike.txt')
		self.assertEqual(common.safeFilename('   &&&mike.txt^%&__'), 'mike.txt__')

	def test_randomHash(self):
		self.assertEqual(len(common.randomHash()), 16)
		self.assertEqual(len(common.randomHash(4)), 4)

	def test_makeArrayUnique(self):
		self.assertEqual(common.makeArrayUnique([1,2,4]), [1,2,4])
		self.assertEqual(common.makeArrayUnique([1,2,3,4,3]), [1,2,3,4])
		self.assertEqual(common.makeArrayUnique([1,2,4,4,4,4,4,4]), [1,2,4])
		self.assertEqual(common.makeArrayUnique([1,2,4,'a','b','c',1,2,4,'a','b','c']), [1,2,4, 'a','b','c'])

	def test_makeWebSafe(self):
		self.assertEqual(common.makeWebSafe('mike%is%cool'), 'mike_is_cool')
		self.assertEqual(common.makeWebSafe('mike1234'), 'mike1234')
		self.assertEqual(common.makeWebSafe('mike__1234'), 'mike__1234')
		self.assertEqual(common.makeWebSafe('    mike  1234^^  '), '____mike__1234____')

	def test_getExtension(self):
		self.assertEqual(common.getExtension('mike.txt'), '.txt')
		self.assertEqual(common.getExtension('/path/to/file.yolo'), '.yolo')
		self.assertEqual(common.getExtension('path/to/file'), '')

	def test_normalizeExtension(self):
		self.assertEqual(common.normalizeExtension('.TXT'), '.txt')
		self.assertEqual(common.normalizeExtension('png'), '.png')
		self.assertEqual(common.normalizeExtension('Yolo'), '.yolo')

	def test_removeExtension(self):
		self.assertEqual(common.removeExtension('mike.txt'), 'mike')
		self.assertEqual(common.removeExtension('path/to/file.psd'), 'path/to/file')
		self.assertEqual(common.removeExtension('mike'), 'mike')

	def test_ensureExtension(self):
		self.assertEqual(common.ensureExtension('Mike.txt', '.txt'), 'Mike.txt')
		self.assertEqual(common.ensureExtension('Mike', '.txt'), 'Mike.txt')
		self.assertEqual(common.ensureExtension('Mike.txt', '.mb'), 'Mike.txt.mb')

	def test_parseCommaArray(self):
		self.assertEqual(common.parseCommaArray('Mike, is, cool'), ['Mike', 'is', 'cool'])
		self.assertEqual(common.parseCommaArray('like, comments'), ['like', 'comments'])
		self.assertEqual(common.parseCommaArray('           wow           ,           amaze            '), ['wow', 'amaze'])

	def test_appendOrSetArray(self):
		self.assertEqual(common.appendOrSetArray([1,2,3], 4), [1,2,3,4])
		self.assertEqual(common.appendOrSetArray(1, [1,2,3]), [1,2,3])
		self.assertEqual(common.appendOrSetArray(1, 3), [3])
		self.assertEqual(common.appendOrSetArray(None, None), [])

	def test_ensureArray(self):
		self.assertEqual(common.ensureArray([1,2,3]), [1,2,3])
		self.assertEqual(common.ensureArray(1), [1])
		self.assertEqual(common.ensureArray(None), [])

	def test_ensureNumber(self):
		self.assertEqual(common.ensureNumber(4), 4)
		self.assertEqual(common.ensureNumber(189.3), 189.3)
		self.assertEqual(common.ensureNumber('a'), 0)

	def test_omitObjectKeys(self):
		self.assertEqual(common.omitObjectKeys({1:2, 3:4, 5:6}, [1]), {3:4, 5:6})
		self.assertEqual(common.omitObjectKeys({1:2, 3:4, 5:6}, [3,5]), {1: 2})
		self.assertEqual(common.omitObjectKeys({1:2, 3:4, 5:6}, [4]), {1:2, 3:4, 5:6})

	def test_collectObjectKeys(self):
		self.assertEqual(common.collectObjectKeys({1:2, 3:4, 5:6}, [3, 5]), {3:4, 5:6})
		self.assertEqual(common.collectObjectKeys({1:2, 3:4, 5:6}, [1]), {1: 2})
		self.assertEqual(common.collectObjectKeys({1:2, 3:4, 5:6}, [4]), {})

	def test_parseInt(self):
		self.assertEqual(common.parseInt(4), 4)
		self.assertEqual(common.parseInt('4a'), 4)
		self.assertEqual(common.parseInt('4'), 4)
		self.assertEqual(common.parseInt('abc'), 0)

	def test_capitalize(self):
		self.assertEqual(common.capitalize('mike'), 'Mike')
		self.assertEqual(common.capitalize('Mike'), 'Mike')
		self.assertEqual(common.capitalize('MIKE'), 'MIKE')
		self.assertEqual(common.capitalize(' mike'), ' mike')
		self.assertEqual(common.capitalize('7mike'), '7mike')

	def test_capitalizeWords(self):
		self.assertEqual(common.capitalizeWords('mike is great'), 'Mike Is Great')
		self.assertEqual(common.capitalizeWords('   wow so nice'), '   Wow So Nice')
		self.assertEqual(common.capitalizeWords(' 7lo 5m2'), ' 7lo 5m2')

	def test_parseSort(self):
		self.assertEqual(common.parseSort("field:ASC", None), {'field' : 'field', 'order': 'ASC', 'combined' : 'field:ASC'})
		self.assertEqual(common.parseSort("field", 1), {'field' : 'field', 'order': 'ASC', 'combined' : 'field:ASC'})
		self.assertEqual(common.parseSort("field:descending", None), {'field' : 'field', 'order': 'DSC', 'combined' : 'field:DSC'})

	def test_stringCompare(self):
		self.assertEqual(common.stringCompare('a', 'b'), -1)
		self.assertEqual(common.stringCompare('not mike', 'mike'), 1)
		self.assertEqual(common.stringCompare('wow', 'wow'), 0)

	def test_getAlphaNumericOnly(self):
		self.assertEqual(common.getAlphaNumericOnly('mike'), 'mike')
		self.assertEqual(common.getAlphaNumericOnly('mike__123'), 'mike123')
		self.assertEqual(common.getAlphaNumericOnly('^$%@^#'), '')

if __name__ == '__main__':
	unittest.main()