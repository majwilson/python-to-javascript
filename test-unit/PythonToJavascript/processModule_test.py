import adjust_sys_path

from utils import parseSource, nodesToString, dumpNodes, nodesToLines, dumpTree

from process import processModule, processFunction

# ==================================================================================================
def test_processModule_01():
    src = '''
        import abc
        from xyz import funcy

        def func1():
            x = 1
            return 123

        class AClass( object ):
            def __init__( self ):
                self.bim = funcy( 1 )
                self.bam = func1( self.bim )
            def meth1( self, p ):
                return self.meth2( p )
            def meth2( self, p ):
                return self.bim + self.bam + p

        class BClass( AClass ):
            """ doc string for BClass """
            def meth2( self, p ):
                r = super().meth2( p )
                return r + 1
    '''
    nodes = parseSource( src )

    infos = processModule( nodes )
    assert infos.class_names == [ "AClass", "BClass" ]
    assert infos.func_names == [ "func1" ]

    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "const abc = require( './abc' );",
        "const { funcy } = require( './xyz' );",
        "function func1() {",
        "    let x = 1;",
        "    return 123;",
        "}",
        "",
        " class AClass extends object {",
        "        constructor() {",      # <-- indent incorrect
        "        this.bim = funcy( 1 );",
        "        this.bam = func1( this.bim );",
        "    }",
        "    meth1( p ) {",
        "        return this.meth2( p );",
        "    }",
        "    meth2( p ) {",
        "        return this.bim + this.bam + p;",
        "    }",
        "",
        "}",
        " class BClass extends AClass {",
        "    /* doc string for BClass */",
        "    meth2( p ) {",             # <-- indent ok cos of doc string
        "        let r = super.meth2( p );",
        "        return r + 1;",
        "    }",
        "",
        "}",
    ]


def test_processModule_02():
    src = '''
        class AClass( PInfo ):
            """ docstring for class """
            def __init__( self, p1, p2, p3 ):
                super( AClass, self ).__init__( p1, p2, p3 );
                self.doInitThing()

            def setup( self ):
                """ docstring for setup """
                super( AClass, self ).setup( p1, p2, p3 );
                self.doSetupThing()

            def whatevs( self ):
                a = 1
                b = 2
    '''
    nodes = parseSource( src )

    # dumpTree( nodes )

    infos = processModule( nodes )
    assert infos.class_names == [ "AClass" ]
    assert infos.func_names == []

    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "class AClass extends PInfo {",
        "    /* docstring for class */",
        "    constructor( p1, p2, p3 ) {",
        "        super( p1, p2, p3 );",
        "        this.doInitThing();",
        "    }",
        "",
        "    setup() {",
        "        /* docstring for setup */",
        "        super.setup( p1, p2, p3 );",
        "        this.doSetupThing();",
        "    }",
        "",
        "    whatevs() {",
        "        let a = 1;",
        "        let b = 2;",
        "    }",
        "",
        "}",
    ]

