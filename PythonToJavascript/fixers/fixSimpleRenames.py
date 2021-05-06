# simple name substitutions - only applied to NAME nodes, exact matches only

from helpers import getNodeKind, gatherSubNodesD

m_fix_simple_names = {
    "False": "false",
    "None": "null",
    "True": "true",
    "__init__" : "constructor",
    "__repr__" : "toString",
    "append": "push",
    "del" : "delete",
    "endswith": "endsWith",
    "getattr": "_pyjs.getAttr",
    "hasattr": "_pyjs.hasAttr",
    "isinstance": "_pyjs.isInstance",
    "print": "console.log",
    "raise": "throw",
    "setattr": "_pyjs.setAttr",
    "startswith": "startsWith",
    "zip": "_pyjs.listZip",
}

def fixSimpleRenames( func_node ):
    for node in gatherSubNodesD( func_node ):
        if getNodeKind( node ) == "NAME":
            if node.value in m_fix_simple_names:
                node.value = m_fix_simple_names[ node.value ]

