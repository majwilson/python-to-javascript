from utils import parseSource, nodesToLines, dumpNodes, dumpTree

from fixers import fixSemicolons

def test_fixSemicolons_01():
    src = """
        x = 1
        callFunc()
        y = callFunc()
        a, b, c = \
            1, 2, 3
    """
    nodes = parseSource( src )
    fixSemicolons( nodes )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "x = 1;",
        "callFunc();",
        "y = callFunc();",
        "a, b, c =             1, 2, 3;",
    ]

def test_fixSemicolons_02():
    """ don't put semicolons after comments """
    src = '''
    def afunc():
        """ this
            is
            a
            comment """
        doStuff()
        x = "this is not a comment"
        'but this is'
    '''
    nodes = parseSource( src )
    fixSemicolons( nodes )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToLines( nodes ) == [
        "def afunc():",
        '    """ this',
        "        is",
        "        a",
        '        comment """',
        "    doStuff();",
        "    x = \"this is not a comment\";",
        "    'but this is'",
    ]