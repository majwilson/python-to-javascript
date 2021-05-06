from Converter import Converter
from helpers import Treeverser, makeLeaf, getNodeIndex, makeImport
from fissix.pytree import Node, Leaf


class ImportNameConverter( Converter ):
    """ gather "import module """

    PATTERN = """
        import_name < import_word='import' any* dotted_as_name < imported=dotted_name as_word='as' as_name=NAME > any* >
            |
        import_name < import_word='import' imported=any* >
    """

    def gather( self, node ):
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.PATTERN )
        return matches

    def processOne( self, match ):
        if "as_word" in match:
            self._processHasAs( match )
        else:
            self._processNotAs( match )

    def _processNotAs( self, match ):
        par_node = match.import_word.parent
        match.import_word.remove();

        imp_names = [ s.strip() for s in str( match.imported[ 0 ] ).split( "," ) ]
        match.imported[ 0 ].remove()

        for imp_name in imp_names:
            imp_node = makeImport()
            imp_node.append_child( makeLeaf( "PYJS", "const " ) )
            imp_node.append_child( makeLeaf( "PYJS", imp_name ) )
            imp_node.append_child( makeLeaf( "EQUAL", " = " ) )
            imp_node.append_child( makeLeaf( "PYJS", "require( './" ) )
            imp_node.append_child( makeLeaf( "PYJS", imp_name ) )
            imp_node.append_child( makeLeaf( "PYJS", "' )" ) )
            if imp_name != imp_names[ -1 ]:
                imp_node.append_child( makeLeaf( "NEWLINE", "\n", "" ) )
            par_node.append_child( imp_node )

    def _processHasAs( self, match ):
        par_node = match.import_word.parent
        match.import_word.remove();

        imp_name = match.imported
        match.imported.remove()
        match.as_word.remove()
        match.as_name.remove()
        imp_node = makeImport()
        imp_node.append_child( makeLeaf( "PYJS", "const " ) )
        imp_node.append_child( makeLeaf( "PYJS", str( match.as_name ).strip() ) )
        imp_node.append_child( makeLeaf( "EQUAL", " = " ) )
        imp_node.append_child( makeLeaf( "PYJS", "require( './" ) )
        imp_node.append_child( makeLeaf( "PYJS", str( match.imported ).strip().replace( ".", "/" ), "" ) )
        imp_node.append_child( makeLeaf( "PYJS", "' )" ) )
        par_node.append_child( imp_node )
