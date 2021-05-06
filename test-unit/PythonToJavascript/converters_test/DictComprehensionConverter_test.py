from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import DictComprehensionConverter

def test_DictComprehensionGather_01():
    src = """
        d = { k : v * 2 for k, v in kvz if v * 10 > 15 }
    """
    matches = DictComprehensionConverter().gather( parseSource( src ) )
    comp_clause = matches[ 0 ]
    assert comp_clause.item_key.toString() == 'k'
    assert comp_clause.item_value.toString() == 'v * 2'
    assert comp_clause.locals.toString() == 'k, v'
    assert comp_clause.looper.toString() == 'kvz'
    assert comp_clause.test.toString() == 'v * 10 > 15'

def test_DictComprehensionGather_02():
    src = """
        d = { kv[ 0 ] : kv[ 1 ] * 2 for kv in kvz if kv[ 1 ] * 10 > 15 }
    """
    matches = DictComprehensionConverter().gather( parseSource( src ) )
    comp_clause = matches[ 0 ]
    assert comp_clause.item_key.toString() == 'kv[ 0 ]'
    assert comp_clause.item_value.toString() == 'kv[ 1 ] * 2'
    assert comp_clause.locals.toString() == 'kv'
    assert comp_clause.looper.toString() == 'kvz'
    assert comp_clause.test.toString() == 'kv[ 1 ] * 10 > 15'


def test_DictComprehensionProcess_01():
    src = """
         d = { k : v * 2 for k, v in kvz }
    """
    nodes = parseSource( src )
    cvtr = DictComprehensionConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """d = kvz.reduce( ( __map, [ k, v ] ) => ( { ...__map, [ k ]: v * 2 } ), {} )"""

def test_DictComprehensionProcess_02():
    src = """
         d = { k : v * 2 for k, v in kvz if v * 10 > 15 }
    """
    nodes = parseSource( src )
    cvtr = DictComprehensionConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """d = kvz.filter( ( [ k, v ] ) => v * 10 > 15 ).reduce( ( __map, [ k, v ] ) => ( { ...__map, [ k ]: v * 2 } ), {} )"""

def test_DictComprehensionProcess_03():
    src = """
         d = { kv[ 0 ] : kv[ 1 ] * 2 for kv in kvz if kv[ 1 ] * 10 > 15 }
    """
    nodes = parseSource( src )
    cvtr = DictComprehensionConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """d = kvz.filter( kv => kv[ 1 ] * 10 > 15 ).reduce( ( __map, kv ) => ( { ...__map, [ kv[ 0 ] ]: kv[ 1 ] * 2 } ), {} )"""

