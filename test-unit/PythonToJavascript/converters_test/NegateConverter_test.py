from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import NegateConverter

def test_NegateGather_01():
    src = """
        x = not y
    """
    matches = NegateConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.not_word.toString() == 'not'
    assert nodesToString( match.right ) == 'y'


def test_NegateProcess_01():
    src = """
        x = not y
    """
    nodes = parseSource( src )
    cvtr = NegateConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """x = !y"""

def test_NegateProcess_02():
    src = """
        x = not ( fun(a) or nuf( b ) )
    """
    nodes = parseSource( src )
    cvtr = NegateConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """x = !( fun(a) or nuf( b ) )"""
