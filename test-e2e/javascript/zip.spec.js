/* this file automatically generated from python */
const { expect } = require( "chai" );
const _pyjs = require( "./_pyjs" );

describe( 'ZipTests', () => {

    it( 'test_zip', () => {
        let l1 = [ 'a', 'b', 'c' ];
        let l2 = [ 1, 2, 3 ];
        let l3 = [ true, false, true ];
        let l4 = [];
        for( let v of _pyjs.listZip( l1, l2, l3 ) ) {
            l4.push( v );
        }
expect(        l4 ).to.eql( [ [ 'a', 1, true ], [ 'b', 2, false ], [ 'c', 3, true ] ] );

    } );
    it( 'test_zip_differing_lengths', () => {
        let l1 = [ 'a', 'b', 'c' ];
        let l2 = [ 1, 2, 3, 4, 5, 6 ];
        let l3 = [ true, false, true ];
        let l4 = [];
        for( let v of _pyjs.listZip( l1, l2, l3 ) ) {
            l4.push( v );
        }
expect(        l4 ).to.eql( [ [ 'a', 1, true ], [ 'b', 2, false ], [ 'c', 3, true ] ] );



    } );
    } );
