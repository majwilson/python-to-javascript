from Converter import Converter
from helpers import Treeverser, AnonObj, makeLeaf, getNodeIndex, getNodeKind, makeTrailer
from fissix.pytree import Node, Leaf


class KeyWordCallConverter( Converter ):
    """
       x = func( a=122, b="hello" ) => x = func( { a: 122, b: "hello" } )
     """

    PATTERN = """
        arglist < args=any* >
    """
    def gather( self, node ):
        """ return list of AnonObjs containing the info we need """
        tv = Treeverser( node )
        matches = tv.gatherMatches( self.PATTERN )
        infos = []
        for match in matches:
            info = AnonObj( node=match.node )

            info.args = []
            for match_arg in match.args:
                arg_info = AnonObj( node=match_arg )
                info.args.append( arg_info )

            infos.append( info )
        return infos

    def processOne( self, match ):
        first_kw_idx = None
        for arg_idx, arg in enumerate( match.args ):
            if not isinstance( arg.node, Leaf ):
                for n in arg.node.children:
                    if getNodeKind( n ) == "COMMA":
                        continue
                    if getNodeKind( n ) == "EQUAL":
                        first_kw_idx = arg_idx
                        break
            if first_kw_idx is not None:
                break

        if first_kw_idx is not None:
            for kw_arg_info in match.args[ first_kw_idx : ]:
                kw_arg_info.node.remove()

            obj_node = makeTrailer()
            match.node.append_child( obj_node )
            obj_node.append_child( makeLeaf( "LBRACE", "{", " " ) )

            for kw_arg_info in match.args[ first_kw_idx : ]:

                kw_arg_node = kw_arg_info.node
                if getNodeKind( kw_arg_node ) == "COMMA":
                    continue
                arg_name = eq_sym  = None
                for arg_sub_node in kw_arg_node.children[ : ]:
                    if getNodeKind( arg_sub_node ) == "NAME" and arg_name is None:
                        arg_name = str( arg_sub_node )
                        arg_sub_node.remove()
                    elif getNodeKind( arg_sub_node ) == "EQUAL":
                        eq_sym = str( arg_sub_node )
                        arg_sub_node.remove()


                if not ( arg_name and eq_sym ):
                    raise Exception( "cannot get arg name & '=' from %r" % kw_arg_node.toString() )

                obj_node.append_child( makeLeaf( "PYJS", arg_name, "" ) )
                obj_node.append_child( makeLeaf( "COLON", ":", "" ) )
                if kw_arg_node.children:
                    kw_arg_node.children[ 0 ].prefix = " "
                    for n in kw_arg_node.children[ : ]:
                        n.remove()
                        obj_node.append_child( n );
                    if kw_arg_info != match.args[ -1 ]:
                        obj_node.append_child( makeLeaf( "COMMA", ",", "" ) )

            obj_node.append_child( makeLeaf( "RBRACE", "}", " " ) )
