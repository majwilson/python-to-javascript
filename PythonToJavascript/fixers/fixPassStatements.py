from helpers import getNodeKind, getNodeIndex, gatherSubNodesD, makeLeaf

def fixPassStatements( nodes ):
    for node in gatherSubNodesD( nodes ):
        if getNodeKind( node ) == "NAME" and node.value == "pass":
            pass_idx = getNodeIndex( node )
            after_node = node.parent.children[ pass_idx + 1 ]
            if getNodeKind( after_node ) == "SEMI":
                after_node.remove()
            node.parent.insert_child( pass_idx, makeLeaf( "PYJS", "/*", node.prefix ) )
            node.prefix = " "
            node.parent.insert_child( pass_idx + 2, makeLeaf( "PYJS", "*/", ' ' ) )

