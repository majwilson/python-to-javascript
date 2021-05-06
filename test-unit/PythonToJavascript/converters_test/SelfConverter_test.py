from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import SelfConverter

def test_SelfGather_01():
    src = """
        self.abc = 1
        self.callMeth()
    """
    matches = SelfConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.self.toString() == 'self'
    assert match.dot.toString() == '.'
    assert match.right.toString() == 'abc'
    assert matches[ 1 ].right.toString() == 'callMeth'


def test_SelfGather_02():
    src = """
        self.callMethA( self.callMethB( self.bam ) )
    """
    matches = SelfConverter().gather( parseSource( src ) )
    assert str( matches[ 0 ].right ) + str( matches[ 0 ].rest ) == 'callMethA( self.callMethB( self.bam ) )'
    assert str( matches[ 1 ].right ) + str( matches[ 1 ].rest ) == 'callMethB( self.bam )'
    assert str( matches[ 2 ].right ) == 'bam'


def test_SelfProcess_01():
    src = """
        self.callMethA( self.callMethB( self.bam ) )
    """
    nodes = parseSource( src )
    cvtr = SelfConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """this.callMethA( this.callMethB( this.bam ) )"""

def test_SelfProcess_02():
    src = """
        def func1():
            self.abc = 1
            self.callMeth()
            self.x = 1
    """
    nodes = parseSource( src )
    cvtr = SelfConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """def func1():
    this.abc = 1
    this.callMeth()
    this.x = 1"""

