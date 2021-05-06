/* this file automatically generated from python */
const { expect } = require( "chai" );
const _pyjs = require( "./_pyjs" );

function getStrings() {
    return [ "world", "how", "are", "you" ];
}

describe( 'StringInterpolationTests', () => {

    it( 'test_StringInterpolation_01', () => {
        let r = _pyjs.stringInterpolate( "hello %s", [ "world" ] );
        expect( r ).to.eql( "hello world" );

    } );
    it( 'test_StringInterpolation_02', () => {
        let s = "hello %s %s %s %s";
        let r = _pyjs.stringInterpolate( s, [ "world", "how", "are", "you" ] );
        expect( r ).to.eql( "hello world how are you" );

    } );
    it( 'test_StringInterpolation_03', () => {
        let s = "hello %s %s %s %s";
        let r = _pyjs.stringInterpolate( s, getStrings() );
        expect( r ).to.eql( "hello world how are you" );



    } );
    } );
