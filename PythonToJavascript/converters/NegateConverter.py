from Converter import Converter
from helpers import Treeverser, AnonObj, makeLeaf, getNodeIndex


class NegateConverter( Converter ):

    PATTERN = """
        not_test< not_word='not' right=any >
    """

    def gather( self, node ):
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.PATTERN )
        return matches

    def processOne( self, match ):
        match.not_word.replace( makeLeaf( "PYJS", "!", match.not_word.prefix ) )
        match.right.prefix = ""

