from os.path import isfile
from analyzer import Analyze
from vm import VirtualMachine as VMachine
from sys import argv as input_args

def run(context):
    output,log, instruction = Analyze(context).get_result()
    if output == 1:
        print("ERROR: %s"%log)
        return
    vm_output, vm_log = VMachine(instruction).run()
    if vm_output == 1:
        print("ERROR: %s"%vm_log)

def main():
    if len(input_args) == 1:
        while 1:
            context = input("Enter list of instruction: ")
            if context == "exit":
                return
            run(context)
    file_path = input_args[1]
    if isfile(file_path):
        file = open(file_path)
        context = file.read()
        file.close()
        run(context)
    else:
        print("ERROR: Unknown %s"%file_path)

if __name__ == "__main__":
    main()
    