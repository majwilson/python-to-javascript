# calver 0Y.0M.0D format
__version__ = '21.05.05'

# --------------------------------------------------------------------------------------------------
# add a single token - 'PYJS' - for us to use when we're creating new
#    pytree Leafs that contain javascript for which there's no python
#    equivalent (eg '=>')

from fissix.pgen2 import token as pgen2_token

pgen2_token.PYJS = pgen2_token.ERRORTOKEN + 1
pgen2_token.N_TOKENS += 1

# now rebuild the tok_name lookup
pgen2_token.tok_name = {}
for _name in dir( pgen2_token ):
    _value = getattr( pgen2_token, _name )
    if type( _value ) is type( 0 ):
        pgen2_token.tok_name[ _value ] = _name

# dump if you need to check
# for k in sorted( pgen2_token.tok_name.keys() ):
#     print( "PG TOKEN", k, pgen2_token.tok_name[ k ] )

# bowler needs to know about our changes
import bowler
bowler.helpers.tok_name = pgen2_token.tok_name


# --------------------------------------------------------------------------------------------------
# give Node and Leaf a toString method
from fissix.pytree import Node, Leaf
def toString( self ):
    return str( self ).strip()
Node.toString = toString
Leaf.toString = toString


# --------------------------------------------------------------------------------------------------
# functions for the outside world to call
from helpers import parseString
from process import processModule
from bowler.helpers import print_tree as dumpTree