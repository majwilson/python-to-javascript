import unittest

class DictComprehensionTests( unittest.TestCase ):

    def test_dictComprehension_01( self ):
        kvz = ( ( 'a', 1 ), ( 'b', 2 ), ( 'c', 3 ) )
        d = { k : v * 2 for k, v in kvz }
        assert d == { 'a': 2, 'b': 4, 'c': 6 }

    def test_dictComprehension_02( self ):
        kvz = ( ( 'a', 1 ), ( 'b', 2 ), ( 'c', 3 ) )
        d = { k : v * 2 for k, v in kvz if v * 10 > 15 }
        assert d == { 'b': 4, 'c': 6 }

    def test_dictComprehension_03( self ):
        kvz = ( ( 'a', 1 ), ( 'b', 2 ), ( 'c', 3 ) )
        d = { kv[ 0 ] : kv[ 1 ] * 2 for kv in kvz if kv[ 1 ] * 10 > 15 }
        assert d == { 'b': 4, 'c': 6 }
