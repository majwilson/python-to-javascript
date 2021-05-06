from Converter import Converter
from helpers import Treeverser, AnonObj, makeLeaf, gatherSubNodesD, getNodeKind, getNodeIndex


class TryExceptConverter( Converter ):

    TRYEX_PATTERN = """
        try_stmt< try_word='try' try_colon=':' try_suite=any*
            ( exc_clause=except_clause< exc_word='except' exc_what=any* > | exc_word='except' )
            exc_colon=':' exc_suite=any*
            ( fin_word='finally' fin_colon=':' fin_suite=any* )*  >
    """

    def gather( self, node ):
        """ return list of AnonObjs containing the info we need """
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.TRYEX_PATTERN )

        infos = []
        for match in matches:
            info = AnonObj()
            info.node = match.node
            info.try_word = match.try_word
            info.try_colon = match.try_colon
            info.try_suite = match.try_suite[ 0 ]
            if "exc_clause" in match:
                info.exc_clause = match.exc_clause
                for node in gatherSubNodesD( info.exc_clause ):
                    if getNodeKind( node ) == "NAME" and node.value == "as":
                        info.exc_as = node
                        as_idx = getNodeIndex( node )
                        info.exc_as_name = node.parent.children[ as_idx + 1  ]

            info.exc_word = match.exc_word
            if "exc_what" in match:
                info.exc_what = match.exc_what[ 0 ]
            info.exc_colon = match.exc_colon
            info.exc_suite = match.exc_suite[ 0 ]

            if "fin_word" in match:
                info.fin_word = match.fin_word
                info.fin_colon = match.fin_colon
                info.fin_suite = match.fin_suite[ 0 ]

            infos.append( info )
        return infos

    def processOne( self, match ):
        """ NB don't replace "raise" with "throw" """
        tryex_indent= self.calcIndent( match.node ) + "    "

        match.try_colon.remove()
        try_suite = match.try_suite
        try_suite.insert_child( 0, makeLeaf( "LBRACE", "{", ' ' ) )
        last_dedent_idx = self.findNodeReverseIndex( try_suite, "DEDENT" )
        indent = self.calcIndent( match.exc_word )
        try_suite.insert_child( last_dedent_idx, makeLeaf( "RBRACE", "}", indent ) )

        name_parent = match.exc_word.parent
        name_idx = getNodeIndex( match.exc_word )
        match.exc_word.replace( makeLeaf( "PYJS", "catch", " " ) )

        if "exc_as" in match:
            match.exc_as.remove()
        if "exc_as_name" in match:
            as_name = match.exc_as_name.value
            match.exc_as_name.remove()
        else:
            as_name = "e"

        name_parent.insert_child( name_idx + 1, makeLeaf( "LPAR", "(", "" ) )
        name_parent.insert_child( name_idx + 2, makeLeaf( "PYJS", as_name, " " ) )
        name_parent.insert_child( name_idx + 3, makeLeaf( "RPAR", ")", " " ) )

        if "exc_what" in match:
            exc_what = match.exc_what
            what_idx = getNodeIndex( exc_what )
            exc_what.parent.insert_child( what_idx, makeLeaf( "PYJS", "/*", ' ' ) )
            exc_what.parent.insert_child( what_idx + 2, makeLeaf( "PYJS", "*/", ' ' ) )

        match.exc_colon.remove()
        exc_suite = match.exc_suite
        exc_suite.insert_child( 0, makeLeaf( "LBRACE", "{", ' ' ) )
        last_dedent_idx = self.findNodeReverseIndex( exc_suite, "DEDENT" )
        exc_suite.insert_child( last_dedent_idx, makeLeaf( "RBRACE", "}", tryex_indent[ : -4 ] ) )
        if "fin_word" not in match:
            exc_suite.insert_child( last_dedent_idx + 1, makeLeaf( "NEWLINE", "\n", "" ) )

        if "fin_word" in match:
            match.fin_word.prefix += " "
            match.fin_colon.remove()
            fin_suite = match.fin_suite
            fin_suite.insert_child( 0, makeLeaf( "LBRACE", "{", ' ' ) )
            last_dedent_idx = self.findNodeReverseIndex( fin_suite, "DEDENT" )
            fin_suite.insert_child( last_dedent_idx, makeLeaf( "RBRACE", "}", tryex_indent[ : -4 ] ) )
            fin_suite.insert_child( last_dedent_idx + 1, makeLeaf( "NEWLINE", "\n", "" ) )
