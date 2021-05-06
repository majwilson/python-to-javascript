from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import DecoratorConverter

def test_DecoratorGather_01():
    src = """
        @require_call_auth( "view" )
        def bim():
            pass
    """
    matches = DecoratorConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert nodesToString( match.at_sym ) == '@'
    assert nodesToString( match.decorated ) == 'require_call_auth( "view" )'
    assert str( match.newl ) == '\n'

def test_DecoratorProcess_01():
    src = """
        @require_call_auth( "view" )
        def bim():
            pass
    """
    nodes = parseSource( src )
    cvtr = DecoratorConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToLines( nodes )[ 0 ] == """/* @require_call_auth( "view" ) DECORATOR */"""
