from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import ImportFromConverter

def test_ImportFromGather_01():
    src = """
        from xyz import funcy
    """
    matches = ImportFromConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.from_word.toString() == 'from'
    assert match.module.toString() == 'xyz'
    assert match.import_word.toString() == 'import'
    assert match.imported.toString() == 'funcy'

def test_ImportFromGather_02():
    src = """
        from amodule import athing, bthing
    """
    matches = ImportFromConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.from_word.toString() == 'from'
    assert match.module.toString() == 'amodule'
    assert match.import_word.toString() == 'import'
    assert match.imported.toString() == 'athing, bthing'

def test_ImportFromGather_03():
    src = """
        from Utils import ( OrderedDict, stripTags, elideString,
                    crackString, padelide, escapeHtml,
                    splitCamelCase, deQuote )
    """
    matches = ImportFromConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.from_word.toString() == 'from'
    assert match.module.toString() == 'Utils'
    assert match.import_word.toString() == 'import'
    assert match.imported.toString() == """OrderedDict, stripTags, elideString,
            crackString, padelide, escapeHtml,
            splitCamelCase, deQuote"""


def test_ImportFromProcess_01():
    src = """
        from xyz import funcy
    """
    nodes = parseSource( src )
    cvtr = ImportFromConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToString( nodes ) == """const { funcy } = require( './xyz' )"""

def test_ImportFromProcess_02():
    src = """
        from amodule import athing, bthing
    """
    nodes = parseSource( src )
    cvtr = ImportFromConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToString( nodes ) == """const { athing, bthing } = require( './amodule' )"""

def test_ImportFromProcess_03():
    src = """
        from Utils import ( OrderedDict, stripTags, elideString,
                    crackString, padelide, escapeHtml,
                    splitCamelCase, deQuote )
    """
    nodes = parseSource( src )
    cvtr = ImportFromConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    strs = nodesToLines( nodes )
    # dumpLines( strs )
    assert strs == [
        "const { OrderedDict, stripTags, elideString,",
        "            crackString, padelide, escapeHtml,",
        "            splitCamelCase, deQuote } = require( './Utils' )",
    ]