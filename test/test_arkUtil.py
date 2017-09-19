
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
		self.assertEqual(arkUtil.postString(
			{'tea': 'pot', 'cat' : 'dog', 'wow': 'amaze'}),
			'tea=pot&wow=amaze&cat=dog')

	def mergeDict(self):
		a = {'a': 'b', 'c': 'd'}
		b = {'e': 'f'}
		c = {'e': {'f':'g'}}
		d = {'e': {'h':'i'}}
		e = {'e': 12}
		f = {'e': 14}
		# g = {'e': [12, 11, 10]}
		# h = {'e': [14, 8]}
		resultAB = {'a': 'b', 'c': 'd', 'e': 'f'}
		resultCD = {'e': {'f': 'g', 'h': 'i'}}
		resultEF = {'e': 14}
		# fix: figure out list merging
		# resultGH = {'e': [14, 8, 12, 11, 10]}
		self.assertEqual(arkUtil.mergeDict(a, b), resultAB)
		self.assertEqual(arkUtil.mergeDict(c, d), resultCD)
		self.assertEqual(arkUtil.mergeDict(e, f), resultEF)
		# self.assertEqual(arkUtil.mergeDict(g, h), resultGH)
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

	def parseFrameRange(self):
		parsed = arkUtil.parseFrameRange('1-10')
		print parsed
		self.assertEqual(len(parsed), 10)
		self.assertIn(1, parsed)
		self.assertIn(10, parsed)

		parsed = arkUtil.parseFrameRange('1-3,5,12')
		print parsed
		self.assertEqual(len(parsed), 5)
		self.assertTrue(1 in parsed)
		self.assertTrue(4 not in parsed)
		self.assertTrue(5 in parsed)
		self.assertTrue(12 in parsed)

		parsed = arkUtil.parseFrameRange('12')
		print parsed
		self.assertEqual(len(parsed), 1)
		self.assertTrue(12 in parsed)

		parsed = arkUtil.parseFrameRange(12)
		print parsed
		self.assertEqual(len(parsed), 1)
		self.assertTrue(12 in parsed)

		parsed = arkUtil.parseFrameRange(12.1)
		print parsed
		self.assertEqual(len(parsed), 1)
		self.assertTrue(12 in parsed)

		parsed = arkUtil.parseFrameRange('1001-1001')
		print parsed
		self.assertEqual(len(parsed), 1)
		self.assertTrue(1001 in parsed)

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

	def splitFrameRangeByChunk(self):
		self.assertEqual(arkUtil.splitFrameRangeByChunk({'startFrame': 1001, 'endFrame': 1100}, 4),
			[{'startFrame': 1001, 'endFrame': 1025},
			 {'startFrame': 1026, 'endFrame': 1050},
			 {'startFrame': 1051, 'endFrame': 1075},
			 {'startFrame': 1076, 'endFrame': 1100}])
		self.assertEqual(arkUtil.splitFrameRangeByChunk({'startFrame': 1001, 'endFrame': 1105}, 4),
			[{'startFrame': 1001, 'endFrame': 1026},
			 {'startFrame': 1027, 'endFrame': 1052},
			 {'startFrame': 1053, 'endFrame': 1078},
			 {'startFrame': 1079, 'endFrame': 1105}])
		self.assertEqual(arkUtil.splitFrameRangeByChunk({'startFrame': 1001, 'endFrame': 1095}, 4),
			[{'startFrame': 1001, 'endFrame': 1023},
			 {'startFrame': 1024, 'endFrame': 1046},
			 {'startFrame': 1047, 'endFrame': 1069},
			 {'startFrame': 1070, 'endFrame': 1095}])

	def expand(self):
		self.assertEqual(arkUtil.expand('{root}/{path}/{to}/{file}.{ext}', {'root':'.', 'path': 'a', 'to': 'b', 'file': 'c', 'ext': 'd'}),
			'./a/b/c.d')
		self.assertEqual(arkUtil.expand('{this}/{is}/{partial}', {'this':'expand'}), 'expand/{is}/{partial}')
		self.assertEqual(arkUtil.expand('{this}/{is}/{partial}', {'this':'expand', 'partial': 'still true'}), 'expand/{is}/still true')
		self.assertEqual(arkUtil.expand('', {'a':'b'}), '')

	def regexFromTemplate(self):
		self.assertEqual(arkUtil.regexFromTemplate('{start}.to.{end}'), '^([\w\d%_-]*)\.to\.([\w\d%_-]*)$')
		self.assertEqual(arkUtil.regexFromTemplate('/{start}/to/{end}'), '^/([\w\d%_-]*)/to/([\w\d%_-]*)$')
		self.assertEqual(arkUtil.regexFromTemplate('{root}/{path}/{to}/{file}.{ext}'), '^([\w\d%_-]*)/([\w\d%_-]*)/([\w\d%_-]*)/([\w\d%_-]*)\.([\w\d%_-]*)$')

	def parse(self):
		self.assertEqual(arkUtil.parse('{start}/middle/{end}', 'a/middle/z'), {'start': 'a', 'end': 'z'})
		self.assertEqual(arkUtil.parse('{this}', 'works'), {'this': 'works'})
		self.assertEqual(arkUtil.parse('{root}/Publish/{asdf}', 'path/Publish/asdf'), {'root': 'path', 'asdf': 'asdf'})

		self.assertError(lambda: arkUtil.parse('{a}/b/{c}', 'a/a/b/c'))
		self.assertError(lambda: arkUtil.parse('{a}/b/{c}', 'a/a/b/'))
		self.assertError(lambda: arkUtil.parse('{a}/b/{c}', 'a/b$/c'))

	def matchesData(self):
		_renderPathAbsoluteShort = '/ramburglar/{project}/Workspaces/{sequence}/{shot}/R|renders/{versionName}/'

		self.assertTrue(arkUtil.matchesData(_renderPathAbsoluteShort, {'project': 'a', 'sequence': 'b', 'shot': 'c', 'versionName': 'd'}))
		self.assertFalse(arkUtil.matchesData(_renderPathAbsoluteShort, {'project': 'a', 'shot': 'c', 'versionName': 'd'}))
		self.assertTrue(arkUtil.matchesData(_renderPathAbsoluteShort, {'project': 'a', 'sequence': 'b', 'shot': 'c', 'versionName': 'd', 'extra': 'e'}))
		self.assertFalse(arkUtil.matchesData('{this}/{is}/{partial}', {'this':'expand'}))

	def matchesText(self):
		_sourcePath = 'r:/{project}/Workspaces/{sequence}/{shot}/{assetType}/'
		_filename = '{assetName}_{assetType}_{versionPadding}_{initials}.{extension}'
		path = 'r:/Aeroplane/Workspaces/AER_Video/AER_Airplane_010/Scene/AER_Airplane_020_scene_v004_asd.mb'
		path2 = 'r:/Aeroplane/Workspaces/AER_Video/AER_Airplane_010/Scene/'

		self.assertTrue(arkUtil.matchesText(_sourcePath, path2))
		self.assertFalse(arkUtil.matchesText(_sourcePath, path))
		self.assertTrue(arkUtil.matchesText(_sourcePath + _filename, path))
		self.assertFalse(arkUtil.matchesText(_sourcePath + _filename, path2))


if __name__ == '__main__':
	tryout.run(test)
