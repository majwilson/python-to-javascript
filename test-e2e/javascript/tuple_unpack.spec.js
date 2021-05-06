/* this file automatically generated from python */
const { expect } = require( "chai" );
const _pyjs = require( "./_pyjs" );

function getStrings() {
    return [ "world", "how", "are", "you" ];
}

describe( 'TupleUnpackTests', () => {

    it( 'test_TupleUnpack_01', () => {
        let [ a, b, c ] = [ 1, 2, 3 ];
        expect( a ).to.eql( 1 );
        expect( b ).to.eql( 2 );
        expect( c ).to.eql( 3 );

    } );
    it( 'test_TupleUnpack_02', () => {
        let [ a, b, c, d ] = getStrings();
        expect( a ).to.eql( "world" );
        expect( b ).to.eql( "how" );
        expect( c ).to.eql( "are" );
        expect( d ).to.eql( "you" );

    } );
    it( 'test_TupleUnpack_03', () => {
        let [ A, [ a, b, c, d ], B ] = [ "HELLO", getStrings(), "WORLD" ];
        expect( A ).to.eql( "HELLO" );
        expect( a ).to.eql( "world" );
        expect( b ).to.eql( "how" );
        expect( c ).to.eql( "are" );
        expect( d ).to.eql( "you" );
        expect( B ).to.eql( "WORLD" );


    } );
    } );
