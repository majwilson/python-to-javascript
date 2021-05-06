import adjust_sys_path

from utils import parseSource, nodesToString, dumpNodes, nodesToLines

from process import processModule, processFunction
from converters import FunctionConverter, StringInterpolationConverter


# ==================================================================================================
def test_processFunction_01():
    src = """
        def func1():
            x = 1
            return 123
    """
    nodes = parseSource( src )
    matches = FunctionConverter().gather( nodes )

    processFunction( matches[ 0 ].node )

    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "function func1() {",
        "    let x = 1;",
        "    return 123;",
        "}",
    ]

def test_processFunction_02():
    src = '''
    def addTagOpener( self, opener ):
        """ opener can be the first part of a tag ("<html_tag") or a complete tag up
                to the closing ">" """
        if self.tag_closer:
            try:
                self.lines[ -1 ] += opener
            except IndexError:
                self.addLine( opener )
    '''
    nodes = parseSource( src )
    matches = FunctionConverter().gather( nodes )

    processFunction( matches[ 0 ].node )

    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "function addTagOpener( opener ) {",
        "    /* opener can be the first part of a tag (\"<html_tag\") or a complete tag up",
        "            to the closing \">\" */",
        "    if( this.tag_closer ) {",
        "        try {",
        "            this.lines[ -1 ] += opener;",
        "        } catch( e ) /* IndexError */ {",
        "            this.addLine( opener );",
        "        }",
        "",
        "    }",
        "}",
    ]

def test_processFunction_03():
    src = '''
        def trimEndChars( self, num_chars ):
            """ nessary in occasionally to allow addTagCloser() to be used after the
                    an open tag has been fully output  """
            if num_chars > len( self.lines[ -1 ] ):
                raise Exception( "attempt to trim too many end chars" )
            self.lines[ -1 ] = self.lines[ -1 ][ : - num_chars ]

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # these enable us to "backtrack" if an error occurs
         # bim
          # bam
        def getLinesNIndent( self ):
            return len( self.lines ), self.indent_lvl
    '''
    nodes = parseSource( src )
    matches = FunctionConverter().gather( nodes )

    processFunction( matches[ 0 ].node )
    processFunction( matches[ 1 ].node )

    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "function trimEndChars( num_chars ) {",
        "    /* nessary in occasionally to allow addTagCloser() to be used after the",
        "            an open tag has been fully output  */",
        "    if( num_chars > len( this.lines[ -1 ] ) ) {",
        "        throw new Error( \'Exception\', \"attempt to trim too many end chars\" );",
        "    }",
        "    this.lines[ -1 ] = this.lines[ -1 ].slice( 0, - num_chars );",
        "}",
        "",
        "// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -",
        "// these enable us to \"backtrack\" if an error occurs",
        " // bim",
        "  // bam",
        "function getLinesNIndent() {",
        "    return len( this.lines ), this.indent_lvl;",
        "}",
    ]


def test_processFunction_04():
    src = '''
class StringBuff( object ):
    """ test """
    def numLines( self ):
        return len( self.lines )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def addLine( self, line ):
        """ add a new line to the output """
        self.lines.append( self.indent_act + self.tag_closer + line )
        self.tag_closer = ""
    '''
    nodes = parseSource( src )
    matches = FunctionConverter().gather( nodes )

    processFunction( matches[ 0 ].node )
    processFunction( matches[ 1 ].node )

    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "class StringBuff( object ):",
        "    \"\"\" test \"\"\"",
        "    function numLines() {",
        "        return len( this.lines );",
        "    }",
        "",
        "    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -",
        "    function addLine( line ) {",
        "        /* add a new line to the output */",
        "        this.lines.push( this.indent_act + this.tag_closer + line );",
        "        this.tag_closer = \"\";",
        "    }",
    ]


def test_processFunction_05():
    src = '''
    def dedent( self, dedent ):
        x = dedent
    '''
    nodes = parseSource( src )
    matches = FunctionConverter().gather( nodes )

    processFunction( matches[ 0 ].node )

    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "function dedent( dedent ) {",
        "    let x = dedent;",
        "}",
    ]

def test_processFunction_06():
    src = '''
    def dedent( self ):
        x = 1
    '''
    nodes = parseSource( src )
    matches = FunctionConverter().gather( nodes )

    processFunction( matches[ 0 ].node )

    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "function dedent() {",
        "    let x = 1;",
        "}",
    ]


def test_processFunction_07():
    src = '''
    def dedent( self ):
        bam()
    '''
    nodes = parseSource( src )
    matches = FunctionConverter().gather( nodes )

    processFunction( matches[ 0 ].node )

    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "function dedent() {",
        "    bam();",
        "}",
    ]


def test_processFunction_08():
    src = '''
    def dictComp( self ):
        return { key: val for ( k, v ) in self.getDictItems() }
    '''
    nodes = parseSource( src )
    matches = FunctionConverter().gather( nodes )

    processFunction( matches[ 0 ].node )

    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "function dictComp() {",
        "    return this.getDictItems().reduce( ( __map, [ [ k, v ] ] ) => ( { ...__map, [ key ]: val } ), {} );",
        "}",
    ]

def test_processFunction_09():
    src = '''
    def stringInterp( self ):
        return "hello %s world %s" % ( self.a, self.b )
    '''
    nodes = parseSource( src )
    matches = FunctionConverter().gather( nodes )

    processFunction( matches[ 0 ].node )

    # dumpTree( nodes )
    # dumpNodes( nodes )
    if StringInterpolationConverter.USE_PYJS:
        assert nodesToLines( nodes ) == [
            "function stringInterp() {",
            "    return _pyjs.stringInterpolate( \"hello %s world %s\", [ this.a, this.b ] );",
            "}",
        ]
    else:
        assert nodesToLines( nodes ) == [
            "function stringInterp() {",
            "    return [ this.a, this.b ].reduce( ( a, c ) => a.replace( /%(s|i|r)?/, c.toString () ), \"hello %s world %s\" );",
            "}",
        ]

def test_processFunction_10():
    src = '''
    def listSlice( self ):
        return m_listy[ 123 : bam ]
    '''
    nodes = parseSource( src )
    matches = FunctionConverter().gather( nodes )

    processFunction( matches[ 0 ].node )

    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "function listSlice() {",
        "    return m_listy.slice( 123, bam );",
        "}",
    ]

def test_processFunction_11():
    src = '''
    def raiseExc( self ):
        if self.p > 123:
            raise SomeError( "this is a mistake" )
    '''
    nodes = parseSource( src )
    matches = FunctionConverter().gather( nodes )

    processFunction( matches[ 0 ].node )

    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "function raiseExc() {",
        "    if( this.p > 123 ) {",
        "        throw new Error( 'SomeError', \"this is a mistake\" );",
        "    }",
        "}",
    ]

def test_processFunction_12():
    src = '''
    def kwArgs( self ):
        self.style_enable_check.setJSCommandVals(
                        style_path=style_sel.path,
                        style_name=style_sel.name,
                        enable="__value__" )

    '''
    nodes = parseSource( src )
    matches = FunctionConverter().gather( nodes )

    processFunction( matches[ 0 ].node )

    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "function kwArgs() {",
        "    this.style_enable_check.setJSCommandVals( {",
        "                    style_path: style_sel.path,",
        "                    style_name: style_sel.name,",
        "                    enable: \"__value__\" } );",
        "}",
    ]

