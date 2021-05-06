from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import ClassConverter

def test_ClassGather_01():
    src = """
        class Bango:
            def __init__( self ): pass
    """
    matches = ClassConverter().gather( parseSource( src ) )
    class_clause = matches[ 0 ]
    assert class_clause.name.toString() == 'Bango'
    assert class_clause.colon.toString() == ':'
    assert class_clause.suite.toString() == 'def __init__( self ): pass'

def test_ClassGather_02():
    src = """
        class Bango( Bingo, Bungo ):
            def __init__( self ): pass
    """
    matches = ClassConverter().gather( parseSource( src ) )
    class_clause = matches[ 0 ]
    assert class_clause.name.toString() == 'Bango'
    params_strs = [ str( p ) for p in class_clause.params ]
    assert str( "".join( params_strs ) ).strip() == '( Bingo, Bungo )'
    assert class_clause.args.toString() == 'Bingo, Bungo'
    assert class_clause.colon.toString() == ':'
    assert class_clause.suite.toString() == 'def __init__( self ): pass'


def test_ClassProcess_01():
    src = """
        class Bango:
            def __init__( self ): pass
    """
    nodes = parseSource( src )
    cvtr = ClassConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpLines( nodesToString( nodes ) )
    assert nodesToLines( nodes ) == [
        'class Bango {',
        '    def __init__( self ): pass',
        '}',
    ]


def test_ClassProcess_02():
    src = """
        class Bango( Bingo ):
            def __init__( self ): pass
    """
    nodes = parseSource( src )
    cvtr = ClassConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpLines( nodesToString( nodes ) )
    assert nodesToLines( nodes ) == [
         'class Bango extends Bingo {',
        '    def __init__( self ): pass',
        '}',
    ]