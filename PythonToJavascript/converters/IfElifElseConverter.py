from Converter import Converter
from helpers import Treeverser, AnonObj, makeLeaf, getNodeIndex


class IfElifElseConverter( Converter ):
    """ class to handle gathering of if / elif /else statements
        NB returns object with if_clause, elif_clauses, else_clause """

    IF_PATTERN = """
        if_stmt <
            if_word='if' if_test=any* if_colon=':' if_suite=any*
            elif=( elif_word='elif' elif_test=any* elif_colon=':' elif_suite=any* )*
            else=( else_word='else' else_colon=':' else_suite=any* )*
            >
    """

    def gather( self, node ):
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.IF_PATTERN )
        infos = []
        for match in matches:

            info = AnonObj( if_clause=None, elif_clauses=[], else_clause=None )

            info.if_clause = self.gatherIfStatement( match )

            info.elif_clauses = self.gatherElifStatements( match )

            node = match.get( "else", None )
            if node:
                info.else_clause = self.gatherElseStatement( match )

            infos.append( info )
        return infos


    def gatherIfStatement( self, if_match ):
        if_match.if_suite = if_match.if_suite[ 0 ]
        return if_match

    def gatherElifStatements( self, elif_match ):
        """ return list of AnonObjs containing the info we need """
        new_list = []
        elif_nodes = elif_match.get( "elif", [] )
        for idx in range( 0, len( elif_nodes ), 4 ):
            elif_info = AnonObj()
            elif_info.elif_word = elif_nodes[ idx + 0 ]
            elif_info.elif_test = elif_nodes[ idx + 1 ]
            elif_info.elif_colon = elif_nodes[ idx + 2 ]
            elif_info.elif_suite = elif_nodes[ idx + 3 ]
            new_list.append( elif_info )
        return new_list

    def gatherElseStatement( self, else_match ):
        else_match.else_suite = else_match.else_suite[ 0 ]
        return else_match

    def processAll( self, matches ):
        all_if_suites = []
        for match in matches:

            if_indent = self.calcIndent( match.if_clause.if_word )

            # if part
            par_node = match.if_clause.if_suite.parent
            if_idx = par_node.children.index( match.if_clause.if_word )
            par_node.insert_child( if_idx + 1, makeLeaf( "LPAR", "(", '' ) )
            match.if_clause.if_colon.replace( makeLeaf( "RPAR", ")", " " ) )
            if_suite = match.if_clause.if_suite
            if_suite.insert_child( 0, makeLeaf( "LBRACE", "{", ' ' ) )
            last_dedent = self.findNodeReverse( if_suite, "DEDENT" )
            last_dedent.prefix = ""
            last_dedent_idx = getNodeIndex( last_dedent )
            last_dedent.parent.insert_child( last_dedent_idx + 0, makeLeaf( "RBRACE", "}", if_indent ) )
            if not match.elif_clauses and not match.else_clause:
                last_dedent.parent.insert_child( last_dedent_idx + 1, makeLeaf( "NEWLINE", "\n", "" ) )

            all_if_suites.append( if_suite )

            # elif parts
            for elif_match in match.elif_clauses:
                par_node = elif_match.elif_test.parent
                if_idx = par_node.children.index( elif_match.elif_word )
                elif_match.elif_word.replace( makeLeaf( "PYJS", "else if", " " ) )
                par_node.insert_child( if_idx + 1, makeLeaf( "LPAR", "(", '' ) )
                elif_match.elif_colon.replace( makeLeaf( "RPAR", ")", " " ) )
                elif_suite = elif_match.elif_suite
                elif_suite.insert_child( 0, makeLeaf( "LBRACE", "{", ' ' ) )
                last_dedent_idx = self.findNodeReverseIndex( elif_suite, "DEDENT" )
                elif_suite.insert_child( last_dedent_idx, makeLeaf( "RBRACE", "}", '' ) )
                if not match.else_clause:
                    elif_suite.insert_child( last_dedent_idx + 1, makeLeaf( "NEWLINE", "\n", "" ) )

                all_if_suites.append( elif_suite )

            # else part
            if match.else_clause:
                match.else_clause.else_colon.remove()
                prefix = match.else_clause.else_word.prefix
                match.else_clause.else_word.prefix = " "
                else_suite = match.else_clause.else_suite
                last_dedent = self.findNodeReverse( else_suite, "DEDENT" )

                else_suite.insert_child( 0, makeLeaf( "LBRACE", "{", " " ) )
                last_dedent_idx = getNodeIndex( last_dedent )
                else_suite.insert_child( last_dedent_idx, makeLeaf( "RBRACE", "}", if_indent ) )

                # sometimes we get a blank line due to this but its better than
                #    missing the '\n' most of the time
                else_suite.insert_child( last_dedent_idx + 1, makeLeaf( "NEWLINE", "\n", "" ) )

                all_if_suites.append( else_suite )

        for sub_if_suite in all_if_suites:
            sub_if_matches = self.gather( sub_if_suite )
            self.processAll( sub_if_matches )
