/* this file automatically generated from python */
const { expect } = require( "chai" );
const _pyjs = require( "./_pyjs" );

describe( 'DictComprehensionTests', () => {

    it( 'test_dictComprehension_01', () => {
        let kvz = [ [ 'a', 1 ], [ 'b', 2 ], [ 'c', 3 ] ];
        let d = kvz.reduce( ( __map, [ k, v ] ) => ( { ...__map, [ k ]: v * 2 } ), {} );
        expect( d ).to.eql( { 'a': 2, 'b': 4, 'c': 6 } );

    } );
    it( 'test_dictComprehension_02', () => {
        let kvz = [ [ 'a', 1 ], [ 'b', 2 ], [ 'c', 3 ] ];
        let d = kvz.filter( ( [ k, v ] ) => v * 10 > 15 ).reduce( ( __map, [ k, v ] ) => ( { ...__map, [ k ]: v * 2 } ), {} );
        expect( d ).to.eql( { 'b': 4, 'c': 6 } );

    } );
    it( 'test_dictComprehension_03', () => {
        let kvz = [ [ 'a', 1 ], [ 'b', 2 ], [ 'c', 3 ] ];
        let d = kvz.filter( kv => kv[ 1 ] * 10 > 15 ).reduce( ( __map, kv ) => ( { ...__map, [ kv[ 0 ] ]: kv[ 1 ] * 2 } ), {} );
        expect( d ).to.eql( { 'b': 4, 'c': 6 } );


    } );
    } );
