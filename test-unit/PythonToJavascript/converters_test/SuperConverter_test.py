from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import SuperConverter

def test_SuperGather_01():
    src = """
        super( SPVEBorderColorMixed, self ).setupValue()
    """
    matches = SuperConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.super_args.toString() == '( SPVEBorderColorMixed, self )'
    assert match.super_method.toString() == '.setupValue'
    assert match.method_args.toString() == '()'


def test_SuperGather_02():
    src = """
        super( self ).setupValue()
    """
    matches = SuperConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.super_args.toString() == '( self )'
    assert match.super_method.toString() == '.setupValue'
    assert match.method_args.toString() == '()'


def test_SuperGather_03():
    src = """
        super().setupValue()
    """
    matches = SuperConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.super_args.toString() == '()'
    assert match.super_method.toString() == '.setupValue'
    assert match.method_args.toString() == '()'

def test_SuperGather_04():
    """ we had bug where super was not being recognised in a function definition,
        and another where it was not identified after 'return' """
    src = """
        def __init__( self, p1, p2, p3 ):
            self.doInitThing()
            return super( AClass, self ).__init__( p1, p2, p3 );
    """
    matches = SuperConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.super_args.toString() == '( AClass, self )'
    assert match.super_method.toString() == '.__init__'
    assert match.method_args.toString() == '( p1, p2, p3 )'


def test_SuperProcess_01():
    src = """
        super( SPVEBorderColorMixed, self ).setupValue()
    """
    nodes = parseSource( src )
    cvtr = SuperConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        'super.setupValue()',
    ]

def test_SuperProcess_02():
    src = """
        super( SPVEBorderColorMixed, self ).__init__( abc )
    """
    nodes = parseSource( src )
    cvtr = SuperConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        'super( abc )',
    ]

def test_SuperProcess_03():
    src = """
        def meth1( self, aval ):
            return super( ABaseClass, self ).meth1( aval )
    """
    nodes = parseSource( src )
    cvtr = SuperConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "def meth1( self, aval ):",
        "    return super.meth1( aval )",
    ]
