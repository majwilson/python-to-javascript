import sys
import os.path
sys.path.append( os.path.realpath( os.path.join( __file__, '../..' ) ) )
sys.path.append( os.path.realpath( os.path.join( __file__, '../../PythonToJavascript' ) ) )
print( "SYSPATH", sys.path )

from PythonToJavascript import parseString
from process_for_test import processTestModule

import os

import click
@click.command()
@click.option('--in_file', help='path to test file to convert.')
@click.option('--out_dir', help='path to directory containing converted test files.')

# --------------------------------------------------------------------------------------------------
def main( in_file, out_dir ):
    print( in_file, out_dir )

    in_folder, in_path = os.path.split( in_file )
    in_path = os.path.splitext( in_path )[ 0 ] + ".js"

    if existsFileInDirectory( in_folder, out_dir, in_path ):
        raise Exception( "dest file already exists - please remove it first!" )
    source = open( in_file ).read()
    parsed = parseString( source )

    processTestModule( parsed )

    writeFileInDirectory( in_folder, out_dir, in_path, str( parsed ) )

# --------------------------------------------------------------------------------------------------
def writeFileInDirectory( source_dir, dest_dir, source_path, dest_data ):
    dest_path = deriveDestPath( source_dir, dest_dir, source_path )
    dest_dir = os.path.dirname( dest_path )
    if not os.path.exists( dest_dir ):
        os.makedirs( dest_dir )
    open( dest_path, "w" ).write( dest_data )


def existsFileInDirectory( source_dir, dest_dir, source_path ):
    dest_path = deriveDestPath( source_dir, dest_dir, source_path )
    return os.path.exists( dest_path )


def deriveDestPath( source_dir, dest_dir, source_path ):
    if not os.path.exists( source_dir ):
        raise Exception( "invalid source root {}".format( source_dir ) )
    if not os.path.exists( dest_dir ):
        raise Exception( "invalid dest root {}".format( dest_dir ) )

    if not source_dir.endswith( "/" ):
        source_dir += "/"
    if not source_path.startswith( "/" ):
        source_rpath = source_path
    else:
        if not source_path.startswith( source_dir ):
            raise Exception( "invalid source path" )
        source_rpath = source_path.replace( source_dir, "" )

    dest_path = os.path.join( dest_dir, source_rpath )
    return dest_path


# --------------------------------------------------------------------------------------------------
main()
