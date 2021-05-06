from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import ImportNameConverter

def test_ImportNameGather_01():
    src = """
        import amodule
    """
    matches = ImportNameConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.import_word.toString() == 'import'
    assert nodesToString( match.imported ) == 'amodule'

def test_ImportNameGather_02():
    src = """
        import amodule, bmodule, cmodule
    """
    matches = ImportNameConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.import_word.toString() == 'import'
    assert nodesToString( match.imported ) == 'amodule, bmodule, cmodule'
    assert "as_word" not in match

def test_ImportNameGather_03():
    src = """
        import core.pscript.PCoreWidget as PCoreWidget
    """
    matches = ImportNameConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert nodesToString( match.import_word ) == 'import'
    assert nodesToString( match.imported ) == 'core.pscript.PCoreWidget'
    assert "as_word" in match
    assert nodesToString( match.as_word ) == 'as'
    assert nodesToString( match.as_name ) == 'PCoreWidget'

def test_ImportNameProcess_01():
    src = """
        import amodule
    """
    nodes = parseSource( src )
    cvtr = ImportNameConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToLines( nodes )[ 0 ] == """const amodule = require( './amodule' )"""

def test_ImportNameProcess_02():
    src = """
        import amodule, bmodule, cmodule
    """
    nodes = parseSource( src )
    cvtr = ImportNameConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToString( nodes ) == """const amodule = require( './amodule' )
const bmodule = require( './bmodule' )
const cmodule = require( './cmodule' )"""

def test_ImportNameProcess_03():
    src = """
        import core.pscript.PCoreWidget as PCoreWidget
    """
    nodes = parseSource( src )
    cvtr = ImportNameConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """const PCoreWidget = require( './core/pscript/PCoreWidget' )"""

