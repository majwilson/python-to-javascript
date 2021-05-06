from helpers import gatherSubNodesD, getNodeKind, getOutNodes

class Converter:
    def __init__( self ):
        pass

    def gather( self, node ):
        raise NotImplementedError( self.__class__.__name__ )

    def processOne( self, match ):
        raise NotImplementedError( self.__class__.__name__ )

    def processAll( self, matches ):
        for match in matches:
            self.processOne( match )

    def findNodeForwardIndex( self, parent, kind, fallback=... ):
        try:
            node = self.findNodeForward( parent, kind )
            return parent.children.index( node )
        except Exception:
            if fallback is not ...:
                return fallback
            raise

    def findNodeForward( self, parent, kind, fallback=... ):
        nodes = gatherSubNodesD( parent )
        for node in nodes:
            if getNodeKind( node ) == kind:
                return node
        if fallback is not ...:
            return fallback
        raise Exception( "cannot find {}".format( kind ) )


    def findNodeReverseIndex( self, parent, kind, fallback=... ):
        try:
            node = self.findNodeReverse( parent, kind )
            return parent.children.index( node )
        except Exception:
            if fallback is not ...:
                return fallback
            raise


    def findNodeReverse( self, parent, kind, fallback=... ):
        nodes = list( reversed( parent.children ) )
        for node in nodes:
            if getNodeKind( node ) == kind:
                return node
        if fallback is not ...:
            return fallback
        raise Exception( "cannot find {}".format( kind ) )


    def calcIndent( self, node ):
        count = 0
        for out_node in getOutNodes( node ):
            if getNodeKind( out_node ) == "suite":
                count += 1
        return "    " * count



