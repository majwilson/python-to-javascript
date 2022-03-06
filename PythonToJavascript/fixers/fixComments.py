from helpers import gatherSubNodesD, getNodeKind
import re

white_space_rgx = re.compile( r"\s+", re.S )
hash_comment_rgx = re.compile( r"(\s*)(#)(.*)", re.S )
tquote_comment_rgx = re.compile( r'(.*?"""|\'\'\')(.*?)("""|\'\'\')', re.S )

def fixComments( nodes ):
    """ comments in triple-quotes are made into block comments (/* ... */);
        comments after # are made into inline comments (// ...) """
    for node in gatherSubNodesD( nodes ):
        if getNodeKind( node ) == "STRING":
            text = node.value
            tquote_m = tquote_comment_rgx.match( text )
            if tquote_m:
                if node.prev_sibling is None:
                    # Comment string (use jsdoc double-star prefix)
                    node.value = "/**" + tquote_m.group( 2 ) + "*/"
                else:
                    # Preserve other strings as template literals
                    node.value = "`" + tquote_m.group( 2 ) + "`"
        else:
            text = node.prefix if white_space_rgx.sub( "", node.prefix ) else ""
            hash_m = hash_comment_rgx.match( text )
            if hash_m:
                comm_body = hash_m.group( 3 )
                comm_lines = [
                    comm_line.replace( "#", "//" )
                    if ( comm_line.strip() and comm_line.strip()[ 0 ] == "#" ) else comm_line
                    for comm_line in comm_body.split( "\n" ) ]
                comm_body = "\n".join( comm_lines )
                node.prefix = hash_m.group( 1 ) + "//" + comm_body


