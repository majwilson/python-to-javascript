import unittest

def getStrings():
    return ( "world", "how", "are", "you" )

class ListSliceTests( unittest.TestCase ):

    def test_ListSlice_01( self ):
        l = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
        assert l[ 3: 8 ] == [ 3, 4, 5, 6, 7 ]

    def test_ListSlice_02( self ):
        l = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
        assert l[ 3: ] == [ 3, 4, 5, 6, 7, 8, 9 ]

    def test_ListSlice_03( self ):
        l = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
        assert l[ : 8 ] == [ 0, 1, 2, 3, 4, 5, 6, 7 ]

    def test_ListSlice_04( self ):
        l = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
        assert l[ : ] == [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]

    def test_ListSlice_05( self ):
        l = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
        assert l[ 2 : -3 ] == [ 2, 3, 4, 5, 6 ]

