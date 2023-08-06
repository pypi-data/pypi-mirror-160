# Counting Unique Characters
This module allows you to count the unique characters that it receives upon entry. 
Works with files and strings.

**Getting started**
A variable `args` is created to which all the arguments that were passed 
to the CLI during the execution of the `create_parser()` function are assigned.

In function `file_check()` receives an object `args` as an input and determines the type:
- if `args` contains a file, then the `load_file()` file handler function is run 
    and the contents of the file are passed to the `unique_characters()` function;
- if `args` does not contain a file, but `args` contains a string, then that string 
    is passed to the `unique_characters()` function

The `unique_characters()` function processes the string passed to it 
and returns the number of unique characters in that string.


