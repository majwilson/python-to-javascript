// functions used in code converted from Python by PythonToJavascript

const isDef = ( obj ) => {
    return obj !== undefined;
};

const getAttr = ( obj, name, fallback ) => {
    var attr = obj[ name ];
    if( isDef( attr ) ) {
        return attr;
    }
    if( isDef( fallback ) ) {
        return fallback;
    }
    throw new Error( `cannot get attr '${ name }' from ${ obj.toString() }` );
};

const setAttr = ( obj, name, val ) => {
    obj[ name ] = val;
};

const hasAttr = ( obj, name, val ) => {
    return isDef( obj[ name ] );
};

const isInstance = ( obj, klass ) => {
    try {
        return obj instanceof klass;
    } catch( e ) {
        try {
            return klass.filter( c => obj instanceof c ).length > 0;
        } catch( ee ) {
            throw new TypeError( `class or list of classes expected not ${ klass }` );
        }
    }
};

const stringInterpolate = ( main_str, inter_strs ) => {
    return inter_strs.reduce( ( a, c ) => a.replace( /%(s|i|r)?/, c.toString () ), main_str );
};

const listZip = function( ...lists ) {
    return lists[ 0 ].map( ( _, i ) => lists.map( l => isDef( l[ i ] ) ? l[ i ] : null ) );
};

Object.assign( exports, {
    isDef,
    getAttr,
    setAttr,
    hasAttr,
    isInstance,
    stringInterpolate,
    listZip,
} );