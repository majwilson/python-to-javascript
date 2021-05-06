class ConverterChain:

    def __init__( self, gath_classes ):
        self.gath_classes = gath_classes

    def convertAll( self, nodes ):

        gath_dones = []
        for gath_class in self.gath_classes:
            gath = gath_class()
            matches = gath.gather( nodes )
            gath_dones.append( ( gath, matches ) )

        for gath, matches in gath_dones:
            gath.processAll( matches )

