from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree
from converters import FunctionConverter

def test_FunctionGather_01():
    src = """
        def func1():
            return 123
    """
    matches = FunctionConverter().gather( parseSource( src ) )
    func_clause = matches[ 0 ]
    assert func_clause.name.toString() == 'func1'
    assert func_clause.params.toString() == '()'
    # assert func_clause.args.toString() == '1'
    assert func_clause.colon.toString() == ':'
    assert func_clause.suite.toString() == 'return 123'
    # assert func_clause.rest.toString() == ':'


def test_FunctionGather_02():
    src = """
        def func1( a, b, c ):
            if a == 1:
                return 123
    """
    matches = FunctionConverter().gather( parseSource( src ) )
    func_clause = matches[ 0 ]
    assert func_clause.name.toString() == 'func1'
    assert func_clause.params.toString() == '( a, b, c )'
    assert func_clause.args.toString() == 'a, b, c'


def test_FunctionProcess_01():
    src = """
        def func1():
            return 123
    """
    nodes = parseSource( src )
    cvtr = FunctionConverter()
    matches = cvtr.gather( nodes )
    cvtr.processAll( matches )
    # dumpTree( nodes )
    # dumpNodes( nodes )
    assert nodesToString( nodes ) == """function func1() {
    return 123
}"""