from Converter import Converter
from helpers import Treeverser, AnonObj, makeLeaf, getNodeIndex


class WhileLoopConverter( Converter ):
    """ class to handle gathering of while statements
        NB returns object with if_clause, elif_clauses, else_clause """

    PATTERN = """
        while_stmt <
            name='while' test=any* colon=':' suite=any*
            >
    """

    def gather( self, node ):
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.PATTERN )
        for match in matches:
            match.test = match.test[ 0 ]
            match.suite = match.suite[ 0 ]
        return matches

    def processOne( self, match ):
        whileloop_indent= self.calcIndent( match.node )

        par_node = match.node
        while_idx = getNodeIndex( match.name  )
        par_node.insert_child( while_idx + 1, makeLeaf( "LPAR", "(", '' ) )
        match.colon.replace( makeLeaf( "RPAR", ")", " " ) )

        suite = match.suite
        suite.insert_child( 0, makeLeaf( "LBRACE", "{", ' ' ) )
        last_dedent_idx = self.findNodeReverseIndex( suite, "DEDENT" )
        suite.insert_child( last_dedent_idx, makeLeaf( "RBRACE", "}", whileloop_indent ) )
        suite.insert_child( last_dedent_idx + 1, makeLeaf( "NEWLINE", "\n", "" ) )
