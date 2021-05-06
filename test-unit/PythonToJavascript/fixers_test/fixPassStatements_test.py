from utils import parseSource, nodesToString, dumpNodes, dumpTree

from fixers import fixPassStatements

def test_fixPassStatements_01():
    src = """
       class DUnitToolErr( Exception ): pass
    """
    nodes = parseSource( src )
    fixPassStatements( nodes )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """class DUnitToolErr( Exception ): /* pass */"""

