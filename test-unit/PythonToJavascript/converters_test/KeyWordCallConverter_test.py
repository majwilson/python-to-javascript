from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import KeyWordCallConverter

def test_KeyWordCallGather_01():
    src = """
        x = func( a, b="hello", c=doIt() )
    """
    # dumpTree( parseSource( src ) )

    matches = KeyWordCallConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert len( match.args ) == 5
    assert match.args[ 0 ].node.toString() == 'a'
    assert match.args[ 1 ].node.toString() == ','
    assert match.args[ 2 ].node.toString() == 'b="hello"'
    assert match.args[ 4 ].node.toString() == 'c=doIt()'

def test_KeyWordCallProcess_01():
    src = """
        x = func( a, b="hello", c=doIt() )
    """
    nodes = parseSource( src )
    cvtr = KeyWordCallConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToString( nodes ) ==  """x = func( a, { b: "hello", c: doIt() } )"""


def test_KeyWordCallProcess_02():
    src = """
                self.style_enable_check.setJSCommandVals(
                                        style_path=style_sel.path,
                                        style_name=style_sel.name,
                                        enable="__value__" )
    """
    nodes = parseSource( src )
    cvtr = KeyWordCallConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "self.style_enable_check.setJSCommandVals( {",
        "                        style_path: style_sel.path,",
        "                        style_name: style_sel.name,",
        "                        enable: \"__value__\" } )",
    ]


def test_KeyWordCallProcess_03():
    src = """
        return sorted( props, key=sortKey )
    """
    nodes = parseSource( src )
    cvtr = KeyWordCallConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToString( nodes ) ==  """return sorted( props, { key: sortKey } )"""


