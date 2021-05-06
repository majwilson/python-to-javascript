import adjust_sys_path
from utils import parseSource, nodesToString, nodesToLines, dumpNodes, dumpTree

from PythonToJavascriptForTests.converters_for_test import (
    UnittestClassToMochaDescribeConverter,
    PytestMethodToMochaItConverter,
    AssertToChaiExpectConverter
)

import unittest
import pytest

# ==================================================================================================
class Tests( unittest.TestCase ):

    # ----------------------------------------------------------------------------------------------
    def test_PytestClassToMochaDescribeProcess_01( self ):
        src = """
            class Tests( unittest.TestCase ):
                def test_func1( self ):
                    assert aval == 'bim'
                def test_func2( self ):
                   assert afunc()
                def notATestFunc( self ):
                    assert whatever == 'bam'
            class OtherClass( OtherBase ):
                pass
            class YetAnotherClass:
                pass
            """
        nodes = parseSource( src )
        cvtr = UnittestClassToMochaDescribeConverter( "unittest.TestCase TestCase" )
        matches = cvtr.gather( nodes )
        cvtr.processAll( matches )
        # dumpNodes( nodes )
        assert nodesToLines( nodes ) == [
            "describe( 'Tests', () => {",
            "    def test_func1( self ):",
            "        assert aval == 'bim'",
            "    def test_func2( self ):",
            "       assert afunc()",
            "    def notATestFunc( self ):",
            "        assert whatever == 'bam'",
            "} );",
            " class OtherClass extends OtherBase {",
            "    pass",
            "}",
            " class YetAnotherClass {",
            "    pass",
            "}",
        ]

    # ----------------------------------------------------------------------------------------------
    def test_FunctionToMochaItProcess_01( self ):
        src = """
            class Tests( unittest.TestCase ):
                def test_func1( self ):
                    assert aval == 'bim'
                def test_func2( self ):
                   assert afunc()
                def notATestFunc( self ):
                    assert whatever == 'bam'
            """
        nodes = parseSource( src )
        matches = PytestMethodToMochaItConverter( in_class=True ).gather( nodes )
        PytestMethodToMochaItConverter( in_class=True ).processAll( matches )
        # dumpNodes( nodes )
        assert nodesToLines( nodes ) == [
            "class Tests( unittest.TestCase ):",
            "    it( 'test_func1', () => {",
            "        assert aval == 'bim'",
            "        } );",
            "    it( 'test_func2', () => {",
            "       assert afunc()",
            "        } );",
            "        notATestFunc() {",
            "        assert whatever == 'bam'",
            "    }",
        ]

    # ----------------------------------------------------------------------------------------------
    def test_AssertToChaiExpectGather_01( self ):
        src = """
            def test_func1( self ):
                assert aval == 'bim'
        """
        nodes = parseSource( src )
        match = AssertToChaiExpectConverter().gather( nodes )[ 0 ]
        assert match.node.toString() == "assert aval == 'bim'"
        assert match.comp_op.toString() == "=="
        assert "truthy" not in match

    def test_AssertToChaiExpectGather_02( self ):
        src = """
            def test_func1( self ):
                assert aval != 'bim'
        """
        nodes = parseSource( src )
        match = AssertToChaiExpectConverter().gather( nodes )[ 0 ]
        assert match.node.toString() == "assert aval != 'bim'"
        assert match.comp_op.toString() == "!="
        assert "truthy" not in match

    def test_AssertToChaiExpectGather_03( self ):
        src = """
            def test_func1( self ):
                assert aval
        """
        nodes = parseSource( src )
        match = AssertToChaiExpectConverter().gather( nodes )[ 0 ]
        assert match.node.toString() == "assert aval"
        assert match.truthy.toString() == "aval"
        assert "comp_op" not in match

    def test_AssertToChaiExpectGather_04( self ):
        src = """
            def test_func1( self ):
                assert not aval
        """
        nodes = parseSource( src )
        match = AssertToChaiExpectConverter().gather( nodes )[ 0 ]
        assert match.node.toString() == "assert not aval"
        assert match.truthy.toString() == "aval"
        assert match.not_word.toString() == "not"
        assert "comp_op" not in match


    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def test_AssertToChaiExpectProcess_01( self ):
        src = """
            def test_func1( self ):
                assert aval == 'bim'
        """
        nodes = parseSource( src )
        cvtr = AssertToChaiExpectConverter()
        matches = cvtr.gather( nodes )
        cvtr.processOne( matches[ 0 ] )
        # dumpNodes( nodes )
        assert nodesToLines( nodes ) == [
            "def test_func1( self ):",
            "    expect( aval ).to.eql( 'bim' )",
        ]

    def test_AssertToChaiExpectProcess_02( self ):
        src = """
            def test_func1( self ):
                assert aval != 'bim'
        """
        nodes = parseSource( src )
        cvtr = AssertToChaiExpectConverter()
        matches = cvtr.gather( nodes )
        cvtr.processOne( matches[ 0 ] )
        # dumpNodes( nodes )
        assert nodesToLines( nodes ) == [
            "def test_func1( self ):",
            "    expect( aval ).not.to.eql( 'bim' )",
        ]

    def test_AssertToChaiExpectProcess_03( self ):
        src = """
            def test_func1( self ):
                assert aval
        """
        nodes = parseSource( src )
        cvtr = AssertToChaiExpectConverter()
        matches = cvtr.gather( nodes )
        cvtr.processOne( matches[ 0 ] )
        # dumpNodes( nodes )
        assert nodesToLines( nodes ) == [
            "def test_func1( self ):",
            "    expect( aval ).to.be.ok",
        ]

    def test_AssertToChaiExpectProcess_04( self ):
        src = """
            def test_func1( self ):
                assert not aval
        """
        nodes = parseSource( src )
        cvtr = AssertToChaiExpectConverter()
        matches = cvtr.gather( nodes )
        cvtr.processOne( matches[ 0 ] )
        # dumpNodes( nodes )
        assert nodesToLines( nodes ) == [
            "def test_func1( self ):",
            "    expect( aval ).not.to.be.ok",
        ]

    def test_AssertToChaiExpectProcess_05( self ):
        src = """
            def test_func1( self ):
                assert aval > 100
        """
        nodes = parseSource( src )
        cvtr = AssertToChaiExpectConverter()
        matches = cvtr.gather( nodes )
        cvtr.processOne( matches[ 0 ] )
        # dumpNodes( nodes )
        assert nodesToLines( nodes ) == [
            "def test_func1( self ):",
            "    expect( aval > 100 ).to.be.ok",
        ]

    def test_AssertToChaiExpectProcess_06( self ):
        src = """
        class Tests( unittest.TestCase ):
            def test_getAttr( self ):
                try:
                    getattr( obj, 'bom' )
                except:
                    excepted = True
                assert excepted
        """
        nodes = parseSource( src )
        cvtr = AssertToChaiExpectConverter()
        matches = cvtr.gather( nodes )
        cvtr.processOne( matches[ 0 ] )
        # dumpNodes( nodes )
        assert nodesToLines( nodes ) == [
            "class Tests( unittest.TestCase ):",
            "    def test_getAttr( self ):",
            "        try:",
            "            getattr( obj, 'bom' )",
            "        except:",
            "            excepted = True",
            "        expect( excepted ).to.be.ok",
        ]

