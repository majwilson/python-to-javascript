/* this file automatically generated from python */
const { expect } = require( "chai" );
const _pyjs = require( "./_pyjs" );

function getStrings() {
    return [ "world", "how", "are", "you" ];
}

describe( 'ListSliceTests', () => {

    it( 'test_ListSlice_01', () => {
        let l = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ];
        expect( l.slice( 3, 8 ) ).to.eql( [ 3, 4, 5, 6, 7 ] );

    } );
    it( 'test_ListSlice_02', () => {
        let l = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ];
        expect( l.slice( 3 ) ).to.eql( [ 3, 4, 5, 6, 7, 8, 9 ] );

    } );
    it( 'test_ListSlice_03', () => {
        let l = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ];
        expect( l.slice( 0, 8 ) ).to.eql( [ 0, 1, 2, 3, 4, 5, 6, 7 ] );

    } );
    it( 'test_ListSlice_04', () => {
        let l = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ];
        expect( l.slice() ).to.eql( [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ] );

    } );
    it( 'test_ListSlice_05', () => {
        let l = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ];
        expect( l.slice( 2, -3 ) ).to.eql( [ 2, 3, 4, 5, 6 ] );



    } );
    } );
