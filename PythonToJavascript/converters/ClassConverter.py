from Converter import Converter
from helpers import Treeverser, makeLeaf, getNodeIndex


class ClassConverter( Converter ):

    CLASS_PATTERN = """
        classdef< class_word='class' name=NAME params=( '(' args=any* ')' )* colon=':' suite=any* >
    """

    def gather( self, node ):
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.CLASS_PATTERN )
        for match in matches:
            if match.get( "args", None ):
                match.args = match.args[ 0 ]
            match.suite = match.suite[ 0 ]
        return matches

    def processOne( self, match ):
        match.class_word.replace( makeLeaf( "PYJS", "class", " " ) )
        if "args" in match:
            par_node = self.findNodeForward( match.args.parent, "LPAR" )
            par_node.replace( makeLeaf( "PYJS", "extends", " " ) )
            par_node = self.findNodeReverse( match.args.parent, "RPAR" )
            par_node.remove()
        match.colon.remove()
        class_suite = match.suite
        class_suite.insert_child( 0, makeLeaf( "LBRACE", "{", ' ' ) )
        last_dedent_idx = self.findNodeReverseIndex( class_suite, "DEDENT", None )
        if last_dedent_idx is None:
            class_suite.append_child( makeLeaf( "RBRACE", "}", "" ) )
            class_suite.append_child( makeLeaf( "NEWLINE", "\n", "" ) )
        else:
            class_suite.insert_child( last_dedent_idx, makeLeaf( "RBRACE", "}", "" ) )
            class_suite.insert_child( last_dedent_idx + 1, makeLeaf( "NEWLINE", "\n", "" ) )

