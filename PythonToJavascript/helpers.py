import fissix
from fissix.pytree import Node, Leaf
from fissix.pgen2 import driver as pgen2_driver
from fissix.pgen2 import token as pgen2_token
from fissix.pygram import python_symbols
from fissix import patcomp

# it's handy to import this from here when developing
from bowler.helpers import print_tree as dumpTree

import os
from textwrap import dedent

# --------------------------------------------------------------------------------------------------
# load grammar & make a driver we can use to parse
fissix_dir = os.path.dirname( fissix.__file__ )
grammar_path = os.path.join( fissix_dir, "Grammar.txt" )
m_grammar = pgen2_driver.load_grammar( grammar_path )
driver = pgen2_driver.Driver( m_grammar, convert=fissix.pytree.convert )

def parseString( string ):
    return driver.parse_string( dedent( string ) + "\n\n", debug=True )

def getGrammar():
    return m_grammar


# --------------------------------------------------------------------------------------------------
def makeLeaf( type_name, value, prefix="" ):
    type_num = typeNameToNum( type_name )
    return Leaf( type_num, value, prefix=prefix )

def makeStatement():
    return Node( python_symbols.stmt, [] )

def makeImport():
    return Node( python_symbols.import_stmt, [] )

def makeTrailer():
    return Node( python_symbols.trailer, [] )

def clearNode( node ):
    for n in node.children[ : ]:
        n.remove()

def typeNameToNum( type_name ):
    from fissix.pgen2 import token as pgen2_token
    num = getattr( pgen2_token, type_name, ... )
    if num is not ...:
        return num
    raise Exception( "cannot get type num for {}".format( type_name ) )

# --------------------------------------------------------------------------------------------------
def gatherSubNodesD( nodes, output=None ):
    """ gather all nodes into a flat list - depth-first """
    output = [] if output is None else output
    if not isinstance( nodes, list ):
        nodes = [ nodes ]
    for node in nodes:
        output.append( node )
        for child_node in node.children:
            gatherSubNodesD( child_node, output )
    return output

def findSubNode( nodes, testFunc, fallback=... ):
    for out_node in gatherSubNodesD( node ):
        if testFunc( out_node ):
            return out_node
    if fallback is not ...:
        return fallback
    raise Exception( 'cannot find sub node' )

def findOutNode( node, testFunc, fallback=... ):
    """ get node and all its parents, inner to outer order """
    for out_node in getOutNodes( node ):
        if testFunc( out_node ):
            return out_node
    if fallback is not ...:
        return fallback
    raise Exception( 'cannot find out node' )

def getOutNodes( node ):
    nodes = [ node ]
    while node.parent:
        nodes.append( node.parent )
        node = node.parent
    return nodes

def getNodeKind( node, fallback=...):
    """ node can be Leaf (symbol) or Node (token) """
    if isinstance( node, Leaf ):
        return typeNumToName( node.type, fallback )
    else:
        return symNumToSymbol( node.type, fallback )

def getNodeIndex( node ):
    return node.parent.children.index( node )

m_grammar_nums_to_syms = {}
for k, v in getGrammar().symbol2number.items():
    m_grammar_nums_to_syms[ v ] = k

def symNumToSymbol( sym_num, fallback=... ):
    sym = m_grammar_nums_to_syms.get( sym_num, fallback )
    if sym is not ...:
        return sym
    raise Exception( "cannot get symbol for {}".format( sym_num ) )

def typeNumToName( type_num, fallback=... ):
    from fissix.pgen2 import token as pgen2_token
    name = pgen2_token.tok_name.get( type_num, fallback )
    if name is not ...:
        return name
    raise Exception( "cannot get type name for {}".format( type_num ) )


# --------------------------------------------------------------------------------------------------
class Treeverser( object ):
    """ takes a tree (or trees) of nodes so that they can be searched for
            bowler pattern to yield a list of matches """

    def __init__( self, trees ):
        if not isinstance( trees, list ):
            self.trees = [ trees ]
        else:
            self.trees = trees

    def gatherMatches( self, pattern_rgx ):
        """ return list of Match objects """
        if isinstance( pattern_rgx, str ):
            pattern_rgx = patcomp.compile_pattern( pattern_rgx )
        matches = []
        for node in self.getSubNodesD():
            results = {}
            if pattern_rgx.match( node, results ):
                match = Match( node )
                match.setResults( results )
                # print( "\nTreeverser-MATCH\n", match )
                matches.append( match )
        return matches

    def getSubNodesD( self ):
        nodes = []
        for tree in self.trees:
            nodes.extend( gatherSubNodesD( tree ) )
        return nodes


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Match( object ):
    """ holds node and the results captured within it """

    def __init__( self, node ):
        self.node = node
        self.results = {}

    def __repr__( self ):
        strs = MatchDumper( self )()
        return "\n".join( strs )

    def setResults( self, results ):
        self.results = results

    def get( self, key, fallback=... ):
        return self.results.get( key, fallback )

    def __getattr__( self, key ):
        try:
            return self.results[ key ]
        except KeyError as e:
            raise AttributeError( str( e ) )

    def __iter__( self ):
        return iter( self.results )


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class MatchDumper( object ):
    """ dumps a Match object for inspection / debug """

    def __init__( self, match ):
        self.match = match

    def __call__( self, output=None ):
        output = [] if output is None else output
        return self._dumpNode( self.match.node, output, results=self.match.results )

    def _dumpNode( self, node, output, results={}, indent=0, recurse=-1 ):
        indent_str = ".  "
        tab = indent_str * indent
        if isinstance( node, Leaf ):
            output.append(
                f"{ tab }[{ getNodeKind( node ) }] { repr( node.prefix ) } { repr( node.value ) }" )
        else:
            output.append(
                f"{ tab }[{ getNodeKind( node ) }] { repr( node.prefix ) }" )

        try:
            # indicate if the given node is one of our captured results
            find_node = node[ 0 ] if isinstance( node, list ) else node
            find_vals = [ val[ 0 ] if isinstance( val, list ) else val
                                                                for val in results.values() if val ]
            result_name = list( results.keys() )[ find_vals.index( find_node ) ]
            output[ -1 ] += f" ===> { result_name }"
        except ValueError:
            pass

        if node.children:
            if recurse:
                for child in node.children:
                    self._dumpNode( child, output, results=results,
                                                        indent=indent + 1, recurse=recurse - 1 )
            else:
                output.append( f"{ indent_str * (indent + 1) }..." )
        return output


# --------------------------------------------------------------------------------------------------
class AnonObj( dict ):
    """ Is it a dict? Is it an object? It's both. Supports dict style
            access by key (o[ attr_name ]) as well as access by attribute
            name (o.attr_name)
        NB inspired by javascript ;-) """

    # attr-style access
    def __getattr__( self, key ):
        try:
            return self[ key ]
        except KeyError as e:
            raise AttributeError( str( e ) )

    def __setattr__( self, key, value ):
        self[ key ] = value

    def __delattr__( self, key ):
        del self[ key ]


