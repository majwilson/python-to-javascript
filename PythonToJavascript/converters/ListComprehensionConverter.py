from Converter import Converter
from helpers import Treeverser, makeLeaf, getNodeIndex, makeStatement
from fissix.pytree import Node, Leaf

import re

class ListComprehensionConverter( Converter ):

    COMP_PATTERN = """
        atom<
            lsqb='[' listmaker<
                item_value=any* comp_for<
                    for_word='for' locals=any* in_word='in' looper=any*
                    ( comp_if<
                        'if' test=any*
                    > )*
                >
            > rsqb=']'
        >
    """

    def gather( self, node ):
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.COMP_PATTERN )
        for match in matches:
            match.item_value = match.item_value[ 0 ]
            match.locals = match.locals[ 0 ]
            match.looper = match.looper[ 0 ]
            if "test" in match:
                match.test = match.test[ 0 ]
        return matches

    def processOne( self, match ):
        parent = match.lsqb.parent
        new = makeStatement()
        num_locals = len( str( match.locals ).split( "," ) )
        match.looper.remove()
        new.append_child( match.looper )
        if "test" in match:
            new.append_child( makeLeaf( "PYJS", ".filter", "" ) )
            new.append_child( makeLeaf( "LPAR", "(", '' ) )
            if num_locals > 1:
                new.append_child( makeLeaf( "LPAR", "(", ' ' ) )
                new.append_child( makeLeaf( "LSQB", "[", ' ' ) )
            new.append_child( match.locals.clone() )
            if num_locals > 1:
                new.append_child( makeLeaf( "RSQB", "]", ' ' ) )
                new.append_child( makeLeaf( "RPAR", ")", ' ' ) )
            new.append_child( makeLeaf( "PYJS", "=>", ' ' ) )
            match.test.remove()
            new.append_child( match.test )
            new.append_child( makeLeaf( "RPAR", ")", ' ' ) )
        if self.needsMap( match.item_value, match.locals ):
            new.append_child( makeLeaf( "PYJS", ".map", "" ) )
            new.append_child( makeLeaf( "LPAR", "(", '' ) )
            if num_locals > 1:
                new.append_child( makeLeaf( "LPAR", "(", ' ' ) )
                new.append_child( makeLeaf( "LSQB", "[", ' ' ) )
            new.append_child( match.locals.clone() )
            if num_locals > 1:
                new.append_child( makeLeaf( "RSQB", "]", ' ' ) )
                new.append_child( makeLeaf( "RPAR", ")", ' ' ) )
            new.append_child( makeLeaf( "PYJS", "=>", ' ' ) )
            match.item_value.remove()
            new.append_child( match.item_value )
            new.append_child( makeLeaf( "RPAR", ")", ' ' ) )
        parent.replace( new )

    def needsMap( self, return_vars, local_vars ):
        return_vars = re.sub( r'\s+', '', str( return_vars ) )
        local_vars = re.sub( r'\s+', '', str( local_vars ) )
        return not( return_vars == local_vars or return_vars == f"({ local_vars })" )

