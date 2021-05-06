from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import WhileLoopConverter
from fixers import fixIndents

def test_WhileLoopGather_01():
    src = """
        while self.hasDUnit( name ):
            name = makeAutoDUnitName()
    """
    matches = WhileLoopConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.name.toString() == 'while'
    assert match.test.toString() == 'self.hasDUnit( name )'
    assert match.colon.toString() == ':'
    assert match.suite.toString() == 'name = makeAutoDUnitName()'


def test_WhileLoopProcess_01():
    src = """
        if 1:
            while self.hasDUnit( name ):
                name = makeAutoDUnitName()
            return something
    """
    nodes = parseSource( src )
    fixIndents( nodes )
    cvtr = WhileLoopConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """if 1:
    while( self.hasDUnit( name ) ) {
        name = makeAutoDUnitName()
    }
    return something"""
