#coding=UTF8

import os
import re
import sys
from fileGenerator import fileBuilder

#This is the filed which implements interactive mode.
#The user is asked by a couple of questions to get the needed
#parameters and the file is build.
#Then the file is build and saved as: path + filename
#The return is a list of strings to show the user input at the end of building
def parameterGen():
    "get parameter for task vertex generator interactive"
    
    #get path (ask as long as right path not entered)
    #write syntax is without filename but with last folder separator
    while True:
        print("You can enter a absolute path or press the ENTER button")
        print(" to use current path of script for generated file result.")
        path = input("Please enter absolute path for result file: ")
        if '.' in path:
            print("Please enter path except of filename!")
            continue
        elif not(path):
            path=os.getcwd()
            if sys.platform == "win32":
                 path = path + "\\"
            else:
                path = path + "/"
            break
        else:
            if sys.platform == "win32":
                if not(re.match(r"^[a-zA-Z]:\\[\w\s\\]+\\$", path)):
                    print("ERROR: wrong path syntax")
                    print("\tvalid syntax on Windows: c:\\User\\...\\")
                    print("your entered: " + path)
                    continue
                else:
                    re.escape(path)
                    break
            else:
                if not(re.match(r"^/[\w\s/]+/$", path)):
                    print("ERROR: wrong path syntax")
                    print("\tvalid syntax on Unix: /home/.../")
                    print("your entered: " + path)
                    continue    
                else:
                    re.escape(path)
                    break
    
    #get filename
    #write syntax is with file extension for c++ files
    while True:
        filename = input("Please enter filename including file extension: ")
        if not(filename):
            print("ERROR: filename doesn't be empty.")
            continue
        if not(re.match(r"^[a-zA-Z_]+\.[a-z]{1,3}$", filename)):
            print("ERROR: wrong filename syntax")
            print("Please enter filename with valid c++ file extension")
            print("your entered: " + filename)
            continue
        else:
            break
    
    #get classname
    while True:
        classname = input("Please enter classname: ")
        if not(classname):
            print("ERROR: classname doesn't be empty.")
            continue
        if not(re.match(r"^[a-zA-Z][\w]+$", classname)):
            print("ERROR: wrong classname syntax")
            print("your entered: " + classname)
            continue
        else:
            break

    #get input values        
    print("\nInput values:")
    print("===============\n\n")

    #enter whole number of inputs
    while True:
        numOfIns = input("How many input values will have the task vertex:")
        if not(re.match(r"^\d{1,2}$", numOfIns)):
            print("ERROR: your enter has to be a positive integer less then 21")
            continue
        else:
            break
    
    #if one needs inputs, how many of them are templates
    if int(numOfIns) != 0:
        while True:
            numOfTemps = input("How many of them are template parameters:")
            if not(re.match(r"^\d{1,2}$", numOfTemps)):
                print("ERROR: your enter has to be a positive integer less then 21")
                continue
            elif int(numOfIns) < int(numOfTemps):
                print("ERROR: number of templates has to be a positive integer less or equal then number of inputs")
                continue
            else:
                break

        inputParam = [0]
        
        #enter template parameter description: datatype or name, initial value
        if int(numOfTemps) > 0:
            inputParam[0] = int(numOfTemps)
            print("Please enter template input members separated by return in the following style:")
            print("template parameter,default value")
            print("If you don't want a default value insert a empty string!")
            for index in range(int(numOfTemps)):
                while True:
                    tmp = input(str(index + 1) + ": ")
                    if not(re.match(r"^[a-zA-Z\d\s]+,[\w\s\d]*$", tmp)):
                        print("ERROR: wrong syntax, plaese try again")
                        continue
                    else:
                        tmp = re.sub(r"^\s+", "", tmp)
                        tmp = re.sub(r",\s+", ",", tmp)
                        tmp = re.sub("r\s+$", "", tmp)
                        tmp = tmp.split(',')
                        elem = [tmp[0], tmp[1]]
                        inputParam.append(elem)
                        break
        #enter leftover inputs
        if int(numOfIns) - int(numOfTemps) > 0:
            print("Please enter the datatype of the remainig inputs:\n")
            for index in range(int(numOfIns) - int(numOfTemps)):
                while True:
                    tmp = input(str(index + 1) + ": ")
                    if not(re.match(r"^[a-zA-Z\s]+$", tmp)):
                        print("ERROR: wrong syntax, please try again")
                        continue
                    else:
                        tmp = re.sub(r"^\s+", "", tmp)
                        tmp = re.sub("r\s+$", "", tmp)
                        elem = [tmp]
                        inputParam.append(elem)
                        break
    else:
        inputParam = [0]

    print("\nOutput values:")
    print("===============\n\n")

    #enter whole number of outputs
    while True:
        numOfOuts = input("How many output values will the task vertex have:")
        if not(re.match(r"^\d{1,2}$", numOfIns)):
            print("ERROR: your enter has to be a positive integer less then 21")
            continue
        else:
            break
    #if one needs outputs, how many of them are templates
    if int(numOfOuts) != 0:
        while True:
            numOfTemps = input("How many of them are template parameters:")
            if not(re.match(r"^\d{1,2}$", numOfTemps)):
                print("ERROR: your enter has to be a positive integer less then 21")
                continue
            if int(numOfOuts) < int(numOfTemps):
                print("ERROR: number of templates has to be a positive integer less or equal then number of outputs")
                continue                
            else:
                break

        outputParam = [0]
    
        #enter template output value descriptions: datatype or name, initial value
        if int(numOfTemps) > 0:
            outputParam[0] = int(numOfTemps)
            print("Please enter template output members separated by return in the following style:")
            print("template parameter, default value")
            print("If you don't want a default value insert a empty string!")
            for index in range(int(numOfTemps)):
                while True:
                    tmp = input(str(index + 1) + ": ")
                    if not(re.match(r"^[a-zA-Z\d\s]+,[\w\s\d]*$", tmp)):
                        print("ERROR: wrong syntax, please try again")
                        continue
                    else:
                        tmp = re.sub(r"^\s+", "", tmp)
                        tmp = re.sub(r",\s+", ",", tmp)
                        tmp = re.sub("r\s+$", "", tmp)
                        tmp = tmp.split(',')
                        elem = [tmp[0], tmp[1]]
                        outputParam.append(elem)
                        break
        
        #enter leftover outputs
        if int(numOfOuts) - int(numOfTemps) > 0:
            print("Please enter the datatype of the remainig outputs:\n")
            for index in range(int(numOfOuts) - int(numOfTemps)):
                while True:
                    tmp = input(str(index + 1) + ": ")
                    if not(re.match(r"^[a-zA-Z\s]+$", tmp)):
                        print("ERROR: wrong syntax, please try again")
                        continue
                    else:
                        tmp = re.sub(r"^\s+", "", tmp)
                        tmp = re.sub("r\s+$", "", tmp)
                        elem = [tmp]
                        outputParam.append(elem)
                        break
    else:
        outputParam = [0]
   
    #ask for clang formated output
    while True:
        clang = input("Do you wish an clang formated output [y,n]?")
        if not(re.match(r"^[yn]$", clang, re.IGNORECASE)):
            print("answer has to be simple character y or n.")
            continue
        else:
            clang = clang.lower()
            if clang in 'y':
                format = True
            else:
                format = False
            break
    
    #safe all parameters for printing at the end of building
    #so one can check if the inputs are interpreted right
    parameter = [path, filename, classname, inputParam, outputParam, format]
    
    #build file
    fileBuilder(parameter[0], parameter[1], parameter[2], parameter[3], parameter[4], parameter[5])

    return parameter