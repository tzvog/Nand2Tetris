import os

from CompilationEngine import *
import sys

if __name__ == '__main__':

    is_directory = os.path.isdir(sys.argv[1])
    # read the files or file parse them and write them into a final file
    if is_directory:
        files = os.listdir(sys.argv[1])
        files_jack = [sys.argv[1] + "/" + i for i in files if i.endswith('.jack')]
        for file in files_jack:
            output_file_name = os.path.splitext(file)[0] + '.xml'
            CompilationEngine(file, output_file_name)
    else:
        output_file_name = os.path.splitext(os.path.abspath(sys.argv[1]))[0] + ".xml"
        CompilationEngine(sys.argv[1], output_file_name)
