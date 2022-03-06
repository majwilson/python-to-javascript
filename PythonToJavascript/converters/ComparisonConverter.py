from Converter import Converter
from helpers import Treeverser, makeLeaf, getNodeIndex, getNodeKind, clearNode


class ComparisonConverter( Converter ):
    """
        x == y => x === y
        x != y => x !== y
        x is None => x === null
        x is not None => x !== null
        x is ... => _pyjs.isDef( x, y )
        x is y => Object.is( x, y )
        x is not y => !Object.is( x, y )
     """

    PATTERN = """
        comparison < left=any comp_op=('<'|'>'|'=='|'>='|'<='|'<>'|'!='|'in'|'is') right=any >
        |
        comparison < left=any comp_op=comp_op< ('not' 'in'|'is' 'not') > right=any >
    """

    def gather( self, node ):
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.PATTERN )
        for match in matches:
            match.comp_op = match.comp_op[ 0 ] if isinstance( match.comp_op, list ) else match.comp_op
        return matches

    def processOne( self, match ):
        comp_op_kind = getNodeKind( match.comp_op )
        if comp_op_kind == "EQEQUAL":
            match.comp_op.replace( makeLeaf( "PYJS", "===", match.comp_op.prefix ) )
        elif comp_op_kind == "NOTEQUAL":
            match.comp_op.replace( makeLeaf( "PYJS", "!==", match.comp_op.prefix ) )
        elif comp_op_kind == "NAME" and match.comp_op.toString() == "is":
            if match.right.toString() == "None":
                match.comp_op.replace( makeLeaf( "PYJS", "===", match.comp_op.prefix ) )
                match.right.replace( makeLeaf( "PYJS", "null", match.right.prefix ) )
            elif match.right.toString() == "...":
                clearNode( match.node )
                match.node.append_child( makeLeaf( "PYJS", "!_pyjs.isDef", match.comp_op.prefix ) )
                match.node.append_child( makeLeaf( "LPAR", "(" ) )
                match.left.prefix = " "
                match.node.append_child( match.left )
                match.node.append_child( makeLeaf( "RPAR", ")", " " ) )
            else:
                clearNode( match.node )
                match.node.append_child( makeLeaf( "PYJS", "Object.is", match.comp_op.prefix ) )
                match.node.append_child( makeLeaf( "LPAR", "(" ) )
                match.left.prefix = " "
                match.node.append_child( match.left )
                match.node.append_child( makeLeaf( "COMMA", ",", "" ) )
                match.right.prefix = " "
                match.node.append_child( match.right.clone() )
                match.node.append_child( makeLeaf( "RPAR", ")", " " ) )
        elif comp_op_kind == "comp_op" and match.comp_op.toString() == "not in":
                clearNode( match.node )
                match.node.append_child( makeLeaf( "PYJS", "!" ) )
                match.node.append_child( makeLeaf( "LPAR", "(" ) )
                match.node.append_child( match.left.clone() )
                match.node.append_child( makeLeaf( "PYJS", " in " ) )
                match.node.append_child( match.right.clone() )
                match.node.append_child( makeLeaf( "RPAR", ")", " " ) )

        elif comp_op_kind == "comp_op" and match.comp_op.toString() == "is not":
            if match.right.toString() == "None":
                match.comp_op.replace( makeLeaf( "PYJS", "!==", match.comp_op.prefix ) )
                match.right.replace( makeLeaf( "PYJS", "null", match.right.prefix ) )
            elif match.right.toString() == "...":
                clearNode( match.node )
                match.node.append_child( makeLeaf( "PYJS", "_pyjs.isDef", match.comp_op.prefix ) )
                match.node.append_child( makeLeaf( "LPAR", "(" ) )
                match.left.prefix = " "
                match.node.append_child( match.left )
                match.node.append_child( makeLeaf( "RPAR", ")", " " ) )
            else:
                clearNode( match.node )
                match.node.append_child( makeLeaf( "PYJS", "!Object.is", match.comp_op.prefix ) )
                match.node.append_child( makeLeaf( "LPAR", "(" ) )
                match.left.prefix = " "
                match.node.append_child( match.left )
                match.node.append_child( makeLeaf( "COMMA", ",", "" ) )
                match.right.prefix = " "
                match.node.append_child( match.right.clone() )
                match.node.append_child( makeLeaf( "RPAR", ")", " " ) )
