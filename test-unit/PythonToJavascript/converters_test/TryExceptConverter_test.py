from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import TryExceptConverter
from fixers import fixIndents


def test_TryExceptGather_01():
    src = """
        try:
            bim()
        except IndexError:
            bam()
            raise
    """
    matches = TryExceptConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.try_word.toString() == 'try'
    assert match.try_colon.toString() == ':'
    assert match.try_suite.toString() == 'bim()'

    assert match.exc_word.toString() == 'except'
    assert match.exc_what.toString() == 'IndexError'
    assert match.exc_colon.toString() == ':'
    assert match.exc_suite.toString() == "bam()\n    raise"


def test_TryExceptGather_02():
    src = """
        try:
            bim()
        except ( IndexError, KeyError ):
            bam()
            raise
    """
    matches = TryExceptConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.try_word.toString() == 'try'
    assert match.try_colon.toString() == ':'
    assert match.try_suite.toString() == 'bim()'

    assert match.exc_word.toString() == 'except'
    assert match.exc_what.toString() == '( IndexError, KeyError )'
    assert match.exc_colon.toString() == ':'
    assert match.exc_suite.toString() == "bam()\n    raise"


def test_TryExceptGather_03():
    src = """
        try:
            bim()
        except ( IndexError, KeyError ) as exy:
            bam()
        finally:
            bom()
    """
    matches = TryExceptConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.try_word.toString() == 'try'
    assert match.try_colon.toString() == ':'
    assert match.try_suite.toString() == 'bim()'

    assert match.exc_word.toString() == 'except'
    assert match.exc_what.toString() == '( IndexError, KeyError )'
    assert match.exc_as.toString() == "as"
    assert match.exc_as_name.toString() == "exy"
    assert match.exc_colon.toString() == ':'
    assert match.exc_suite.toString() == "bam()"


    assert match.fin_word.toString() == 'finally'
    assert match.fin_colon.toString() == ':'
    assert match.fin_suite.toString() == 'bom()'


def test_TryExceptGather_04():
    src = """
        try:
            getattr( obj, 'bom' )
        except:
            pass
    """
    matches = TryExceptConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.try_word.toString() == 'try'
    assert match.try_colon.toString() == ':'
    assert match.try_suite.toString() == "getattr( obj, 'bom' )"

    assert match.exc_word.toString() == 'except'
    assert "exc_what" not in match
    assert match.exc_colon.toString() == ':'
    assert match.exc_suite.toString() == "pass"



def test_TryExceptProcess_01():
    src = """
        try:
            bim()
        except ( IndexError, KeyError ):
            bam()
        return 123
    """
    nodes = parseSource( src )
    cvtr = TryExceptConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "try {",
        "    bim()",
        "} catch( e ) /* ( IndexError, KeyError ) */ {",
        "    bam()",
        "}",
        "return 123",
    ]

def test_TryExceptProcess_02():
    src = """
        try:
            bim()
        except ( IndexError, KeyError ):
            bam()
            raise
        finally:
            bom()
        return 123
    """
    nodes = parseSource( src )
    cvtr = TryExceptConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "try {",
        "    bim()",
        "} catch( e ) /* ( IndexError, KeyError ) */ {",
        "    bam()",
        "    raise",
        "} finally {",
        "    bom()",
        "}",
        "return 123",
    ]

def test_TryExceptProcess_03():
    src = """
        try:
            getattr( obj, 'bom' )
        except:
            pass
    """
    nodes = parseSource( src )
    cvtr = TryExceptConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "try {",
        "    getattr( obj, 'bom' )",
        "} catch( e ) {",
        "    pass",
        "}",
    ]

def test_TryExceptProcess_04():
    src = """
if 1:
    if 1:
        if 1:
            try:
                bim()
            except IndexError as exy:
                bam()
                raise
    """
    nodes = parseSource( src )
    fixIndents( nodes )
    cvtr = TryExceptConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "if 1:",
        "    if 1:",
        "        if 1:",
        "            try {",
        "                bim()",
        "            } catch( exy ) /* IndexError */ {",
        "                bam()",
        "                raise",
        "            }",
    ]
