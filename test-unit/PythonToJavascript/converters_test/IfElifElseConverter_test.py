from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import IfElifElseConverter

def test_IfElifElseGather_01():
    src = """
    if x:
        doThis()
    """
    matches = IfElifElseConverter().gather( parseSource( src ) )
    if_clause = matches[ 0 ].if_clause
    assert if_clause.if_word.toString() == "if"
    assert if_clause.if_test[ 0 ].toString() == "x"
    assert if_clause.if_colon.toString() == ":"
    assert if_clause.if_suite.toString() == 'doThis()'


def test_IfElifElseGather_02():
    src = """
    if x:
        doThis()
    else:
        doThat()
    """
    matches = IfElifElseConverter().gather( parseSource( src ) )
    else_clause = matches[ 0 ].else_clause
    assert else_clause.else_word.value == "else"
    assert else_clause.else_colon.value == ":"
    assert else_clause.else_suite.toString() == 'doThat()'


def test_IfElifElseGather_03():
    src = """
    if x:
        doThis()
    elif y:
        doY()
    elif z > 1234 and bam - 4 == 100:
        doZ()
    else:
        doThat()
    """
    matches = IfElifElseConverter().gather( parseSource( src ) )
    elif_clause = matches[ 0 ].elif_clauses[ 0 ]
    assert elif_clause.elif_word.toString() == "elif"
    assert elif_clause.elif_test.toString() == "y"
    assert elif_clause.elif_colon.toString() == ":"
    assert elif_clause.elif_suite.toString() == 'doY()'

    elif_clause = matches[ 0 ].elif_clauses[ 1 ]
    assert elif_clause.elif_word.toString() == "elif"
    assert elif_clause.elif_test.toString() == "z > 1234 and bam - 4 == 100"
    assert elif_clause.elif_colon.toString() == ":"
    assert elif_clause.elif_suite.toString() == 'doZ()'



def test_IfElifElseProcess_01():
    src = """
        if x:
            doThis()
    """
    nodes = parseSource( src )
    cvtr = IfElifElseConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """if( x ) {
    doThis()
}"""

def test_IfElifElseProcess_02():
    src = """
        if x:
            doThis()
        else:
            doThat()
    """
    nodes = parseSource( src )
    cvtr = IfElifElseConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """if( x ) {
    doThis()
} else {
    doThat()
}"""

def test_IfElifElseProcess_03():
    src = """
        if x:
            doThis()
        elif y:
            doElif1()
        else:
            doThat()
    """
    nodes = parseSource( src )
    cvtr = IfElifElseConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """if( x ) {
    doThis()
} else if( y ) {
    doElif1()
} else {
    doThat()
}"""

def test_IfElifElseProcess_04():
    src = """
        if x:
            doThis()
            if y:
                doBem()
    """
    nodes = parseSource( src )
    cvtr = IfElifElseConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """if( x ) {
    doThis()
    if( y ) {
        doBem()
    }
}"""


def test_IfElifElseProcess_05():
    src = """
        if x:
            doThis()
            if y:
                doBem()
                if z:
                    doBom()
                else:
                    doBam()"""
    nodes = parseSource( src )
    cvtr = IfElifElseConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """if( x ) {
    doThis()
    if( y ) {
        doBem()
        if( z ) {
            doBom()
        } else {
            doBam()
        }

    }
}"""


def test_IfElifElseProcess_06():
    src = """
        def bam( x ):
            doThis()
            if y:
                doBem()
                if z:
                    doBom()
                else:
                    doBam()"""
    nodes = parseSource( src )
    cvtr = IfElifElseConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """def bam( x ):
    doThis()
    if( y ) {
        doBem()
        if( z ) {
            doBom()
        } else {
            doBam()
        }

    }"""

def test_IfElifElseProcess_07():
    src = """
        # -------
        if x:
            doThis()
        else:
            doThat()
    """
    nodes = parseSource( src )
    cvtr = IfElifElseConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """# -------
if( x ) {
    doThis()
} else {
    doThat()
}"""

