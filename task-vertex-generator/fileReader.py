#coding=UTF8

#This is a parser for an input file which contains descriptions
#of task vertex classes.
#Every line in the files describes a special class. 
#The line should have the following structure:
#
#   path;
#   filename;
#   classname;
#   numberOfInputs; 
#   numberOfTemplateInputs;
#   pairs of template inputs in the following structure typeOrName, initalValue | ... | dataType | ...;
#   followed by data type of standard member;
#   numberOfOutputs;
#   numberOfTemplateOutputs;
#   pairs of template outputs in the following structure typeOrName, initalValue | ... | dataType | ...;
#   followed by data type of standard member;
#   clang-format usage true/false
#  
#   This examples should help for understanding line structure:
#       ""; AddVertex.h; AddVertex; 2; 2; T, int | U, T; 1; 1; O, T; TRUE
#       "c:\coding\test\"; MulVertex.h; MulVertex; 2; 2; T, int | U, T; 1; 1; O, T; true
#       "/hone/user/coding/"; DivVertex.h; DivVertex; 2; 2; T, int | U, T; 1; 1; O, T; FALSE
#If a line is valid, the file will be build automatically and saved as: path + filename.

from fileGenerator import fileBuilder
import re
import os
import sys


def fileReader(filepath):
    "parse file and generate task vertex class from line elements"
    #load file
    inputFile = open(filepath,"r")

    #separate lines from file
    listOfLines = inputFile.readlines()
    
    for line in listOfLines:
        parameterList = []
        
        #erase whitespace
        line = line.strip() #at front and back of string
        line = line.replace("; ", ";") #between values

        #separate line elements
        elements = line.split(";")

        #check for valid path
        path = elements[0]
        path = path.replace('\"', "")
        if not(path):
            path=os.getcwd()
            if sys.platform == "win32":
                parameterList.append(path + "\\")
            else:
                parameterList.append(path + "/")
        else:
            if (sys.platform == "win32"):
                if not(re.match(r"[a-zA-Z]:\\[[\w\s\\\d]+\\$", path)):
                        raise FileNotFoundError("No valid Filepath")
                else:
                    re.escape(path)
                    parameterList.append(path)
            elif (sys.platform == "darwin" or sys.platform.startswith("linux")):
                if not(re.match(r"^/[[\w\s/\d]+/$", path)):
                    raise FileNotFoundError("No valid Filepath")
                else:
                    re.escape(path)
                    parameterList.append(path)
            else:
                raise SystemError("operating system is not supported")

        #check for valid filename
        filename = elements[1]
        if not(filename):
            raise ValueError("filename doesn't be empty.")
        elif not(re.match(r"^[\w]+\.[a-z]{1,3}$", filename)):
            raise ValueError("wrong filename syntax")
        else:
            parameterList.append(filename)

        #check for valid classname
        classname = elements[2]
        if not(classname):
            raise ValueError("classname doesn't be empty.")
        elif not(re.match(r"^[a-zA-Z][\w]+$", classname)):
            raise ValueError("wrong classname syntax")
        else:
            parameterList.append(classname)

        #check valid number of inputs
        numOfIns = int(elements[3])
        if numOfIns > 20 or numOfIns < 0:
            raise ValueError("The number of inputs has to be a positive integer less then 21")
        
        #are there any input values
        if not(numOfIns):
            parameterList.append([0])
        else:
            inputList = [0]
            numOfTemps = int(elements[4])
            if numOfIns < numOfTemps:
                raise ValueError("Number of Templates higher than number of all input values.")
            tmpIns = elements[5]
            tmpIns = tmpIns.split("|")

            #are there any template values
            if numOfTemps > 0:
                inputList[0] = numOfTemps

                #copy templates
                for index in range(numOfTemps):
                    tmp = tmpIns[index]
                    if not(re.match(r"^[a-zA-Z\s]+,[\w\s\d]*$", tmp)):
                        raise ValueError("wrong syntax for input value")
                    else:
                        tmp = re.sub(r"^\s+", "", tmp)
                        tmp = re.sub(r",\s+", ",", tmp)
                        tmp = re.sub("r\s+$", "", tmp)
                        tmp = tmp.split(',')
                        elem = [tmp[0], tmp[1]]
                        inputList.append(elem)

            #copy other inputs
            for index in range(numOfTemps, numOfIns):
                tmp = tmpIns[index]
                if not(re.match(r"^[a-zA-Z\s]+$", tmp)):
                    raise ValueError("wrong syntax for input value")
                else:
                    tmp = re.sub(r"^\s+", "", tmp)
                    tmp = re.sub("r\s+$", "", tmp)
                    elem = [tmp]
                    inputList.append(elem)

            parameterList.append(inputList)

        #check valid number of outputs
        numOfOuts = int(elements[6])
        if numOfOuts > 20 or numOfOuts < 0:
            raise ValueError("The number of inputs has to be a positive integer less then 21")
        
        #are there any input values
        if not(numOfOuts):
            parameterList.append([0])
        else:
            outputList = [0]
            numOfTemps = int(elements[7])
            if numOfOuts < numOfTemps:
                raise ValueError("Number of Templates higher than number of all output values.")
            tmpOuts = elements[8]
            tmpOuts = tmpOuts.split("|")

            #are there any template values
            if numOfTemps > 0:
                outputList[0] = numOfTemps

                #copy templates
                for index in range(numOfTemps):
                    tmp = tmpOuts[index]
                    if not(re.match(r"^[a-zA-Z\s]+,[\w\s\d]*$", tmp)):
                        raise ValueError("wrong syntax for output value")
                    else:
                        tmp = re.sub(r"^\s+", "", tmp)
                        tmp = re.sub(r",\s+", ",", tmp)
                        tmp = re.sub("r\s+$", "", tmp)
                        tmp = tmp.split(',')
                        elem = [tmp[0], tmp[1]]
                        outputList.append(elem)

            #copy other inputs
            for index in range(numOfTemps, numOfOuts):
                tmp = tmpOuts[index]
                if not(re.match(r"^[a-zA-Z\s]+$", tmp)):
                    raise ValueError("wrong syntax for output value")
                else:
                    tmp = re.sub(r"^\s+", "", tmp)
                    tmp = re.sub("r\s+$", "", tmp)
                    elem = [tmp]
                    outputList.append(elem)



            parameterList.append(outputList)

        #check for auto format
        clang = elements[9]
        clang =clang.lower()
        if not(re.match(r"^[a-zA-Z]{4,5}$",clang)):
            raise ValueError("wrong syntax for auto format choose")
        else:
            if clang == "true":
                parameterList.append(True)
            else:
                parameterList.append(False)        

        fileBuilder(parameterList[0],parameterList[1],parameterList[2],parameterList[3],parameterList[4],parameterList[5])

    inputFile.close()
    return 