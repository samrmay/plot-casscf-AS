import os
import sys
from subprocess import Popen, PIPE
import re


def get_mo_range(out):
    with open(out) as infile:
        while True:
            line = infile.readline()
            if 'Determined orbital ranges:' in line:
                infile.readline()
                active = infile.readline()
                break
        match = re.search(r'Active\s+(\d+)\s+-\s+(\d+)\s+', active)
        orb_min, orb_max = match.group(1, 2)
    return int(orb_min), int(orb_max)


def main():
    cmd = ['orca_plot', 'FeFeTHF+1_9_casscf_022121_locAS.gbw', '-i']
    p = Popen(cmd, stdout=PIPE, stdin=PIPE)
    p.communicate(input='5\n7\n10'.encode())


main()
