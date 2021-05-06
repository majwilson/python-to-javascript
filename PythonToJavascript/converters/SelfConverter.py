from Converter import Converter
from helpers import Treeverser, makeLeaf, getNodeIndex


class SelfConverter( Converter ):

    SELF_PATTERN = """
        power< self='self' trailer< dot='.' right=any* > ( rest=trailer< any* > )* >
    """

    def gather( self, node ):
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.SELF_PATTERN )
        infos = []
        for match in matches:
            match.right = match.right[ 0 ]
        return matches

    def processOne( self, match ):
        match.self.replace( makeLeaf( "PYJS", "this", match.self.prefix ) )

