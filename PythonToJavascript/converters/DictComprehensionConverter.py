from Converter import Converter
from helpers import Treeverser, AnonObj, makeLeaf, getNodeIndex, makeStatement


class DictComprehensionConverter( Converter ):

    COMP_PATTERN = """
        atom<
            lbrace='{' dictsetmaker<
                item_key=any* colon=':' item_value=any* comp_for<
                    for_word='for' locals=any* in_word='in' looper=any*
                    ( comp_if<
                        'if' test=any*
                    > )*
                >
            > rbrace='}'
        >
    """

    MAP = "__map"   # name of local map object

    def gather( self, node ):
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.COMP_PATTERN )
        for match in matches:
            match.item_key = match.item_key[ 0 ]
            match.item_value = match.item_value[ 0 ]
            match.locals = match.locals[ 0 ]
            match.looper = match.looper[ 0 ]
            if "test" in match:
                match.test = match.test[ 0 ]
        return matches


    def processOne( self, match ):
        parent = match.lbrace.parent
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

        new.append_child( makeLeaf( "DOT", ".", "" ) )
        new.append_child( makeLeaf( "PYJS", "reduce", "" ) )
        new.append_child( makeLeaf( "LPAR", "(", '' ) )
        new.append_child( makeLeaf( "LPAR", "(", ' ' ) )
        new.append_child( makeLeaf( "PYJS", self.MAP, " " ) )
        new.append_child( makeLeaf( "COMMA", ",", '' ) )
        if num_locals > 1:
            new.append_child( makeLeaf( "LSQB", "[", ' ' ) )
        match.locals.remove()
        new.append_child( match.locals )
        new.append_child( match.item_value )
        if num_locals > 1:
            new.append_child( makeLeaf( "RSQB", "]", ' ' ) )
        new.append_child( makeLeaf( "RPAR", ")", ' ' ) )
        new.append_child( makeLeaf( "PYJS", "=>", ' ' ) )
        new.append_child( makeLeaf( "LPAR", "(", ' ' ) )
        new.append_child( makeLeaf( "LBRACE", "{", ' ' ) )
        new.append_child( makeLeaf( "PYJS", "...", ' ' ) )
        new.append_child( makeLeaf( "PYJS", self.MAP, "" ) )
        new.append_child( makeLeaf( "COMMA", ",", '' ) )
        new.append_child( makeLeaf( "LSQB", "[", ' ' ) )
        match.item_key.remove()
        new.append_child( match.item_key )
        new.append_child( makeLeaf( "RSQB", "]", ' ' ) )
        new.append_child( makeLeaf( "COLON", ":", "" ) )
        match.item_value.remove()
        new.append_child( match.item_value )
        new.append_child( makeLeaf( "RBRACE", "}", ' ' ) )
        new.append_child( makeLeaf( "RPAR", ")", ' ' ) )
        new.append_child( makeLeaf( "COMMA", ",", '' ) )
        new.append_child( makeLeaf( "LBRACE", "{", ' ' ) )
        new.append_child( makeLeaf( "RBRACE", "}", '' ) )
        new.append_child( makeLeaf( "RPAR", ")", ' ' ) )
        parent.replace( new )

