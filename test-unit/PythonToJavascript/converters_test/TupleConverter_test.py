from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import TupleConverter


def test_TupleGather_01():
    src = """
        l = ( 1, 2, 3 )
    """
    matches = TupleConverter().gather( parseSource( src ) )
    assert matches[ 0 ].contents.toString() == "1, 2, 3"

def test_TupleGather_02():
    src = """
        l = ( 'a', ( 1, 2, 3 ), 'b' )
    """
    matches = TupleConverter().gather( parseSource( src ) )
    assert matches[ 0 ].contents.toString() == "'a', ( 1, 2, 3 ), 'b'"
    assert matches[ 1 ].contents.toString() == "1, 2, 3"

def test_TupleGather_03():
    src = """
        ( a, b, c ) = func( x, y, z )
    """
    matches = TupleConverter().gather( parseSource( src ) )
    assert matches[ 0 ].contents.toString() == "a, b, c"
    assert len( matches ) == 1

def test_TupleProcess_01():
    src = """
        l = ( 1, 2, 3 )
    """
    nodes = parseSource( src )

    cvtr = TupleConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )

    assert nodesToLines( nodes ) == [
        "l = [ 1, 2, 3 ]",
    ]

def test_TupleProcess_02():
    src = """
        l = ( 'a', ( 1, 2, 3 ), 'b' )
    """
    nodes = parseSource( src )

    cvtr = TupleConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )

    assert nodesToLines( nodes ) == [
        "l = [ 'a', [ 1, 2, 3 ], 'b' ]",
    ]

def test_TupleProcess_03():
    src = """
        ( a, b, c ) = func( x, y, z )
    """
    nodes = parseSource( src )

    cvtr = TupleConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )

    assert nodesToLines( nodes ) == [
        "[ a, b, c ] = func( x, y, z )",
    ]
