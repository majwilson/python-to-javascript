from Converter import Converter
from helpers import Treeverser, makeLeaf, getNodeIndex, clearNode, dumpTree


class ListSliceConverter( Converter ):
    """ FIXME """

    PATTERN = """
        trailer < lsqb='[' subscript < start=any colon=':' finish=any > rsqb=']' >
        |
        trailer < lsqb='[' subscript < colon=':' finish=any > rsqb=']' >
        |
        trailer < lsqb='[' subscript < start=any colon=':' > rsqb=']' >
        |
        trailer < lsqb='[' colon=':' rsqb=']' >
    """

    def gather( self, node ):
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.PATTERN )
        return matches

    def processOne( self, match ):
        clearNode( match.node )
        match.node.append_child( makeLeaf( "PYJS", ".slice" ) )
        match.node.append_child( makeLeaf( "LPAR", "(" ) )
        if not ( "start" in match or "finish" in match ):
            match.node.append_child( makeLeaf( "RPAR", ")", "" ) )
        else:
            if "start" in match:
                match.node.append_child( match.start.clone() )
            else:
                match.node.append_child( makeLeaf( "PYJS", "0", " " ) )
            if "finish" in match:
                match.node.append_child( makeLeaf( "COMMA", ",", "" ) )
                match.node.append_child( match.finish.clone() )
            match.node.append_child( makeLeaf( "RPAR", ")", " " ) )
