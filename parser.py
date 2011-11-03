#!/usr/bin/python

from load import *

import fileinput
import sys

# resolution in seconds
def parse_psi_torque(trace):
    first = True
    for line in fileinput.input(trace):
        fields = line.split(','); 
        start = int(fields[0]) 
        if first:
            offset = start
            first = False
        start = int(start) - offset
        servers = int(fields[3])
        end = int(fields[5]) - offset
        excess = int(fields[4])
        duration = end - start
        deadline = end + excess
        power = float(servers * 200.0)
        work = Work(power, duration)
        yield (start, work, deadline) 


def to_string(parsed):
    return ''.join([str(parsed[0]), ", ", str(parsed[1]), ", ", str(parsed[2])])

parsers = {}
parsers["psi-torque"] = parse_psi_torque

def print_parsers():
    sys.stderr.write(''.join(parsers.keys()))
    sys.stderr.write("\n")

def print_usage(): 
    sys.stderr.write(''.join(["Usage: \n\t", sys.argv[0], " <parser> <tracefile>\n"]))
    sys.stderr.write(''.join(["\t\t or\n\t", sys.argv[0], " parsers\n\t\tfor a list of parsers available.\n"]))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit()
    
    if len(sys.argv) < 3:
        if sys.argv[1] == 'parsers':
            print_parsers()
        else:
            print_usage()
        sys.exit()

    if sys.argv[1] not in parsers:
        sys.stderr.write("ERROR: Unknown parser.\n")
        print_usage()


    for parsed in parsers[sys.argv[1]](sys.argv[2]):
        sys.stdout.write(''.join([to_string(parsed), "\n"]))

