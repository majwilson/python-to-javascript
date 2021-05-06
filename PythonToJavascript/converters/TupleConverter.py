from Converter import Converter
from helpers import Treeverser, makeLeaf


class TupleConverter( Converter ):

    PATTERN = """
        atom< lpar='(' contents=testlist_gexp rpar=')'  >
    """

    def gather( self, node ):
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.PATTERN )
        return matches

    def processOne( self, match ):
        match.lpar.replace( makeLeaf( "LSQB", "[", match.lpar.prefix ) )
        match.rpar.replace( makeLeaf( "RSQB", "]", match.rpar.prefix ) )

