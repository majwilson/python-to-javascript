from Converter import Converter
from helpers import Treeverser, makeLeaf, getNodeIndex


class BoolOpsConverter( Converter ):

    PATTERN = """
        and_test< left=any* and_word='and' right=any* > | or_test< left=any* or_word='or' right=any* >
    """

    def gather( self, node ):
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.PATTERN )
        for match in matches:
            match.left = match.left[ 0 ]
            match.right = match.right[ 0 ]
        return matches

    def processOne( self, match ):
        if "and_word" in match:
            match.and_word.replace( makeLeaf( "PYJS", "&&", match.and_word.prefix ) )
        elif "or_word" in match:
            match.or_word.replace( makeLeaf( "PYJS", "||", match.or_word.prefix ) )
