const BaseClass = require( './BaseClass' );
const { aFunc, bFunc } = require( './AModule' );

class AClass extends BaseClass.ABaseClass {

    constructor( val1, val2 ) {
        super( val1 );
        this.val2 = val2;
    }

    meth1( aval ) {
        let val = this.val1 * this.val2 + aval;
        return super.meth1( val );
    }

    meth2( astr ) {
        return func( astr, this.val1, this.val2 );
    }
}

function func( a, b, c ) {
    let x = aFunc( a, b );
    return bFunc( c, x );
}







