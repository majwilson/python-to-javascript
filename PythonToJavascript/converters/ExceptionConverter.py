from Converter import Converter
from helpers import Treeverser, makeLeaf, makeStatement, getNodeIndex, dumpTree


class ExceptionConverter( Converter ):
    """
        raise NameError( 'bill' ) => throw new Error( 'NameError', bill )
    """

    PATTERN = """
        raise_stmt < raise_word='raise' exc_name=NAME >
        |
        raise_stmt < raise_word='raise' power < exc_name=NAME trailer< '(' args=any ')' > > >
    """

    def gather( self, node ):
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.PATTERN )
        return matches

    def processOne( self, match ):
        new = makeStatement()
        new.append_child( makeLeaf( "PYJS", "throw", match.raise_word.prefix ) )
        new.append_child( makeLeaf( "PYJS", "new", ' ' ) )
        new.append_child( makeLeaf( "PYJS", "Error", ' ' ) )
        new.append_child( makeLeaf( "LPAR", "(", "" ) )
        new.append_child( makeLeaf( "PYJS", "'%s'" % match.exc_name.toString(), ' ' ) )
        if "args" in match:
            new.append_child( makeLeaf( "COMMA", ",", "" ) )
            new.append_child( match.args )
        new.append_child( makeLeaf( "RPAR", ")", " " ) )
        match.node.replace( new )
