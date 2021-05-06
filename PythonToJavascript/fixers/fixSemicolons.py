from helpers import Treeverser, getNodeKind, makeLeaf

def fixSemicolons( nodes ):
    STMT_PATTERN = """
        simple_stmt < stmt=any newl='\\n' >
    """

    tv = Treeverser( nodes )
    matches = tv.gatherMatches( STMT_PATTERN )
    infos = []
    for match in matches:
        if getNodeKind( match.stmt ) != "STRING":   # stmt is not a comment
            par_node = match.newl.parent
            newl_idx = par_node.children.index( match.newl )
            if getNodeKind( par_node.children[ newl_idx - 1 ] ) != "SEMI":
                par_node.insert_child( newl_idx, makeLeaf( "SEMI", ";", '' ) )

    return infos

