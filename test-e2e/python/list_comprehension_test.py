import unittest

class ListComprehensionTests( unittest.TestCase ):

    def test_ListComprehension_01( self ):
        vz = ( 1, 2, 3, 4 )
        l = [ v * 3 for v in vz ]
        assert l == [ 3, 6, 9, 12 ]

    def test_ListComprehension_02( self ):
        vz = ( 1, 2, 3, 4 )
        l = [ v * 3 for v in vz if 10 / v  > 4  ]
        assert l == [ 3, 6 ]

    def test_ListComprehension_03( self ):
        kvz = ( ( 10, 1 ), ( 20, 2 ), ( 30, 3 ) )
        l = [ k * 5 + v for k, v in kvz if v * 10 > 15  ]
        assert l == [ 102, 153 ]

    def test_ListComprehension_04( self ):
        kvz = ( ( 10, 1 ), ( 20, 2 ), ( 30, 3 ) )
        l = [ kv[ 0 ] * 5 + kv[ 1 ] for kv in kvz if kv[ 1 ] * 10 > 15  ]
        assert l == [ 102, 153 ]


