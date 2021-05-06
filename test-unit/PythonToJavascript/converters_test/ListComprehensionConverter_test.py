from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import ListComprehensionConverter

def test_ListComprehensionGather_01():
    src = """
        lines = [ "%s:%s;" % ( k, v ) for k, v in strs.items() if v % 2 ]
    """
    matches = ListComprehensionConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.item_value.toString() == '"%s:%s;" % ( k, v )'
    assert match.locals.toString() == 'k, v'
    assert match.looper.toString() == 'strs.items()'
    assert match.test.toString() == 'v % 2'

def test_ListComprehensionProcess_01():
    src = """
        res = [ func( k, v ) for k, v in d.items() ]
    """
    nodes = parseSource( src )
    cvtr = ListComprehensionConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """res = d.items().map( ( [ k, v ] ) => func( k, v ) )"""

def test_ListComprehensionProcess_02():
    src = """
        res = [ v for v in d.values() if v > 123 ]
    """
    nodes = parseSource( src )
    cvtr = ListComprehensionConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """res = d.values().filter( v => v > 123 )"""

def test_ListComprehensionProcess_03():
    src = """
        res = [ v for k, v in d.items() if test( k, v ) > 123 ]
    """
    nodes = parseSource( src )
    cvtr = ListComprehensionConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """res = d.items().filter( ( [ k, v ] ) => test( k, v ) > 123 ).map( ( [ k, v ] ) => v )"""

def test_ListComprehensionProcess_04():
    src = """
        res = [ func( k, v ) for k, v in d.items() if test( k, v ) > 123 ]
    """
    nodes = parseSource( src )
    cvtr = ListComprehensionConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """res = d.items().filter( ( [ k, v ] ) => test( k, v ) > 123 ).map( ( [ k, v ] ) => func( k, v ) )"""

def test_ListComprehensionProcess_05():
    src = """
        res = [ ( k, v ) for k, v in d.items() if test( k, v ) > 123 ]
    """
    nodes = parseSource( src )
    cvtr = ListComprehensionConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """res = d.items().filter( ( [ k, v ] ) => test( k, v ) > 123 )"""
