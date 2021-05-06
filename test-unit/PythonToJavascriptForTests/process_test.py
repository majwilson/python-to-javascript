import adjust_sys_path

from PythonToJavascriptForTests.process_for_test import processTestModule

from utils import parseSource, nodesToString, dumpNodes, nodesToLines, dumpTree

# ==================================================================================================
def test_processModule_01():
    src = """
        class Tests( unittest.TestCase ):
            def test_func1( self ):
                assert aval == 'bim'
            def test_func2( self ):
                someStuff()
                assert afunc()
            def notATestFunc( self ):
                assert whatever == 'bam'
        class OtherClass( OtherBase ):
            pass
        class YetAnotherClass:
            pass
    """
    nodes = parseSource( src )

    infos = processTestModule( nodes )

    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "describe( 'Tests', () => {",
        "    it( 'test_func1', () => {",
        "        expect( aval ).to.eql( 'bim' );",
        "    } );",
        "    it( 'test_func2', () => {",
        "        someStuff();",
        "        expect( afunc() ).to.be.ok;",
        "    } );",
        "        notATestFunc() {",
        "        assert whatever === 'bam';",
        "    }",
        "} );",
        " class OtherClass extends OtherBase {",
        "    /* pass */",
        "}",
        " class YetAnotherClass {",
        "    /* pass */",
        "}",
    ]

def test_processModule_02():
    src = """
        class Tests( unittest.TestCase ):
            def test_getAttr( self ):
                try:
                    getattr( obj, 'bom' )
                except:
                    excepted = True
                assert excepted    """
    nodes = parseSource( src )
    infos = processTestModule( nodes )

    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "describe( 'Tests', () => {",
        "    it( 'test_getAttr', () => {",
        "        try {",
        "            _pyjs.getAttr( obj, 'bom' );",
        "        } catch( e ) {",
        "            let excepted = true;",
        "        }",
        "expect(        excepted ).to.be.ok;",
        "",
        "    } );",
        "    } );",
    ]
