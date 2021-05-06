import unittest

def getStrings():
    return ( "world", "how", "are", "you" )

class TupleUnpackTests( unittest.TestCase ):

    def test_TupleUnpack_01( self ):
        ( a, b, c ) = ( 1, 2, 3 )
        assert a == 1
        assert b == 2
        assert c == 3

    def test_TupleUnpack_02( self ):
        ( a, b, c, d ) = getStrings()
        assert a == "world"
        assert b == "how"
        assert c == "are"
        assert d == "you"

    def test_TupleUnpack_03( self ):
        ( A, ( a, b, c, d ), B ) = ( "HELLO", getStrings(), "WORLD" )
        assert A == "HELLO"
        assert a == "world"
        assert b == "how"
        assert c == "are"
        assert d == "you"
        assert B == "WORLD"
