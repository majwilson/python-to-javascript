from Converter import Converter
from helpers import Treeverser, makeLeaf, getNodeIndex, gatherSubNodesD, getNodeKind, findOutNode


class FunctionConverter( Converter ):

    def __init__( self, in_class=False ):
        super( FunctionConverter, self ).__init__()
        self.in_class = in_class


    FUNC_PATTERN = """
        funcdef < def_word='def' name=NAME params=parameters< '(' args=any* ')' > colon=':' suite=suite rest=any* >
    """

    def gather( self, node ):
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.FUNC_PATTERN )
        for match in matches:
            if match.get( "args", None ):
                match.args = match.args[ 0 ]
        return matches

    def processOne( self, match ):
        func_indent = self.calcIndent( match.node )

        if self.in_class:
            match.def_word.remove()
            match.name.prefix = func_indent
        else:
            match.def_word.replace( makeLeaf( "NAME", "function", func_indent ) )

        match.colon.remove()
        func_suite = match.suite
        func_suite.insert_child( 0, makeLeaf( "LBRACE", "{", ' ' ) )
        last_dedent_idx = self.findNodeReverseIndex( func_suite, "DEDENT" )
        func_suite.insert_child( last_dedent_idx, makeLeaf( "RBRACE", "}", func_indent ) )
        func_suite.insert_child( last_dedent_idx + 1, makeLeaf( "NEWLINE", "\n", "" ) )

            # remove any "self" param + comma + space before closing paren
        self_param = self.findSelfParam( match.params )
        if self_param:
            child_nodes = self_param.parent.children
            self_param.remove()
            if child_nodes:
                first_node = child_nodes[ 0 ]
                if getNodeKind( first_node ) == "COMMA":
                    first_node.remove()
                if len( child_nodes ) == 2:
                    child_nodes[ -1 ].prefix = ""


    def findSelfParam( self, node ):
        for sub_node in gatherSubNodesD( node ):
            if getNodeKind( sub_node ) == "NAME" and sub_node.value =="self":
                return sub_node
        return None
