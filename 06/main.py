from Parser import *
import sys
import os


def write_to_file(p, name):

    bin_file = open(name + '.hack', "w")

    while p.has_more_commands():
        p.advance()
        bin_file.writelines(p.get_binary() + '\n')

    bin_file.close()


if __name__ == '__main__':

    only_file_name = sys.argv[1].split('/')[-1]

    if ".asm" in only_file_name:
        only_file_name = only_file_name.split('.')[0]

        # gets the directory we are going to work with
        file_directory_help = sys.argv[1].split('.asm')[0]

        p = Parser(sys.argv[1])
        write_to_file(p, file_directory_help)

    else:
        path = sys.argv[1]
        files = os.listdir(path)

        files_asm = [i for i in files if i.endswith('.asm')]

        for file in files_asm:
            p = Parser(path + "/" + file)

            file_name = file.split('.')[0]
            write_to_file(p, path + "/" + file_name)
