from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import StringInterpolationConverter

def test_StringInterpolationGather_01():
    src = """
        astring % aval
    """
    matches = StringInterpolationConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.left.toString() == 'astring'
    assert match.percent_sym.toString() == '%'
    assert match.right.toString() == 'aval'

def test_StringInterpolationGather_02():
    src = """
        "%s:%s" % ( aval, bval )
    """
    matches = StringInterpolationConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.left.toString() == '"%s:%s"'
    assert match.right.toString() == '( aval, bval )'

def test_StringInterpolationProcess_01():
    src = """
        astring % aval
    """
    nodes = parseSource( src )
    cvtr = StringInterpolationConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    if cvtr.USE_PYJS:
        assert nodesToString( nodes ) == \
                """_pyjs.stringInterpolate( astring, [ aval ] )"""
    else:
        assert nodesToString( nodes ) == \
                """[ aval ].reduce( ( a, c ) => a.replace( /%(s|i|r)?/, c.toString () ), astring )"""

def test_StringInterpolationProcess_02():
    src = """
        "%s:%s" % ( aval, bval )
    """
    nodes = parseSource( src )
    cvtr = StringInterpolationConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    if cvtr.USE_PYJS:
        assert nodesToString( nodes ) == \
                """_pyjs.stringInterpolate( \"%s:%s\", ( aval, bval ) )"""
    else:
        assert nodesToString( nodes ) == \
                """( aval, bval ).reduce( ( a, c ) => a.replace( /%(s|i|r)?/, c.toString () ), "%s:%s" )"""

def test_StringInterpolationProcess_03():
    src = """
        return "/__utr-%s/__kyz-%s/__pqw-%s" % self.getSessIds()
    """
    nodes = parseSource( src )
    cvtr = StringInterpolationConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    if cvtr.USE_PYJS:
        assert nodesToString( nodes ) == \
            """return _pyjs.stringInterpolate( \"/__utr-%s/__kyz-%s/__pqw-%s\", self.getSessIds() )"""
    else:
        assert nodesToString( nodes ) == \
            """return self.getSessIds().reduce( ( a, c ) => a.replace( /%(s|i|r)?/, c.toString () ), "/__utr-%s/__kyz-%s/__pqw-%s" )"""

