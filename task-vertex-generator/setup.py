#coding=UTF8

#generated file archive and install it by other user

from distutils.core import setup

setup(
    name="task-vertex-generator",
    version = "1.0",
    author = "Werner, A",
    author_email = "andre.werner-w2m@rub.de",
    description = "Generate task graph vertices for simulation in SystemC",
    data_files = [(".",[".clang-format"] )],
    py_modules = ["TaskVertexGenerator",
                  "doxygenDescriptionGen",
                  "fileGenerator",
                  "fileReader",
                  "interactiveGen"],
    url="localhost"
    )


