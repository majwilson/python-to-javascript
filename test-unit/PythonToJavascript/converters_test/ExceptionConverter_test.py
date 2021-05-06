from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import ExceptionConverter

def test_ExceptionGather_01():
    src = """
        raise NameError
    """
    matches = ExceptionConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.raise_word.toString() == 'raise'
    assert match.exc_name.toString() == 'NameError'
    assert "args" not in match

def test_ExceptionGather_02():
    src = """
        raise NameError( "bimbambom" )
    """
    matches = ExceptionConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.raise_word.toString() == 'raise'
    assert match.exc_name.toString() == 'NameError'
    assert match.args.toString() == '"bimbambom"'

def test_ExceptionProcess_01():
    src = """
        raise NameError
    """
    nodes = parseSource( src )
    cvtr = ExceptionConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToString( nodes ) ==  """throw new Error( 'NameError' )"""

def test_ExceptionProcess_02():
    src = """
        raise NameError( "bimbambom" )
    """
    nodes = parseSource( src )
    cvtr = ExceptionConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToString( nodes ) ==  """throw new Error( 'NameError', "bimbambom" )"""

def test_ExceptionProcess_03():
    src = """
        raise CustomError( 1, [ 'a', 'b', 'c' ], 'hello' )
    """
    nodes = parseSource( src )
    cvtr = ExceptionConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToString( nodes ) ==  \
                        """throw new Error( 'CustomError', 1, [ 'a', 'b', 'c' ], 'hello' )"""

