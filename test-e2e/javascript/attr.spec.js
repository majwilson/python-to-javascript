/* this file automatically generated from python */
const { expect } = require( "chai" );
const _pyjs = require( "./_pyjs" );

 class TObj {
        constructor() {
        this.bim= 123;
        this.bam= 'hello';
    }

}
function makeTObj() {
    // in JS this needs to read:
    return new TObj();
    return TObj();
}


describe( 'AttrTests', () => {

    it( 'test_getAttr', () => {
        let obj = makeTObj();
        expect( _pyjs.getAttr( obj, 'bim' ) ).to.eql( 123 );
        expect( _pyjs.getAttr( obj, 'bam' ) ).to.eql( 'hello' );
        expect( _pyjs.getAttr( obj, 'bom', 0 ) ).to.eql( 0 );

        let excepted = false;
        try {
            _pyjs.getAttr( obj, 'bom' );
        } catch( e ) {
            excepted = true;
        }
expect(        excepted ).to.be.ok;

    } );
    it( 'test_setAttr', () => {
        let obj = makeTObj();
        _pyjs.setAttr( obj, 'bim', 100 );
        expect( _pyjs.getAttr( obj, 'bim' ) ).to.eql( 100 );
        _pyjs.setAttr( obj, 'bom', 'bom' );
        expect( _pyjs.getAttr( obj, 'bom' ) ).to.eql( 'bom' );

    } );
    it( 'test_hasAttr', () => {
        let obj = makeTObj();
        expect( _pyjs.hasAttr( obj, 'bim' ) ).to.eql( true );
        expect( _pyjs.hasAttr( obj, 'bam' ) ).to.eql( true );
        expect( _pyjs.hasAttr( obj, 'bom' ) ).to.eql( false );



    } );
    } );
