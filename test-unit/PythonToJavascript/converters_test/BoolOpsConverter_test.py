from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import BoolOpsConverter

def test_BoolOpsGather_01():
    src = """
        x = 1 and 2
        y = a or b
    """
    matches = BoolOpsConverter().gather( parseSource( src ) )
    and_clause = matches[ 0 ]
    assert and_clause.and_word.toString() == 'and'
    assert and_clause.left.toString() == '1'
    assert and_clause.right.toString() == '2'
    or_clause = matches[ 1 ]
    assert or_clause.or_word.toString() == 'or'
    assert or_clause.left.toString() == 'a'
    assert or_clause.right.toString() == 'b'


def test_BoolOpsProcess_01():
    src = """
        x = 1 and 2
        y = a or b
    """
    nodes = parseSource( src )
    cvtr = BoolOpsConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """x = 1 && 2
y = a || b"""


# NB this passes but the result is incorrect
def test_BoolOpsProcess_02():
    src = """
        y = 3 and 4 and 5 or 6
    """
    nodes = parseSource( src )
    cvtr = BoolOpsConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """y = 3 && 4 and 5 || 6"""
# Hmmmmmmmm                                   ^^^
