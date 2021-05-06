from Converter import Converter
from helpers import Treeverser, makeLeaf, getNodeIndex, makeImport


class ImportFromConverter( Converter ):
    """ gather "import module """

    PATTERN = """
        import_from < from_word='from' module=any* import_word='import' lpar='('* imported=(NAME | import_as_names) rpar=')'* >
    """

    def gather( self, node ):
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.PATTERN )
        infos = []
        for match in matches:
            match.from_word = match.from_word
            match.module = match.module[ 0 ]
            match.import_word = match.import_word
            if match.lpar:
                match.lpar = match.lpar[ 0 ]
            match.imported = match.imported[ 0 ]
            if match.rpar:
                match.rpar = match.rpar[ 0 ]
        return matches

    def processOne( self, match ):
        par_node = match.import_word.parent
        match.from_word.remove();
        match.import_word.remove();

        imp_names = [ s.strip() for s in str( match.imported ).split( "," ) ]

        match.imported.remove()

        if match.lpar:
            match.lpar.remove()
        if match.rpar:
            match.rpar.remove()

        imp_node = makeImport()
        imp_node.append_child( makeLeaf( "PYJS", "const " ) )
        imp_node.append_child( makeLeaf( "LBRACE", "{", "" ) )
        match.imported.remove()
        imp_node.append_child( match.imported  )
        imp_node.append_child( makeLeaf( "RBRACE", "}", " " ) )
        imp_node.append_child( makeLeaf( "EQUAL", " = " ) )
        imp_node.append_child( makeLeaf( "PYJS", "require( './" ) )
        match.module.remove()
        match.module.prefix = ""
        imp_node.append_child( match.module )
        imp_node.append_child( makeLeaf( "PYJS", "' )" ) )
        par_node.append_child( imp_node )
