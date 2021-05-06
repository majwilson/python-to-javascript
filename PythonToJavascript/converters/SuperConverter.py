from Converter import Converter
from helpers import Treeverser, AnonObj, makeLeaf, getNodeIndex, dumpTree


class SuperConverter( Converter ):
    """
        super( SPVEBorderColorMixed, self ).setupValue() => super.setupValue()
        super( SPVEBorderColorMixed, self ).__init__() => super()
    """

    PATTERN = """
        power < 'super' super_args=trailer super_method=trailer method_args=trailer > rest=any*
    """

    def gather( self, node ):
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.PATTERN )
        return matches

    def processOne( self, match ):
        match.super_args.remove()
        if str( match.super_method ) == ".__init__":
            match.super_method.remove()

