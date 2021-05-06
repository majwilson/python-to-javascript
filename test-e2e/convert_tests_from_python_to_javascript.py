"""
    Running this file will convert tests files in tests-e2e/python to
        javascript versions in tests-e2e/javascript
"""
import sys
import os.path
sys.path.append( os.path.realpath( os.path.join( __file__, '../..' ) ) )
sys.path.append( os.path.realpath( os.path.join( __file__, '../../PythonToJavascript' ) ) )
sys.path.append( os.path.realpath( os.path.join( __file__, '../../PythonToJavascriptForTests' ) ) )

# ==================================================================================================
from PythonToJavascript import parseString
from PythonToJavascriptForTests.process_for_test import processTestModule

SOURCE_DIR = os.path.realpath( os.path.join( __file__, "../python/" ) )
DEST_DIR = os.path.realpath( os.path.join( __file__, "../javascript" ) )

_PYJS_NAME = "_pyjs.js"
_PYJS_PATH = os.path.realpath( os.path.join( __file__, "../../", _PYJS_NAME ) )

# ==================================================================================================
def copyPyjs():
    dest_path = os.path.join( DEST_DIR, _PYJS_NAME )
    if os.path.exists( dest_path ):
        os.remove( dest_path )
    open( dest_path, "w" ).write( open( _PYJS_PATH ).read() )

def getSourceTestPaths( source_dir ):
    test_paths = []
    for fname in sorted( os.listdir( source_dir ), key=lambda y: y.lower() ):
        if fname[ 0 ] == ".":
            continue        # ignore hidden files
        if fname.startswith( "__" ) and fname.endswith( "__" ):
            continue        # ignore special folders
        test_path = os.path.join( source_dir, fname )
        if os.path.isdir( test_path ):
            test_paths.extend( getSourceTestPaths( test_path ) )
        elif test_path.endswith( "_test.py" ):
            test_paths.append( test_path )
        else:
            pass            # ignore this file
    return test_paths


def deriveDestPath( source_dir, dest_dir, source_path ):
    if not source_dir.endswith( "/" ):
        source_dir += "/"
    if source_path.startswith( "/" ):
        source_rpath = source_path.replace( source_dir, "" )

    dest_path = os.path.join( dest_dir, source_rpath )
    dest_dir, dest_name = os.path.split( dest_path )
    dest_name = adjustDestFileName( dest_name )
    dest_path = os.path.join( dest_dir, dest_name )
    return dest_path


def convertTestFile( source_path, dest_path ):
    source = open( source_path ).read()
    parsed = parseString( source )

    processTestModule( parsed )

    out_code = str( parsed )
    out_code = adjustOutCode( out_code )

    dest_dir = os.path.dirname( dest_path )
    if not os.path.exists( dest_dir ):
        os.makedirs( dest_dir )

    if os.path.exists( dest_path ):
        os.remove( dest_path )
    open( dest_path, "w" ).write( out_code )


def adjustDestFileName( orig_name ):
    name, ext = os.path.splitext( orig_name )
    if name.endswith( "_test" ):
        name = name.replace( "_test", ".spec" )
    else:
        name = name + ".spec"
    return name + ".js"


def adjustOutCode( orig_code ):
    """ take raw output from conversion and adjust it so it will run """
    out_lines = []
    def out( l ): out_lines.append( l )

    out( f"/* this file automatically generated from python */" )
    out( 'const { expect } = require( "chai" );' )
    out( 'const _pyjs = require( "./_pyjs" );' )
    out( "" )

    for orig_line in orig_code.split( "\n" ):
        if "unittest" not in orig_line:
            out( orig_line )

    return "\n".join( out_lines )


def convertTestFiles( source_dir, dest_dir ):
    source_paths = getSourceTestPaths( source_dir )
    print( f"converting { len( source_paths ) } test files from { source_dir } to { dest_dir }" )
    for source_path in source_paths:
        dest_path = deriveDestPath( source_dir, dest_dir, source_path )
        convertTestFile( source_path, dest_path )


# ==================================================================================================
if __name__ == "__main__":
    copyPyjs()
    convertTestFiles( SOURCE_DIR, DEST_DIR )


