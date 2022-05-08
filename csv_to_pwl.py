import sys, getopt, csv
from decimal import *
from utils import time_to_str, parse_time

def convert(input_file, output_file, sample_interval):
    with open(input_file, newline='') if input_file else sys.stdin as csvfile:
        with open(output_file, mode='w') if output_file else sys.stdout as pwlfile:
            reader = csv.reader(csvfile, delimiter=',')
            timestamp = Decimal("0")
            for row in reader:
                timestamp += sample_interval
                pwlfile.write(time_to_str(timestamp) + " " + str(Decimal(row[0])) + "\n")


def main(argv):
    input_file = None
    output_file = None
    sample_interval = None

    usage = 'waveform_to_pwl.py -i <input file> -o <output file> -s <sample interval>'

    try:
        opts, args = getopt.getopt(argv, "hi:o:s:", ["input_file=", "output_file=", "sample_interval="])
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
        elif opt in ("-s", "--sample_interval"):
            sample_interval = arg

    if sample_interval is None:
        print(usage)
        sys.exit(2)

    convert(input_file, output_file, parse_time(sample_interval))


if __name__ == "__main__":
    main(sys.argv[1:])
