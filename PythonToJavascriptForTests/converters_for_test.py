from PythonToJavascript.converters import ClassConverter, FunctionConverter
from PythonToJavascript.Converter import Converter

from helpers import Treeverser, makeLeaf, makeStatement, findOutNode, getNodeKind


# ==================================================================================================
class UnittestClassToMochaDescribeConverter( ClassConverter ):
    """ rewrites class declaration into mocha style

            class Tests( unittest.TestCase ):
                ...

            =>

            describe( 'tests', () => {
              ...
            } );

        NB this converts non-test classes as normal
    """

    def __init__( self, test_superclass_strings ):
        super( UnittestClassToMochaDescribeConverter, self ).__init__()
        if not isinstance( test_superclass_strings, list ):
            test_superclass_strings = test_superclass_strings.split()
        self.test_superclass_strings = test_superclass_strings


    def processOne( self, class_info ):
        if not ( 'args' in class_info and class_info.args.toString() in self.test_superclass_strings ):
            super( UnittestClassToMochaDescribeConverter, self ).processOne( class_info )
            return

        class_name = class_info.name.toString()
        class_indent= self.calcIndent( class_info.node )

        parent = class_info.class_word.parent
        new = makeStatement()
        new.append_child( makeLeaf( "PYJS", "describe", '' ) )
        new.append_child( makeLeaf( "LPAR", "(", '' ) )
        new.append_child( makeLeaf( "STRING", f"'{ class_name }'", ' ' ) )
        new.append_child( makeLeaf( "COMMA", ",", '' ) )
        new.append_child( makeLeaf( "LPAR", "(", ' ' ) )
        new.append_child( makeLeaf( "RPAR", ")", '' ) )
        new.append_child( makeLeaf( "PYJS", "=>", ' ' ) )
        new.append_child( makeLeaf( "LBRACE", "{", ' ' ) )
        new.append_child( class_info.suite )
        new.append_child( makeLeaf( "DEDENT", "", class_indent ) )

        new.append_child( makeLeaf( "RBRACE", "}", '' ) )
        new.append_child( makeLeaf( "RPAR", ")", ' ' ) )
        new.append_child( makeLeaf( "SEMI", ";", '' ) )
        new.append_child( makeLeaf( "NEWLINE", "\n", '' ) )
        new.append_child( makeLeaf( "DEDENT", "", class_indent ) )

        parent.replace( new )


# ==================================================================================================
class PytestMethodToMochaItConverter( FunctionConverter ):
    """ rewrites test function body into mocha style

            def test_ListComprehension_01( self ):
                ...

            it( 'dictComprehension_01', () => {
              ...
            } );

        NB this converts non-test methods as normal
    """

    def processOne( self, func_info ):
        func_name = func_info.name.toString()
        if not func_name.startswith( 'test_' ):
            super( PytestMethodToMochaItConverter, self ).processOne( func_info )
            return

        func_indent= self.calcIndent( func_info.node )

        parent = func_info.def_word.parent
        new = makeStatement()
        new.append_child( makeLeaf( "PYJS", "it", '' ) )
        new.append_child( makeLeaf( "LPAR", "(", '' ) )
        new.append_child( makeLeaf( "STRING", f"'{ func_name }'", ' ' ) )
        new.append_child( makeLeaf( "COMMA", ",", '' ) )
        new.append_child( makeLeaf( "LPAR", "(", ' ' ) )
        new.append_child( makeLeaf( "RPAR", ")", '' ) )
        new.append_child( makeLeaf( "PYJS", "=>", ' ' ) )
        new.append_child( makeLeaf( "LBRACE", "{", ' ' ) )
        new.append_child( func_info.suite )
        new.append_child( makeLeaf( "DEDENT", "", func_indent ) )

        new.append_child( makeLeaf( "RBRACE", "}", '' ) )
        new.append_child( makeLeaf( "RPAR", ")", ' ' ) )
        new.append_child( makeLeaf( "SEMI", ";", '' ) )
        new.append_child( makeLeaf( "NEWLINE", "\n", '' ) )
        new.append_child( makeLeaf( "DEDENT", "", func_indent ) )

        parent.replace( new )


# ==================================================================================================
class AssertToChaiExpectConverter( Converter ):
    """ rewrites assert statement body into chai expect style

            assert aval == 'bom'
            assert aval
            assert aval > 100
            =>
            expect( aval ).to.eql( 'bom' )
            expect( aval ).to.be.ok
            expect( aval > 100 ).to.be.ok

        NB only converts assert statements that appear in function whose name starts
            'test_'
        NB per the above, this conversion should be run before the enclosing functions
            are converted
    """

    PATTERN = """
        assert_stmt< assert_word='assert' (
            comp=comparison< left=any comp_op=('<'|'>'|'=='|'>='|'<='|'<>'|'!='|'in'|'is') right=any >
            |
            not_test< not_word='not' truthy=any >
            |
            truthy=any
        ) >
    """

    def gather( self, node ):
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.PATTERN )
        matches = [ m for m in matches if findOutNode( m.node, self.isTestFuncNode, None ) ]
        for match in matches:
            if 'comp_op' in match:
                match.comp_op = match.comp_op[ 0 ]
        return matches

    def isTestFuncNode( self, node ):
        return getNodeKind( node ) == 'funcdef' and node.toString().startswith( 'def test_' )

    def processOne( self, match ):
        parent = match.assert_word.parent
        new = makeStatement()
        new.append_child( makeLeaf( "PYJS", "expect", match.assert_word.prefix ) )
        new.append_child( makeLeaf( "LPAR", "(", '' ) )
        if 'comp' in match:
            if match.comp_op.toString() in [ "==", "!=" ]:
                new.append_child( match.left )
            else:
                new.append_child( match.comp )
        else:
            new.append_child( match.truthy )
        new.append_child( makeLeaf( "RPAR", ")", ' ' ) )
        new.append_child( makeLeaf( "DOT", ".", '' ) )
        if ( 'comp' in match and match.comp_op.toString() == "!=" ) or "not_word" in match:
            new.append_child( makeLeaf( "PYJS", "not", '' ) )
            new.append_child( makeLeaf( "DOT", ".", '' ) )
        new.append_child( makeLeaf( "PYJS", "to", '' ) )
        new.append_child( makeLeaf( "DOT", ".", '' ) )
        if 'comp' in match and match.comp_op.toString() in [ "==", "!=" ]:
            new.append_child( makeLeaf( "PYJS", "eql", '' ) )
            new.append_child( makeLeaf( "LPAR", "(", '' ) )
            new.append_child( match.right )
            new.append_child( makeLeaf( "RPAR", ")", ' ' ) )
        else:
            new.append_child( makeLeaf( "PYJS", "be", '' ) )
            new.append_child( makeLeaf( "DOT", ".", '' ) )
            new.append_child( makeLeaf( "PYJS", "ok", '' ) )
        parent.replace( new )


