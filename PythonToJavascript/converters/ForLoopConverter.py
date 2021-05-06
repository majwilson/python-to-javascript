from Converter import Converter
from helpers import Treeverser, makeLeaf, getNodeIndex


class ForLoopConverter( Converter ):

    FORLOOP_PATTERN = """
        for_stmt< for_word='for' loop_vars=any in_word='in' iterable=any for_colon=':' for_suite=any* >
    """

    def gather( self, node ):
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.FORLOOP_PATTERN )
        for match in matches:
            match.for_suite = match.for_suite[ 0 ]
        return matches

    def processOne( self, match ):
        forloop_indent = self.calcIndent( match.node )

                # replace ( x, y ) with [ x, y ]
        loop_vars_lpar_node = self.findNodeForward( match.loop_vars, "LPAR", None )
        if loop_vars_lpar_node:
            loop_vars_lpar_node.replace( makeLeaf( "LSQB", "[", loop_vars_lpar_node.prefix ) )
            loop_vars_rpar_node = self.findNodeReverse( match.loop_vars, "RPAR" )
            loop_vars_rpar_node.replace( makeLeaf( "RSQB", "]", loop_vars_rpar_node.prefix ) )
        else:   # replace x, y with [ x, y ]
            loop_vars_comma_node = self.findNodeForward( match.loop_vars, "COMMA", None )
            if loop_vars_comma_node:
                match.loop_vars.insert_child( 0, makeLeaf( "LSQB", "[", " " ) )
                match.loop_vars.append_child( makeLeaf( "RSQB", "]", " " ) )

            # in => of
        match.in_word.replace( makeLeaf( "PYJS", "of", " " ) )

            # parens round loop head
        par_node = match.node
        for_idx = getNodeIndex( match.for_word  )
        par_node.insert_child( for_idx + 1, makeLeaf( "LPAR", "(", '' ) )
        par_node.insert_child( for_idx + 2, makeLeaf( "PYJS", "let", ' ' ) )
        match.for_colon.replace( makeLeaf( "RPAR", ")", " " ) )

            # braces round loop body
        for_suite = match.for_suite
        for_suite.insert_child( 0, makeLeaf( "LBRACE", "{", ' ' ) )
        last_dedent_idx = self.findNodeReverseIndex( for_suite, "DEDENT" )
        for_suite.insert_child( last_dedent_idx, makeLeaf( "RBRACE", "}", forloop_indent ) )
        for_suite.insert_child( last_dedent_idx + 1, makeLeaf( "NEWLINE", "\n", "" ) )
