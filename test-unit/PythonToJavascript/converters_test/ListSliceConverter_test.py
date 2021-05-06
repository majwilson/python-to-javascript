from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import ListSliceConverter

def test_ListSliceGather_01():
    src = """
        alist[ start : finish ]
    """
    matches = ListSliceConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.start.toString() == 'start'
    assert match.colon.toString() == ':'
    assert match.finish.toString() == 'finish'

def test_ListSliceGather_02():
    src = """
        alist[ : finish ]
    """
    matches = ListSliceConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert "start" not in match
    assert match.colon.toString() == ':'
    assert match.finish.toString() == 'finish'

def test_ListSliceGather_03():
    src = """
        alist[ start : ]
    """
    matches = ListSliceConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert match.start.toString() == 'start'
    assert match.colon.toString() == ':'
    assert "finish" not in match

def test_ListSliceGather_04():
    src = """
        alist[ : ]
    """
    matches = ListSliceConverter().gather( parseSource( src ) )
    match = matches[ 0 ]
    assert "start" not in match
    assert match.colon.toString() == ':'
    assert "finish" not in match


def test_ListSliceProcess_01():
    src = """
        alist[ start : finish ]
    """
    nodes = parseSource( src )
    cvtr = ListSliceConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToString( nodes ) ==  """alist.slice( start, finish )"""

def test_ListSliceProcess_02():
    src = """
        alist[ 1 + 2 + 3 : f( x ) ]
    """
    nodes = parseSource( src )
    cvtr = ListSliceConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToString( nodes ) ==  """alist.slice( 1 + 2 + 3, f( x ) )"""

def test_ListSliceProcess_03():
    src = """
        alist[ : finish ]
    """
    nodes = parseSource( src )
    cvtr = ListSliceConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToString( nodes ) ==  """alist.slice( 0, finish )"""

def test_ListSliceProcess_04():
    src = """
        alist[ start : ]
    """
    nodes = parseSource( src )
    cvtr = ListSliceConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToString( nodes ) ==  """alist.slice( start )"""

def test_ListSliceProcess_05():
    src = """
        alist[ : ]
    """
    nodes = parseSource( src )
    cvtr = ListSliceConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    assert nodesToString( nodes ) ==  """alist.slice()"""
