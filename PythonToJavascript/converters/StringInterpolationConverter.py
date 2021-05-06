from Converter import Converter
from helpers import Treeverser, makeLeaf, makeStatement, getNodeKind
from fissix.pytree import Node, Leaf


class StringInterpolationConverter( Converter ):
    """ str % ( a, b, c ) => _pyjs.stringFormat( str, a, b, c ) """

    PATTERN = """
        term < left=any+ percent_sym='%' right=any+ >
    """
    USE_PYJS = True

    def gather( self, node ):
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.PATTERN )
        for match in matches:
            match.left = match.left[ 0 ]
            match.right = match.right[ 0 ]
        return matches

    def processOne( self, match ):
        if self.USE_PYJS:
            self.processOne_PYJS( match )
        else:
            self.processOne_NO_PYJS( match )

    def processOne_PYJS( self, match ):
        """
            this results in
                _pyjs.stringInterpolate( left, right );
            which is a short but needs the external function
        """
        is_multi = getNodeKind( match.right ) == "power" or \
                                        len( str( match.right ).split( "," ) ) > 1
        new = makeStatement()
        new.append_child( makeLeaf( "NAME", "_pyjs.stringInterpolate", match.left.prefix ) )
        new.append_child( makeLeaf( "LPAR", "(" ) )
        match.left.prefix = ' '
        new.append_child( match.left )
        new.append_child( makeLeaf( "COMMA", ",", "" ) )
        if not is_multi:
            new.append_child( makeLeaf( "LSQB", "[", ' ' ) )
        new.append_child( match.right )
        if not is_multi:
            new.append_child( makeLeaf( "RSQB", "]", ' ' ) )

        new.append_child( makeLeaf( "RPAR", ")", " " ) )
        match.percent_sym.parent.replace( new )

    def processOne_NO_PYJS( self, match ):
        """
            this results in
                right.reduce( ( a, c ) => a.replace( /%(s|i|r)?/, c.toString () ), left );
            which is self-contained but a bit long-winded
        """
        is_multi = getNodeKind( match.right ) == "power" or \
                                        len( str( match.right ).split( "," ) ) > 1

        new = makeStatement()
        if not is_multi:
            new.append_child( makeLeaf( "LSQB", "[", ' ' ) )
        new.append_child( match.right )
        if not is_multi:
            new.append_child( makeLeaf( "RSQB", "]", ' ' ) )
        new.append_child( makeLeaf( "DOT", ".", '' ) )
        new.append_child( makeLeaf( "PYJS", "reduce", '' ) )
        new.append_child( makeLeaf( "LPAR", "(", '' ) )
        new.append_child( makeLeaf( "LPAR", "(", ' ' ) )
        new.append_child( makeLeaf( "PYJS", "a", ' ' ) )
        new.append_child( makeLeaf( "COMMA", ",", "" ) )
        new.append_child( makeLeaf( "PYJS", "c", ' ' ) )
        new.append_child( makeLeaf( "RPAR", ")", ' ' ) )
        new.append_child( makeLeaf( "PYJS", "=>", ' ' ) )
        new.append_child( makeLeaf( "PYJS", "a", ' ' ) )
        new.append_child( makeLeaf( "DOT", ".", '' ) )
        new.append_child( makeLeaf( "PYJS", "replace", '' ) )
        new.append_child( makeLeaf( "LPAR", "(", '' ) )
        new.append_child( makeLeaf( "PYJS", "/%(s|i|r)?/", ' ' ) )
        new.append_child( makeLeaf( "COMMA", ",", "" ) )
        new.append_child( makeLeaf( "PYJS", "c", ' ' ) )
        new.append_child( makeLeaf( "DOT", ".", '' ) )
        new.append_child( makeLeaf( "PYJS", "toString", '' ) )
        new.append_child( makeLeaf( "LPAR", "(", ' ' ) )
        new.append_child( makeLeaf( "RPAR", ")", '' ) )
        new.append_child( makeLeaf( "RPAR", ")", ' ' ) )
        new.append_child( makeLeaf( "COMMA", ",", "" ) )
        match.left.prefix = ' '
        new.append_child( match.left )
        new.append_child( makeLeaf( "RPAR", ")", ' ' ) )

        match.percent_sym.parent.replace( new )
