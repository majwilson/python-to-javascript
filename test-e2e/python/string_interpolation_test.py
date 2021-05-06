import unittest

def getStrings():
    return ( "world", "how", "are", "you" )

class StringInterpolationTests( unittest.TestCase ):

    def test_StringInterpolation_01( self ):
        r = "hello %s" % "world"
        assert r == "hello world"

    def test_StringInterpolation_02( self ):
        s = "hello %s %s %s %s"
        r = s % ( "world", "how", "are", "you" )
        assert r == "hello world how are you"

    def test_StringInterpolation_03( self ):
        s = "hello %s %s %s %s"
        r = s % getStrings()
        assert r == "hello world how are you"

