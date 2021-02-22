import argparse
from subprocess import Popen, PIPE
import re


def parse_args():
    parser = argparse.ArgumentParser(
        description="plot active space orbitals from casscf orca job")

    parser.add_argument('-b', '--basename', type=str,
                        help='Basename of orca job')

    parser.add_argument('-f', '--output_format', type=str,
                        help='Output of plot files', default='.cube')

    parser.add_argument('-i', '--mo_input_extension', type=str,
                        help='file extension of MO input file', default='.gbw')

    parser.add_argument('-n', '--ngrid', type=int,
                        help='number of grid points', default='40')

    parser.add_argument('-p', '--plot_type', type=int,
                        help='plot type of output', default='mo')

    args = parser.parse_args()

    return args.basename, args.output_format, args.mo_input_extension, args.ngrid, args.plot_type


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


def generate_plot(p, mo, op, f, pt=1, ngrid=40):
    plot_type = '\n'.join(['1', str(pt)]) + '\n'
    mo_op = '\n'.join(['2', str(mo), '3', str(op)]) + '\n'
    format_ = '\n'.join(['5', str(f)]) + '\n'
    resolution = '\n'.join(['4', str(ngrid)]) + '\n'
    in_dat = plot_type + mo_op + format_ + resolution + '10\n'
    p.stdin.write(in_dat.encode())


def main(basename):
    out_file = basename + '.out'
    mo_file = basename + '.gbw'
    cmd = ['orca_plot', mo_file, '-i']

    orb_min, orb_max = get_mo_range(out_file)

    p = Popen(cmd, stdin=PIPE, stdout=PIPE)
    for mo in range(orb_min, orb_max + 1):
        generate_plot(p, mo, 0, 7)
    p.stdin.write('11\n'.encode())


main('FeFeTHF+1_9_casscf_022121_locAS')
