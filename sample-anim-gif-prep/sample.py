import BaseClass
from AModule import aFunc, bFunc

class AClass( BaseClass.ABaseClass ):

    def __init__( self, val1, val2 ):
        super( ABaseClass, self ).__init__( val1 )
        self.val2 = val2

    def meth1( self, aval ):
        val = self.val1 * self.val2 + aval
        return super( ABaseClass, self ).meth1( val )

    def meth2( self, astr ):
        return func( astr, self.val1, self.val2 );


def func( a, b, c ):
    x = aFunc( a, b )
    return bFunc( c, x )









