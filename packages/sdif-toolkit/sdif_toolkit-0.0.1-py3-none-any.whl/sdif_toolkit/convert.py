import argparse
import os
from tkinter import filedialog
from records import RECORD_TYPES



def read(path):
    file = open(path)
    for line in file.readlines():
        code = line[0:2]
        
        if code in RECORD_TYPES.keys():
            print(RECORD_TYPES[code](line).toJSON())

def is_valid_path(path):
    """Validates path to ensure it is valid in the current file system"""

    if not path:
        raise ValueError("No path given")
    if os.path.isfile(path) or os.path.isdir(path):
        return path
    else:
        raise ValueError(f"Invalid path: {path}")

def parse_args():
    """Get command line arguments"""

    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('-i', '--input_path', dest='input_path', type=is_valid_path, help="The path of the file or folder to process")

    args = vars(parser.parse_args())

    # Display The Command Line Arguments
    print("## Command Arguments #################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in args.items()))
    print("######################################################################")

    return args

def main():

    args = parse_args()

    input_file = args["input_path"]

    if input_file is None:
        input_file = filedialog.askopenfilename()

    if input_file == '':
        exit()

    read(input_file)    


if __name__ == "__main__":
    main()