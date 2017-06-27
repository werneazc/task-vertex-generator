#!/usr/bin/env python
#coding=UTF8

#This script generates task vertex classes by interpreting a file or
#in interactive mode.
#The standard is interactive mode. The user is asked by a couple of 
#questions to get the needed parameters and the file is build.
#If the user adds --file or -f followed by a path or the filename,
#the script works with that file. 
#
#author: Werner, A; date: June 2015

import sys
import os
import re
from argparse import ArgumentParser
from interactiveGen import parameterGen
from fileReader import fileReader

#write parser
parser = ArgumentParser(description="Generate task vertex c++ files for SystemC simulation.",
                        epilog="Filepath only necessary for filemode.")


#add parser options
parser.add_argument("-f","--file", dest="filemode", help="use file mode", action="store_true")
parser.add_argument("filepath", help="path to import file in filemode", nargs="?")


#do building process    
try:
    
    #check for valid python version
    req_version = (3,0)
    cur_version = sys.version_info
    if not(cur_version >= req_version):
        raise EnvironmentError("need python 3.x or higher")

    #get arguments from command line
    args = parser.parse_args();
    
    #interactive mode
    if not(args.filemode):
        # generate output to describe the the script functionality
        print("\nPython Version " + sys.version)
        print("\n\n===========================================================================")
        print("This is a generator for building a basic task vertex structure.")
        print("It implements all functionality to use it in the simulator except")
        print("the operation that has to be done. So you have to implement the execute method")
        print("and the notifyObservers method yourself.\n")
        print("author: Werner, A; date: June 2015")
        print("===========================================================================\n")

        #do interactive mode
        parameter = parameterGen()

        #print finishing message
        print("\nFile successfully build with parameters:")
        for value in parameter:
            print(value)

        print("\n File is saved as: " + parameter[0] + parameter[1])

    #file mode
    #if the file path is valid, the fileReader is called and 
    #task vertex classes are build automatically
    else:
        print("**********************************")
        print("TaskVertexGenerator version 1.0")
        print("author: Werner, A; date: June 2015")
        print("**********************************\n")
        
        #check input file path
        if not(args.filepath):
            raise SyntaxError("file mode need a file or a file path.")
        elif re.match(r"^[a-zA-Z\s]+\.txt$", args.filepath): #file name set -> use current folder path + file name
            tmp = os.getcwd()
            if sys.platform == "win32":
                fileReader(tmp + "\\" + args.filepath)
            else:
                fileReader(tmp + "/" + args.filepath)
        else: #else check path if it's syntactical right 
            tmp = re.sub(r"^\s+", "", args.filepath)
            tmp = re.sub(r"\s+$", "", tmp)
            if (sys.platform == "win32"):
                if not(re.match(r"^[a-zA-Z]:\\[[\w\s\\\d]+\.txt$", tmp)):
                    raise FileNotFoundError("No valid file path")
                else:
                    fileReader(tmp)
            elif (sys.platform == "darwin" or sys.platform.startswith("linux")):
                if not(re.match(r"^/[[\w\s/\d]+\.txt$", tmp)):
                    raise FileNotFoundError("No valid file path")
                else:
                    fileReader(tmp)
            else:
                raise FileNotFoundError("No valid file path")
        
        #print user message at the end of process
        print("File(s) successfully build.")
    
except FileNotFoundError as e:
    print("File not found.")
    print("Please check path or filename.")
    sys.exit(-1)

except TypeError as e:
    print("type error message: ", e.args[0])
    sys.exit(-1)

except ValueError as e:
    print("value error message: ", e.args[0])
    sys.exit(-1)

except EnvironmentError as e:
        print("error message: ", e.args[0])
        print("system version: " + sys.version)
        sys.exit(-1)

else:
    sys.exit(0);
    