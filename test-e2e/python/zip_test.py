import unittest

class ZipTests( unittest.TestCase ):

    def test_zip( self ):
        l1 = [ 'a', 'b', 'c' ]
        l2 = [ 1, 2, 3 ]
        l3 = [ True, False, True ]
        l4 = []
        for v in zip( l1, l2, l3 ):
            l4.append( v )
        assert l4 == [ ( 'a', 1, True ), ( 'b', 2, False ), ( 'c', 3, True ) ]

    def test_zip_differing_lengths( self ):
        l1 = [ 'a', 'b', 'c' ]
        l2 = [ 1, 2, 3, 4, 5, 6 ]
        l3 = [ True, False, True ]
        l4 = []
        for v in zip( l1, l2, l3 ):
            l4.append( v )
        assert l4 == [ ( 'a', 1, True ), ( 'b', 2, False ), ( 'c', 3, True ) ]

