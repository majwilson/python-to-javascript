from Converter import Converter
from helpers import Treeverser, makeLeaf, getNodeIndex


class DecoratorConverter( Converter ):
    """ make decorators into comments """

    PATTERN = """
        decorator < at_sym='@' decorated=any* newl='\\n' >
    """

    def gather( self, node ):
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.PATTERN )
        return matches

    def processOne( self, match ):
        par_node = match.newl.parent
        par_node.insert_child( 0, makeLeaf( "PYJS", "/* ", match.at_sym.prefix ) )
        match.at_sym.prefix = ""
        newl_idx = par_node.children.index( match.newl )
        par_node.insert_child( newl_idx, makeLeaf( "PYJS", " DECORATOR */" ) )
