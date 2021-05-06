from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import AssignmentConverter

def test_AssignmentGather_01():
    src = """
        x = 1
        self.abc = self.xyz
        a, b, c = func()
    """
    matches = AssignmentConverter().gather( parseSource( src ) )
    assn_clause = matches[ 0 ]
    assert assn_clause.left.toString() == 'x'
    assert assn_clause.equals.toString() == '='
    assert assn_clause.right.toString() == '1'
    assert matches[ 1 ].left.toString() == 'self.abc'
    assert matches[ 1 ].right.toString() == 'self.xyz'
    assert matches[ 2 ].left.toString() == 'a, b, c'
    assert matches[ 2 ].right.toString() == 'func()'

def test_AssignmentGather_02():
    src = """
        [ a, b, c ] = ( 1, 2, 3 )
    """
    matches = AssignmentConverter().gather( parseSource( src ) )
    assn_clause = matches[ 0 ]
    assert assn_clause.left.toString() == '[ a, b, c ]'
    assert assn_clause.equals.toString() == '='
    assert assn_clause.right.toString() == '( 1, 2, 3 )'


def test_AssignmentProcess_01():
    src = """
        x = 1
        self.abc = self.xyz
        a, b, c = func()
    """
    nodes = parseSource( src )
    cvtr = AssignmentConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "let x = 1",
        "self.abc = self.xyz",
        "let a, b, c = func()",
    ]

def test_AssignmentProcess_02():
    src = """
        x = 1
        y = 2
        z = 3
        x = "hello"
        z = 'bye'
    """
    nodes = parseSource( src )
    cvtr = AssignmentConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "let x = 1",
        "let y = 2",
        "let z = 3",
        "x = \"hello\"",
        "z = 'bye'",
    ]

def test_AssignmentProcess_03():
    src = """
        ( a, b, c ) = ( 1, 2, 3 )
    """
    nodes = parseSource( src )
    cvtr = AssignmentConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "let ( a, b, c ) = ( 1, 2, 3 )",
    ]

def test_AssignmentProcess_04():
    src = """
        [ a, b, c ] = ( 1, 2, 3 )
    """
    nodes = parseSource( src )
    cvtr = AssignmentConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "let [ a, b, c ] = ( 1, 2, 3 )",
    ]