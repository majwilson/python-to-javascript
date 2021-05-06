from PythonToJavascript import parseString, dumpTree

def parseSource( source ):
    parsed = parseString( source.rstrip() )
    # dumpTree( parsed )
    return parsed

def nodesToString( nodes ):
    if not isinstance( nodes, list ):
        nodes = [ nodes ]
    return "".join( [ str( n ) for n in nodes ] ).strip()

def nodesToLines( nodes ):
    return nodesToString( nodes ).split( "\n" )

def dumpNodes( nodes, show_nums=False ):
    dumpLines( nodesToLines( nodes ), show_nums )

def dumpLines( lines, show_nums=False ):
    print( "\n>---" )
    if not isinstance( lines, list ):
        lines = lines.split( "\n" );
    for idx, l in enumerate( lines ):
        l = l.replace( '"', r'\"' )
        if show_nums:
            print( '%03d        "%s",' % ( idx, l ) )
        else:
            print( '        "%s",' % ( l ) )
    print( "---<" )


