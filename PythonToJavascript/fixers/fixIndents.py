from helpers import gatherSubNodesD, getNodeKind
import re

def fixIndents( nodes ):
    prefix = ""
    for sub_node in gatherSubNodesD( nodes ):
        if getNodeKind( sub_node ) == "DEDENT":
            space_rgx = re.compile( r"(.*?)( +)(\n*)$", re.S )
            m = space_rgx.match( sub_node.prefix )
            if m:
                prefix = m.group( 2 )
                sub_node.prefix = m.group( 1 ) + m.group( 3 )
        elif getNodeKind( sub_node ) == "NAME":
            if prefix:
                sub_node.prefix = " " * len( prefix )
                prefix = ""

