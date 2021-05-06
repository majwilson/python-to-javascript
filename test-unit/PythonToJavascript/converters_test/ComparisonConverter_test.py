from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import ComparisonConverter

def test_ComparisonGather_01():
    src = """
        x == y; x < y; x > y; x >= y; x <= y; x <> y; x != y; x in y; x is y
    """
    # dumpTree( parseSource( src ) )
    matches = ComparisonConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert nodesToString( match.left ) == 'x'
    assert nodesToString( match.comp_op ) == '=='
    assert nodesToString( match.right ) == 'y'
    assert nodesToString( matches[ 3 ].comp_op ) == '>='
    assert nodesToString( matches[ 7 ].comp_op ) == 'in'

def test_ComparisonGather_02():
    src = """
        x is not y; x not in y
    """
    # dumpTree( parseSource( src ) )

    matches = ComparisonConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert nodesToString( match.left ) == 'x'
    assert nodesToString( match.comp_op ) == 'is not'
    assert nodesToString( match.right ) == 'y'
    assert nodesToString( matches[ 1 ].comp_op ) == 'not in'

def test_ComparisonProcess_01():
    src = """
        x == y
    """
    nodes = parseSource( src )
    cvtr = ComparisonConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToString( nodes ) ==  """x === y"""

def test_ComparisonProcess_02():
    src = """
        x != y
    """
    nodes = parseSource( src )
    cvtr = ComparisonConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToString( nodes ) ==  """x !== y"""

def test_ComparisonProcess_03():
    src = """
        x is None
    """
    nodes = parseSource( src )
    cvtr = ComparisonConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToString( nodes ) ==  """x === null"""

def test_ComparisonProcess_04():
    src = """
        x is not None
    """
    nodes = parseSource( src )
    cvtr = ComparisonConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToString( nodes ) ==  """x !== null"""

def test_ComparisonProcess_05():
    src = """
        x is y
    """
    nodes = parseSource( src )
    cvtr = ComparisonConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToString( nodes ) ==  """Object.is( x, y )"""


def test_ComparisonProcess_06():
    src = """
        x is not y
    """
    nodes = parseSource( src )
    cvtr = ComparisonConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToString( nodes ) ==  """!Object.is( x, y )"""


def test_ComparisonProcess_07():
    src = """
        dflt is ...
    """
    nodes = parseSource( src )
    cvtr = ComparisonConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToString( nodes ) ==  """!_pyjs.isDef( dflt )"""

def test_ComparisonProcess_08():
    src = """
        dflt is not ...
    """
    nodes = parseSource( src )
    cvtr = ComparisonConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToString( nodes ) ==  """_pyjs.isDef( dflt )"""

