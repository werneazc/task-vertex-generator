#coding=UTF8

#This function builds a doxygen command line to describe a variable. 
#The function can get the variable name as a optional parameter.
#The return is a list of strings with the description base.
def valueDescriptionGen( variablename="" ):
    "generates doxygen variable discription base"
    retList = ["//! \\var " + variablename + "\n"]
    retList.extend(["//! \\brief short description\n"])
    return retList

    
#This function builds doxygen command lines to describe a class. 
#If the class has template variables it adds an optional description base.
#The function needs as optinal parameters the class name and the number of template parameters.
#The return is a list of strings with the description base.
def classDescriptionGen( classname = "", countValTparam = 0 ):   
    "generates doxygen class discription base"
    retList = ["\n/************************************************************************/\n"]
    retList.extend(["// " + classname + "\n"])
    retList.extend(["//! \n"])
    retList.extend(["//! \\class " + classname + "\n"])
    retList.extend(["//! \\brief short description\n"])
    retList.extend(["//!\n"])
    retList.extend(["//! \\details detailed description\n"])
    retList.extend(["//!\n"])
    if (countValTparam != 0):
        for it in range(countValTparam):
            retList.extend(["//! \\tparam template parameter description\n"])
    retList.extend(["/************************************************************************/" + "\n\n"])
    return retList

#This is s short doxygen command line to name and brief a file.
#The function can get a optional parameter to name the file.
#The return is a list of strings with the description base.
def fileDescriptionGen( filename="" ):
    "generates doxygen function description base"
    retList = ["//! \\file " + filename + "\n"]
    retList.extend(["//! \\brief short description\n\n"])
    return retList

#This function creates a documentation field for doxygen.
#It can get optional parameters for function name and number of parameters.
#The field include beginnings for brief, details, parameter and return.
 #The return is a list of strings with the description base. 
def functionDescriptionGen( functionname="", numOfParam=0 ):
    "generates doxygen file discription base"
    retList = ["\n/************************************************************************/" + "\n"]
    retList.extend(["// " + functionname + "\n"])
    retList.extend(["//! \n"])
    retList.extend(["//! \\brief short description\n"])
    retList.extend(["//!\n"])
    retList.extend(["//! \\details detailed description\n"])
    retList.extend(["//!\n"])
    if (numOfParam != 0):
        for it in range(numOfParam):
            retList.extend(["//! \\param [in] parameter description\n"])
    retList.extend(["//! \\return return value description\n"])
    retList.extend(["/************************************************************************/\n\n"])
    return retList

