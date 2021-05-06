from PythonToJavascript.converters import (
    AssignmentConverter,
    BoolOpsConverter,
    # ClassConverter,
    ComparisonConverter,
    DecoratorConverter,
    DictComprehensionConverter,
    ExceptionConverter,
    ForLoopConverter,
    FunctionConverter,
    IfElifElseConverter,
    ImportFromConverter,
    ImportNameConverter,
    KeyWordCallConverter,
    ListComprehensionConverter,
    ListSliceConverter,
    NegateConverter,
    SelfConverter,
    StringInterpolationConverter,
    SuperConverter,
    TryExceptConverter,
    TupleConverter,
    WhileLoopConverter,
)
from PythonToJavascript.ConverterChain import ConverterChain
from fixers import (
    fixComments,
    fixIndents,
    fixPassStatements,
    fixSemicolons,
    fixSimpleRenames,
)
from helpers import AnonObj

from PythonToJavascriptForTests.converters_for_test import (
    UnittestClassToMochaDescribeConverter,
    PytestMethodToMochaItConverter,
    AssertToChaiExpectConverter
)

# --------------------------------------------------------------------------------------------------
def processTestModule( module_nodes ):

    infos = AnonObj( class_names=[], func_names=[] )

    # convert asserts before anything else
    assert_cvtr = AssertToChaiExpectConverter()
    assert_cvtr.processAll( assert_cvtr.gather( module_nodes ) )

    ConverterChain( [ ImportNameConverter, ImportFromConverter ] ).convertAll( module_nodes )

    class_gath = UnittestClassToMochaDescribeConverter( "unittest.TestCase" )
    class_matches = class_gath.gather( module_nodes )

    if not class_matches:
        print( "NO CLASSES" )
    else:
        for class_match in class_matches:
            print( "\nCLASS", class_match.name )
            class_gath.processOne( class_match )
            fixComments( class_match.suite )

            func_matches = PytestMethodToMochaItConverter( in_class=True ).gather( class_match.suite )
            for func_match in func_matches:
                print( "----METHOD", func_match.name )
                processTestFunction( func_match.node, in_class=True )
            infos.class_names.append( class_match.name.toString() )

    func_matches = PytestMethodToMochaItConverter().gather( module_nodes )
    for func_match in func_matches:
        print( "FUNCTION ", func_match.name )
        processTestFunction( func_match.node )
        infos.func_names.append( func_match.name.toString() )

    fixComments( module_nodes )
    fixPassStatements( module_nodes )
    fixSimpleRenames( module_nodes )

    fixSemicolons( module_nodes )

    return infos


# --------------------------------------------------------------------------------------------------
def processTestFunction( func_node, in_class=False ):
    """ process all aspects of a function including the function itself """

    fixIndents( func_node )

    func_gath = PytestMethodToMochaItConverter( in_class )
    func_matches = func_gath.gather( func_node )
    func_gath.processAll( func_matches )

    gath_classes = [
        AssignmentConverter,
        BoolOpsConverter,
        ComparisonConverter,
        DecoratorConverter,
        DictComprehensionConverter,
        ExceptionConverter,
        ForLoopConverter,
        IfElifElseConverter,
        KeyWordCallConverter,
        ListComprehensionConverter,
        ListSliceConverter,
        NegateConverter,
        SelfConverter,
        StringInterpolationConverter,
        SuperConverter,
        TryExceptConverter,
        TupleConverter,
        WhileLoopConverter,
    ]

    ConverterChain( gath_classes ).convertAll( func_node )

    fixComments( func_node )
    fixPassStatements( func_node )
    fixSemicolons( func_node )
    fixSimpleRenames( func_node )

