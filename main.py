import os
import sys
import subprocess
import re


def generate_plot_inp_from_out(base, mo_infile_ext, outfile_ext):
    out = base + '.out'
    mo_infile = base + mo_infile_ext
    plot_inp = base + '_plot.inp'

    ext_opt_dict = {'.cube': "Gaussian_Cube", '.plt': "gOpenMol_bin"}

    with open(out) as infile:
        while True:
            line = infile.readline()
            if 'Determined orbital ranges:' in line:
                infile.readline()
                active = infile.readline()
                print(active)
                break
        match = re.search(r'Active\s+(\d+)\s+-\s+(\d+)\s+', active)
        orb_min, orb_max = match.group(1, 2)

    with open(plot_inp, 'w') as outfile:
        outfile.write(f"%moinp {mo_infile}\n")
        outfile.write("\n".join([f"%output", 'XYZFile true', 'end\n']))

        outfile.write(f'%plots\n')
        outfile.write(f"Format {ext_opt_dict[outfile_ext]}\n")

        for mo in range(int(orb_min), int(orb_max) + 1):
            outfile.write(f'MO("{base}.mo{mo}a{outfile_ext}", {mo}, 0)\n')
        outfile.writelines('end')


generate_plot_inp_from_out('FeFeTHF+1_9_casscf_022121_locAS', '.gbw', '.cube')
