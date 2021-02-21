import os
import sys
import subprocess
import re


def generate_plot_inp_from_out(base, mo_infile_ext, outfile_ext):
    orb_range = re.compile(r'Active\s+(\d+)\s+-\s+(\d+)\s+')

    out = base + '.out'
    mo_infile = base + mo_infile_ext
    plot_inp = base + '_plot.inp'

    ext_opt_dict = {'.cube': "Gaussian_Cube", '.plt': "gOpenMol_bin"}

    with open(out) as infile:
        while True:
            line = infile.readline()
            if line == 'Determined Orbital Ranges':
                infile.readline()
                active = infile.readline()
                break
        match = re.match(orb_range, active)
        orb_min, orb_max = match.group(2, 3)

    with open(plot_inp, 'w') as outfile:
        outfile.writelines([f"%moinp {mo_infile}"])
        outfile.writelines([f"%output", 'XYZFile true', 'end', '\n'])

        outfile.writelines(f'%plots')
        outfile.writelines([f"Format {ext_opt_dict[outfile_ext]}"])

        for mo in range(int(orb_min), int(orb_max) + 1):
            outfile.writelines([f'MO("{base}.mo{mo}a{outfile_ext}", {mo}, 0)'])
        outfile.writelines(['end'])
