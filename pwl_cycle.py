import sys, getopt
from decimal import *
from utils import time_to_str, parse_time

def cycle(input_file, output_file, num_cycles, period):
    with open(input_file) if input_file else sys.stdin as infile:
        lines = infile.readlines()
        lines = [line.rstrip() for line in lines]
    offset = Decimal(0)
    with open(output_file, mode='w') if output_file else sys.stdout as pwlfile:
        for x in range(num_cycles):
            for line in lines:
                parts = line.split(" ")
                pwlfile.write(time_to_str(parse_time(parts[0]) + offset) + " " + parts[1] + "\n")
            offset += period


def main(argv):
    input_file = None
    output_file = None
    num_cycles = 2
    period = None

    usage = 'waveform_to_pwl.py -i <input file> -o <output file> -n <number of cycles> -p <period>'

    try:
        opts, args = getopt.getopt(argv, "hi:o:n:p:", ["input_file=", "output_file=", "num_cycles=", "period="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-i", "--input_file"):
            input_file = arg
        elif opt in ("-o", "--output_file"):
            output_file = arg
        elif opt in ("-n", "--num_cycles"):
            num_cycles = arg
        elif opt in ("-p", "--period"):
            period = arg

    if period is None:
        print(usage)
        sys.exit(2)

    cycle(input_file, output_file, int(num_cycles), parse_time(period))


if __name__ == "__main__":
    main(sys.argv[1:])
