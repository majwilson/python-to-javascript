from Converter import Converter
from helpers import Treeverser, makeLeaf, getNodeIndex, getNodeKind


class AssignmentConverter( Converter ):

    ASSN_PATTERN = """
        expr_stmt < left=any* equals='=' right=any* >
    """

    def gather( self, node ):
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.ASSN_PATTERN )
        for match in matches:
            match.left = match.left[ 0 ]
            match.right = match.right[ 0 ]
        return matches

    def processAll( self, matches ):
        done_vars = []
        for match in matches:
            if getNodeKind( match.left ) == "atom":
                name_node = match.left
            elif getNodeKind( match.left ) == "NAME":
                name_node = match.left
            else:
                name_node = self.findNodeForward( match.left, "NAME", None )
            if name_node:
                str_name_node = name_node.toString()
                if str_name_node != "self" and str_name_node not in done_vars:
                    name_node.parent.insert_child( 0, makeLeaf( "PYJS", "let", name_node.prefix ) )
                    name_node.prefix = " "
                    done_vars.append( str_name_node )

