from os.path import isfile
from analyzer import Analyze
from vm import VirtualMachine as VMachine
from sys import argv as input_args

def main():
    if len(input_args) == 1:
        print("ERROR: Missing file path")
        return
    file_path = input_args[1]
    if isfile(file_path):
        file = open(file_path)
        output,log, instruction = Analyze(file.read()).get_result()
        file.close()
        if output == 1:
            print("ERROR: %s"%log)
            return
        vm_output, vm_log = VMachine(instruction).run()
        if vm_output == 1:
            print("ERROR: %s"%vm_log)
    else:
        print("ERROR: Unknown %s"%file_path)

if __name__ == "__main__":
    main()
    