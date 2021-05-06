import unittest

class TObj:
    def __init__( self ):
        self.bim= 123
        self.bam= 'hello'

def makeTObj():
    # in JS this needs to read:
    # return new TObj();
    return TObj()


class AttrTests( unittest.TestCase ):

    def test_getAttr( self ):
        obj = makeTObj()
        assert getattr( obj, 'bim' ) == 123
        assert getattr( obj, 'bam' ) == 'hello'
        assert getattr( obj, 'bom', 0 ) == 0

        excepted = False
        try:
            getattr( obj, 'bom' )
        except:
            excepted = True
        assert excepted

    def test_setAttr( self ):
        obj = makeTObj()
        setattr( obj, 'bim', 100 )
        assert getattr( obj, 'bim' ) == 100
        setattr( obj, 'bom', 'bom' )
        assert getattr( obj, 'bom' ) == 'bom'

    def test_hasAttr( self ):
        obj = makeTObj()
        assert hasattr( obj, 'bim' ) == True
        assert hasattr( obj, 'bam' ) == True
        assert hasattr( obj, 'bom' ) == False

