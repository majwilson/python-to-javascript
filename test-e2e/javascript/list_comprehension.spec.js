/* this file automatically generated from python */
const { expect } = require( "chai" );
const _pyjs = require( "./_pyjs" );

describe( 'ListComprehensionTests', () => {

    it( 'test_ListComprehension_01', () => {
        let vz = [ 1, 2, 3, 4 ];
        let l = vz.map( v => v * 3 );
        expect( l ).to.eql( [ 3, 6, 9, 12 ] );

    } );
    it( 'test_ListComprehension_02', () => {
        let vz = [ 1, 2, 3, 4 ];
        let l = vz.filter( v => 10 / v  > 4 ).map( v => v * 3 );
        expect( l ).to.eql( [ 3, 6 ] );

    } );
    it( 'test_ListComprehension_03', () => {
        let kvz = [ [ 10, 1 ], [ 20, 2 ], [ 30, 3 ] ];
        let l = kvz.filter( ( [ k, v ] ) => v * 10 > 15 ).map( ( [ k, v ] ) => k * 5 + v );
        expect( l ).to.eql( [ 102, 153 ] );

    } );
    it( 'test_ListComprehension_04', () => {
        let kvz = [ [ 10, 1 ], [ 20, 2 ], [ 30, 3 ] ];
        let l = kvz.filter( kv => kv[ 1 ] * 10 > 15 ).map( kv => kv[ 0 ] * 5 + kv[ 1 ] );
        expect( l ).to.eql( [ 102, 153 ] );




    } );
    } );
