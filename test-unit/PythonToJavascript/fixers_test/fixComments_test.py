from utils import parseSource, nodesToString, dumpNodes, dumpTree

from fixers import fixComments

def test_fixComments_01():
    src = """
        # comment-1
        doOne()
        doTwo() # comment-2
    """
    nodes = parseSource( src )
    fixComments( nodes )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """// comment-1
doOne()
doTwo() // comment-2"""


def test_fixComments_02():
    src = '''
    def aFunc():
        """ single-line comment """
        doOne()
    '''
    nodes = parseSource( src )
    fixComments( nodes )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """def aFunc():
    /* single-line comment */
    doOne()"""


def test_fixComments_03():
    src = '''
    def aFunc():
        """ this is
            a multi-line
            comment """
        doOne()
    '''
    nodes = parseSource( src )
    fixComments( nodes )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """def aFunc():
    /* this is
        a multi-line
        comment */
    doOne()"""


