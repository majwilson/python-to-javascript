from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import ForLoopConverter
from fixers import fixIndents

def test_ForLoopGather_01():
    src = """
        for x in container:
            y = x
    """
    matches = ForLoopConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.for_word.toString() == 'for'
    assert match.loop_vars.toString() == 'x'
    assert match.in_word.toString() == 'in'
    assert match.iterable.toString() == 'container'
    assert match.for_colon.toString() == ':'
    assert match.for_suite.toString() == 'y = x'


def test_ForLoopGather_02():
    src = """
        for idx, x in enumerate( zip( l1, l2 ) ):
            doit( idx, x )
    """
    matches = ForLoopConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.for_word.toString() == 'for'
    assert match.loop_vars.toString() == 'idx, x'
    assert match.in_word.toString() == 'in'
    assert match.iterable.toString() == 'enumerate( zip( l1, l2 ) )'
    assert match.for_colon.toString() == ':'
    assert match.for_suite.toString() == 'doit( idx, x )'


def test_ForLoopProcess_01():
    src = """
    for x in y:
        doit( x )
    """
    nodes = parseSource( src )
    fixIndents( nodes )
    cvtr = ForLoopConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """for( let x of y ) {
    doit( x )
}"""

def test_ForLoopProcess_02():
    src = """
    if 1:
        for idx, x in enumerate( zip( l1, l2 ) ):
            doit( x )
        return 123
    """
    nodes = parseSource( src )
    fixIndents( nodes )
    cvtr = ForLoopConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpLines( nodesToString( nodes ) )
    assert nodesToString( nodes ) == """if 1:
    for( let [ idx, x ] of enumerate( zip( l1, l2 ) ) ) {
        doit( x )
    }
    return 123"""

def test_ForLoopProcess_03():
    src = """
    for x in c1:
        for y in c2:
            for z in c3:
                doit( x, y, z )
    """
    nodes = parseSource( src )
    fixIndents( nodes )
    cvtr = ForLoopConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """for( let x of c1 ) {
    for( let y of c2 ) {
        for( let z of c3 ) {
            doit( x, y, z )
        }

    }
}"""

def test_ForLoopProcess_04():
    src = """
    for ( x, y ) in y:
        doit( x, y )
    """
    nodes = parseSource( src )
    fixIndents( nodes )
    cvtr = ForLoopConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpLines( nodesToString( nodes ) )
    assert nodesToLines( nodes ) == [
         'for( let [ x, y ] of y ) {',
        '    doit( x, y )',
        '}',
    ]
