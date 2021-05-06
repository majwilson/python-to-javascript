from utils import parseSource, nodesToLines, dumpNodes, dumpTree

from fixers import fixSimpleRenames

def test_fixSimpleRenames_01():
    src = '''
        x = None
        y = True
        z = False
        f = a.startswith( 'a' )
        g = b.endswith( 'b' )
        c.append( d )
        def __init__( self ): pass
        def __repr__( self ): return 'hhh'
        raise e
        del abc
        if hasattr( x, 'bam' ): pass
        y = getattr( x, 'bam', None )
        setattr( a, b, c )
        print( "bim bam bom" )
    '''
    nodes = parseSource( src )

    fixSimpleRenames( nodes )

    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "x = null",
        "y = true",
        "z = false",
        "f = a.startsWith( 'a' )",
        "g = b.endsWith( 'b' )",
        "c.push( d )",
        "def constructor( self ): pass",
        "def toString( self ): return 'hhh'",
        "throw e",
        "delete abc",
        "if _pyjs.hasAttr( x, 'bam' ): pass",
        "y = _pyjs.getAttr( x, 'bam', null )",
        "_pyjs.setAttr( a, b, c )",
        'console.log( "bim bam bom" )',
    ]

def test_fixSimpleRenames_02():
    src = '''
        isinstance( a, AClass )
        zip( a, b )

    '''
    nodes = parseSource( src )

    fixSimpleRenames( nodes )

    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        '_pyjs.isInstance( a, AClass )',
        '_pyjs.listZip( a, b )'
    ]
