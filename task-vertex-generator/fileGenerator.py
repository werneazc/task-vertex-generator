#coding=UTF8

import os
import shutil

#This function build a basic structure of a task vertex class.
#The parameters are:
#   path: string which contains the path where the generated file is saved
#   filename: string of name of the generated file including the file extension
#   classname: string with name of the generated class
#   inputParam: list of all input parameters
#       The list has the following structure: [int,["",""], ...[""]]
#           -int: number of template parameters
#           -["",""]: name/type of template member and initial value
#           -[""]: data type of standard member
#  outputParam: list of all input parameters
#       The list has the following structure: [int,["",""], ...[""]]
#           -int: number of template parameters
#           -["",""]: name/type of template member and initial value
#           -[""]: data type of standard member
#  format: True format the generated file at the end with clang-format.
#          The program should be available on the PC, else an exception is generated.
#The function has no return. The file is saved to: path + filename.
def fileBuilder(path="", filename="", classname="", inputParam=[], outputParam=[], format=False ):
    "builds a standard vertex file"
    
    from doxygenDescriptionGen import fileDescriptionGen

    if( (len(outputParam) <= 0) or (len(inputParam) <=0)):
        raise ValueError("wrong number of input and/or output variables (> 0)") 

    #in a value description the first element shows the number of template parameters
    #the following number between element 1 and the count value of template parameters are
    #for template description
    numOfTparamInput = inputParam[0]
    numOfTparamOutput = outputParam[0]

    numOfIns = len(inputParam) - 1
    numOfOuts = len(outputParam) - 1

    #name gen definitions
    inputStrList = ["_inputOne", "_inputTwo", "_inputThree", "_inputFour", 
                    "_inputSix", "_inputSeven","_inputEight", "_inputNine",
                    "_inputTen", "_inputEleven", "_inputTwelve", "_inputThirteen",
                    "_inputFourteen", "_inputFifeteen", "_inputSixteen", "_inputSeventeen",
                    "_inputEighteen", "_inputNineteen", "_inputTwenty"]
    returnStrList = ["_returnOne", "_returnTwo", "_returnThree", "_returnFour", 
                     "_returnSix", "_returnSeven","_returnEight", "_returnNine",
                     "_returnTen", "_returnEleven", "_returnTwelve", "_returnThirteen",
                     "_returnFourteen", "_returnFifeteen", "_returnSixteen", "_returnSeventeen",
                     "_returnEighteen", "_returnNineteen", "_returnTwenty"]
    inputSideStr = ["0", "1" ]

    #file description
    file = fileDescriptionGen(filename)

    #declarations
    decl = declGen()

    #constructers: tParam stores template parameters
    tParam=[]
    for it in range (1, numOfIns + 1):
        tParam.extend([inputParam[it][0]])
    constructers = constructorGen(classname, tParam, numOfIns, inputStrList, inputSideStr)
    
    #notification method: tParam saves type of output for number of bytes send
    tParam=[]
    for it in range(1, numOfOuts + 1 ):
        tParam.extend([outputParam[it][0]])
    notify = notificationGen()

    #execute method: tParam saves type of output for cast
    execute = executeGen()

    #getResults method: tParam saves type of output for tuple definition
    getResults = resultGen(numOfOuts, returnStrList, tParam)

    #Observer implementation
    #observer = observerGen()

    #helper function implementation
    functions = scModuleFuncGen(classname)

    #member implemenration
    inputTypes=[]
    for it in range (1, numOfIns + 1):
        inputTypes.extend([inputParam[it][0]])
    outputTypes = []
    for it in range(1, numOfOuts + 1 ):
        outputTypes.extend([outputParam[it][0]])
    member = memberGen(numOfIns, inputStrList, inputTypes, numOfOuts, returnStrList, outputTypes, inputSideStr)


    #class description
    #body = constructers + notify + execute + getResults + observer + functions + member
    body = constructers + notify + execute + getResults + functions + member

    tParam=[]
    if (numOfTparamInput != 0):
        for it in range (1,numOfTparamInput + 1):
            tParam.extend([inputParam[it]])
    if (numOfTparamOutput != 0):
        for it in range (1,numOfTparamOutput + 1):
            tParam.extend([outputParam[it]])
    classDesc = classGen(classname, tParam, body)


    #file description
    body = decl + classDesc
    namespace = namespaceGen("vc_utils", body)
    includes = includeGen(namespace)
    includeGuard = includeGardGen(classname, includes)

    fObj = open(path + filename, "w") 

    for elem in file:
        fObj.write(elem) 
    for elem in includeGuard:
        fObj.write(elem) 
    
    fObj.close()

    if (format):
        if not(shutil.which("clang-format")):
            print("WARNING: clang-format not found. File not formated.")
        else:
            os.system("clang-format -style=file -i " + path + filename)

    return
 
#This function adds an include guard around a list of strings
#named body.
#The define of the include guard could be named by classname parameter.
def includeGardGen( classname="", body=[] ):
    "puts a include guard around a body string list"
    retList=["#ifndef " + classname.upper() + "_H_\n"]
    retList.extend(["#define " + classname.upper() + "_H_\n"])
    retList += body
    retList.extend(["#endif\n"])
    return retList

#This function adds a namespace around the body.
#The body contains a list of strings which should be
#inside the namespace.
def namespaceGen( namespace="", body=[] ):
    "puts a namespace around a body string list"
    retList=["\nnamespace  " + namespace + "\n{\n"]
    retList += body
    retList.extend(["} // end of namespace " + namespace + "\n\n"])
    return retList

#This function returns a list of strings with forward declarations of a 
#task vertex class.    
def declGen():
    retList = ["\n/************************************************************************/\n"]
    retList.extend(["// declarations:\n"])
    retList.extend(["class Observer;\n"])
    retList.extend(["struct ProcessUnit_Base;\n"])
    retList.extend(["/************************************************************************/\n"])
    return retList


#This function generates a c++ class implementation
#around a string list named body.
#The body should include the class methods and members.
#The function adds the class name, the derivations 
#and a doxygen class description base and return this
#as a list of string.
#The parameters are:
#   classname: string of the class name
#   template: a list of template parameter descriptions
#             including name/type and initial value
#   body: list of strings with methods and members of the class
def classGen( classname="", template=[], body=[] ):
    "builds class body around body" 

    #import needed functions
    from doxygenDescriptionGen import classDescriptionGen

    #check number of templates
    numOfTemplates = len(template)

    #check if tubles of template is right (name, standard value)
    for it in template:
        if (len(it) > 2):
            raise ValueError(" to many arguments ")

    #implement class doxygen description
    retList = classDescriptionGen(classname, numOfTemplates)
    
    #implement tamplate description
    if (numOfTemplates != 0):
        retList.extend(["template<\n"])
        for it in template:
            if not(it[1]) or it[1] is "\"\"":
                retList.extend(["typename " + it[0] + ",\n"])
            else:
                retList.extend(["typename " + it[0]])
                retList.extend([" = " + it[1] + ",\n"])
        retList[-1] = retList[-1].replace(",", ">")
        
    #implement class 
    retList.extend(["class " + classname + " : public sc_core::sc_module, public Task_Base\n"])
    retList.extend(["{\n"])
    retList += body
    retList.extend(["};\n"])
    return retList

#This function returns a list of strings with all
#necessary includes for a task vertex class.    
def includeGen(body=[]):
    "writes all includes in file"
    retList = ["\n#include <Typedefinitions.h>\n"] 
    retList.extend(["#include <Task_Base.h>\n"])
    retList.extend(["#include <utility>\n"])
    retList.extend(["#include <memory>\n"])
    retList.extend(["#include <tuple>\n"])
    retList += body
    return retList

    
#This function builds the constructor of a task vertex class.
#The function parameters are:
#   classname: string of name of class
#   tparam: list of list of template parameters and there initial values [[tparamName or type, initial], ...]
#   numOfIns: number of inputs of task vertex class
#   inputStrList: a list of strings to name the variables
#   inputSideStr: the first to vales could be named as RHS and LHS    
#The function generates all valid and forbidden constructers.
#The return is a list of strings.     
def constructorGen( classname="", tparam=[], numOfIns=0, inputStrList=[], inputSideStr=["vc_utils::SIDE::LHS", "vc_utils::SIDE::RHS"] ):
    "generate constructor for Standard vertex file"

    #Standard constructer
    retList = ["public:\n" + "//! \\brief constructor with sc_time object\n"]
    retList.extend(["explicit " + classname + "(ProcessUnit_Base* _pUnit, name_t _name, unsigned int _vertexNumber, unsigned int _vertexColor, cobnst sc_time_t& _latency ) :\n"])
    retList.extend(["sc_core::sc_module( _name ),\n"])
    retList.extend(["Task_Base( std::string( _name ), _vertexNumber, _vertexColor, _latency ),\n"])
    retList.extend(["m_coreFreeEv( ( this->getName( ) + \"_coreFreeEv\" ).c_str( ) ),\n"])
    retList.extend(["m_ProcessUnit( _pUnit )\n"])
    retList.extend(["{\n"])

    retList.extend(["\n// set class type\n"])
    retList.extend(["this->setClassType( typeid( *this ).name( ) );\n"])

    retList.extend(["\n//register execution process at scheduler in elaboration phase\n"])
    retList.extend(["sc_core::sc_spawn( sc_bind( &" + classname + "::execute, this ), ( this->getName( ) + \"_" + classname +
                   "Process\" ).c_str( ) );\n"])
    
    #generate synchronisation events
    retList.extend(["\n//generate input value synchronizations events\n"])
    for it in range(numOfIns):
        retList.extend(["m_inputEvVec.emplace_back( new event_t( ( this->getName( ) + \"" + inputStrList[it] + "Ev\" ).c_str( ) ) );\n"])

    retList.extend(["//and list for process notification\n"])
    retList.extend(["for (auto &e : m_inputEvVec)\n"])
    retList.extend(["\tm_exeProcEvAndList &= *e;\n"])

    retList.extend(["\n//create Observer for input values\n"])
    for it in range(numOfIns):
        if (it <= 1):
            retList.extend(["inputObs.addObserver( m_inputEvVec[" + inputSideStr[it] + "].get(),\n" + 
                        "reinterpret_cast<dataPtr_t>( &m" + inputStrList[it] + "Val.second ),\n" + 
                        "sizeof( " + str(tparam[it]) + " ) );\n"])
        else:
            retList.extend(["inputObs.addObserver( m_inputEvVec[" + str(it) + "].get(),\n" + 
                        "reinterpret_cast<dataPtr_t>( &m" + inputStrList[it] + "Val.second ),\n" + 
                        "sizeof( " + str(tparam[it]) + " ) );\n"])
    retList.extend(["}\n\n"])

    #second constructer without sc_time object
    retList.extend(["//! \\brief constructor\n"])
    retList.extend(["explicit " + classname + 
                    "(ProcessUnit_Base* _pUnit, name_t _name, unsigned int _vertexNumber, unsigned int _vertexColor, double _latency, unit_t _unit ) :\n"])
    retList.extend([ classname +"( _pUnit, _name, _vertexNumber, _vertexColor, sc_time_t( _latency, _unit ) )\n"])
    retList.extend(["{ }\n\n"])

    #destructor
    retList.extend(["//! \\brief destructor\n"])
    retList.extend(["virtual ~"+ classname + "( ) = default;\n\n"])

    #forbidden constructers:
    retList.extend(["private:\n" + "//forbidden constructors:\n" + classname + "( ) = delete; //!< \\brief because vertexID should be unique\n"])
    retList.extend([classname + "( const " + classname + "& _source ) = delete;  //!< \\brief because sc_module could not be copied\n"])
    retList.extend([classname + "( "+ classname + "&& _source ) = delete;  //!< \\brief because move not implemented for sc_module\n"])
    retList.extend([classname + "& operator=( const "+ classname + "& _source ) = delete; //!< \\brief forbidden\n"])
    retList.extend([classname + "& operator=( "+ classname + "&& _source ) = delete; //!< \\brief forbidden\n\n"])
    return retList

#A notification of values depends on the special structure of a task vertex class.
#(for example the number of outputs and there order (id)).
#The notifyObservers Method has to be implemented by the user.
#This function only adds the base construction of this class method and 
#the base structure to describe the method in doxygen.
#The return is a string list.
def notificationGen(returnStrList=[], numOfBytes=[], numOfOuts=0):
    "generate notifyObservers function implementation"

    from doxygenDescriptionGen import functionDescriptionGen

    #generate doxygen description
    retList = ["public:\n"] + functionDescriptionGen("notifyObservers", 1 )

    retList.extend(["virtual void notifyObservers( unsigned int _outputId ) override\n"])
    retList.extend(["{\n"])
    retList.extend(["#error implement observer notifications here\n"])
    retList.extend(["}\n"])

    return retList
 

#Every task vertex class has a functionality to implement. 
#If the functionality works on values, it should be the members
#of the object, copied by notify-Method from the Observer class.
#This function generates a base construction of the execute function.
#The user has to implement the functionality by himself.
#The result of the function is a list of strings with:
#  - a doxygen description base
#  - the synchronization mechanism for input values and free core unit
#  - the space for the functionality and the notifyObservers-method.
def executeGen():
    "generate execute function implementation"

    from doxygenDescriptionGen import functionDescriptionGen

    #generate doxygen description
    retList = ["public:\n"] + functionDescriptionGen("execute")

    retList.extend(["virtual void execute( void ) override\n"])
    retList.extend(["{\n"])
    retList.extend(["while ( true )\n"])
    retList.extend(["{\n"])
    retList.extend(["//parent value synchronization\n"])
    retList.extend(["sc_core::wait( m_exeProcEvAndList );\n\n"])


    retList.extend(["m_ProcessUnit->isCoreUsed( &m_coreFreeEv );\n"])
    retList.extend(["sc_core::wait( m_coreFreeEv );\n\n"])
    
    retList.extend(["#error write vertex functionality here\n\n"])

    retList.extend(["\nm_ProcessUnit->freeUsedCore( this->getVertexLatency( ));\n\n"])
    retList.extend(["//notify children observers for output value\n"])
    retList.extend(["#error call notifyObservers from here\n"])
    
    retList.extend(["}\n"])
    retList.extend(["}\n"])
    return retList

#This function generates a class method implementation to return all 
#outgoing values a task vertex class.
#Therefor the return value of the function resultGen is a tuple of values.
#The description of the tuple and the maker function depends on types of
#outgoing values.
#The parameters are:
#  numOfOuts: number of output parameters
#  returnStrList: list of strings to name return values
#  outputType: list of string with output value type
#The function returns a list of strings with a specialized function
#and the base of a doxygen function description.
def resultGen( numOfOuts=1, returnStrList=[], outputType=[] ):
    "generate getResult implementation"

    from doxygenDescriptionGen import functionDescriptionGen

    if (len(outputType) < numOfOuts):
        raise ValueError("number of types is not equal to number of outputs")

    #generate doxygen description
    retList = ["public:\n"] + functionDescriptionGen("getResults")

    #generate return tuple
    retList.extend(["std::tuple<"])
    for it in range(numOfOuts):
        if (it == 0):
            retList.extend([outputType[it]])
        else:
             retList.extend([", " + outputType[it]])
    retList.extend(["> getResults( void ) const\n"])
    retList.extend(["{\n"])
    retList.extend(["auto retVal = std::make_tuple (\n"])

    for it in range(numOfOuts):
        if (it == 0):
            retList.extend(["m" + returnStrList[it] + "Val.second"])
        else:
             retList.extend([", m" + returnStrList[it] + "Val.second"])

    retList.extend([");\n"])
    retList.extend(["return retVal;\n"])
    retList.extend(["}\n"])
    return retList

#This function isn't used anymore but could be used to add vector of Observer to a task vertex class.
#The vector is replaced by the ObserverManager.
#The manager is implemented in th Task_Base class so the vector isn't needed anymore.
#The return is a list of strings with a vector of Observer and a doxygen description line.
def observerGen( ):
    "generate Observer instantiation"

    from doxygenDescriptionGen import valueDescriptionGen

    retList = ["public:\n"]
    retList.extend(["\n/************************************************************************/\n"])
    retList.extend(["//Observers\n"])
    retList.extend(valueDescriptionGen("inputObsVec"))
    retList.extend(["/************************************************************************/\n"])
    retList.extend(["std::vector<std::unique_ptr<Observer> > inputObsVec;\n"])

    return retList
    
#This functions adds private members to a task vertex class.
#The parameters are:
#   numOfIns: number of input parameters
#   inputStrList: a list of strings to name the variables
#   inputType: a list of string with data types of the member variables
#   numOfOuts: number of input parameters
#   returnStrList: a list of strings to name the variables
#   outputType: a list of string with data types of the member variables
#   inputSideStr: the first to vales could be named as RHS and LHS
#The function also adds the base for variables descriptions in doxygen for every value.
#The function will generate an exception if more then twenty in- or output values are generated.
#The return is a list of strings with members, events and a process unit pointer.
def memberGen(numOfIns=0, inputStrList=[], inputType=[], numOfOuts=0, returnStrList=[], outputType=[], inputSideStr=["vc_utils::SIDE::LHS", "vc_utils::SIDE::RHS"]):
    "implement input and result variables"

    from doxygenDescriptionGen import valueDescriptionGen

    if (numOfOuts != len(outputType)):
        raise ValueError("wrong number of output types for set number of outputs")
    if (numOfIns != len(inputType)):
        raise ValueError("wrong number of input types for set number of inputs")

    retList = ["private:\n"]
    retList.extend(["/************************************************************************/\n"])
    retList.extend(["//Member\n"])
    retList.extend(["/************************************************************************/\n\n"])
    retList.extend(valueDescriptionGen("numOfIns"))
    retList.extend(["const unsigned int numOfIns = { " + str(numOfIns) + " };\n"])
    retList.extend(valueDescriptionGen("numOfOuts"))
    retList.extend(["const unsigned int numOfOuts = { " + str(numOfOuts) + " };\n\n"])
    
    #generate inputs
    for it in range(numOfIns):
        valName = "m" +  inputStrList[it] + "Val"
        retList.extend(valueDescriptionGen(valName))
        if (it < 2):
            retList.extend(["std::pair<unsigned int, " + inputType[it] + " > " + valName + " = { " +
                            inputSideStr[it] + ", 0 };\n\n"])
        else:
            retList.extend(["std::pair<unsigned int, " + inputType[it] + " > " + valName + " = { " +
                            str(it) + ", 0 };\n\n"])
    #generate outputs
    for it in range(numOfOuts):
        valName = "m" +  returnStrList[it] + "Val"
        retList.extend(valueDescriptionGen(valName))        
        retList.extend(["std::pair<unsigned int, " + outputType[it] + " > " + valName + " = { " +
                            str(it) + ", 0 };\n\n"])

    #synchronization events
    retList.extend(["/************************************************************************/\n"])
    retList.extend(["//scheduler synchronization events\n"])
    retList.extend(["/************************************************************************/\n\n"])
    retList.extend(valueDescriptionGen("m_inputEvVec"))
    retList.extend(["std::vector<std::unique_ptr<event_t> > m_inputEvVec;\n"])
    retList.extend(valueDescriptionGen("m_coreFreeEv"))
    retList.extend(["event_t m_coreFreeEv;\n"])
    retList.extend(valueDescriptionGen("m_exeProcEvAndList"))
    retList.extend(["sc_core::sc_event_and_list m_exeProcEvAndList;\n"])
    
    #interface to process unit
    retList.extend(["\n/************************************************************************/\n"])
    retList.extend(["//interface to process unit\n"])
    retList.extend(["/************************************************************************/\n\n"])
    retList.extend(valueDescriptionGen("m_ProcessUnit"))
    retList.extend(["ProcessUnit_Base* const m_ProcessUnit;\n"])
    
    return retList


#Every SystemC module is derived from sc_object.
#This short function adds the main object description functions to a 
#task vertex implementation.
#The function needs the class name to return the correct kind of module. 
#The return is a list of strings with function implementation and a short
#doxygen command with a short brief. 
def scModuleFuncGen(classname=""):
    "generates implementation for object description output"

    #kind implementaion
    retList = ["public:\n"] 
    retList.extend(["//! \\brief return kind of systemC module as string\n"])
    retList.extend(["virtual const char* kind( ) const override { return \"" + classname + "\"; }\n\n"])

    #print implementation
    retList.extend(["//! \\brief return kind of systemC module as string\n"])
    retList.extend(["virtual void print(::std::ostream& os = ::std::cout ) const override" +
                    "{os << this->name( );}\n\n"])

    #dump implementation
    retList.extend(["//! \\brief return name and kind of systemC module as string\n"])
    retList.extend(["virtual void dump(::std::ostream& os = ::std::cout ) const override" + 
                    "{os << this->name( ) << \", \" << this->getClassType( );}\n\n"])

    return retList