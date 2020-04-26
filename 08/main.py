from CodeWriter import *
import sys
import os

if __name__ == '__main__':

    # checks if we are dealing with a directory or file
    is_directory = os.path.isdir(sys.argv[1])

    # extract the final file name
    if is_directory:
        only_directory_name = sys.argv[1].split('/')[-1]
        output_file_name = sys.argv[1] + "/" + only_directory_name + ".asm"
    else:
        output_file_name = os.path.splitext(os.path.abspath(sys.argv[1]))[0] + ".asm"

    # creates a file we are writing to
    code_write = CodeWriter(output_file_name)

    # read the files or file parse them and write them into a final file
    if is_directory:
        files = os.listdir(sys.argv[1])
        files_vm = [i for i in files if i.endswith('.vm')]
        for file in files_vm:
            code_write.set_file_name(sys.argv[1] + "/" + file)
    else:
        code_write.set_file_name(sys.argv[1])

    code_write.close()
