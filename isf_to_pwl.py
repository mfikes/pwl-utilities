import sys, getopt, csv
from decimal import *
import struct
from utils import time_to_str, parse_time


# isfread derived from code Copyright (c) 2011, Gustavo Pasquevich,
# derived from a Matlab script isfread.m by Jhon Lipp

def isfread(filename):
    """ Read isf file and return x y and head information.

    input:
        string with the ISF-filename.

    output:
        Returns a tuple of three elements:
        x - list with the x values
        y - list with the y values
        head - dictionary with the head-information stored in the file."""

    FID = open(filename, 'r', encoding='latin-1')

    hdata = FID.read(511)  # read first 511 bytes

    # Subroutines used to extract inrormation from the head --------------------
    def getnum(string, tag):
        """ Loock into the string for the tag and extract the concequent number"""
        n1 = string.find(tag)
        n2 = string.find(';', n1)

        s2 = string[n1 + len(tag):n2]
        j = s2.find('.')
        if j == -1:
            return int(string[n1 + len(tag):n2])
        else:
            return float(string[n1 + len(tag):n2])

    def getstr(string, tag):
        """ Loock into the string for the tag and extract the concequent string"""
        n1 = string.find(tag)
        n2 = string.find(';', n1)
        return string[n1 + len(tag):n2].lstrip()

    def getquotedstr(string, tag):
        """ Loock into the string for the tag and extract the concequent quoted
        string"""
        n1 = string.find(tag)
        n2 = string.find('"', n1 + 1)
        n3 = string.find('"', n2 + 1)
        return string[n2 + 1:n3]

    def cmp(a, b):
        return (a > b) - (a < b)

    # ---------------------------------------------------------------------------

    head = {'bytenum': getnum(hdata, 'BYT_NR'),
            'bitnum': getnum(hdata, 'BIT_NR'),
            'encoding': getstr(hdata, 'ENCDG'),
            'binformat': getstr(hdata, 'BN_FMT'),
            'byteorder': getstr(hdata, 'BYT_OR'),
            'wfid': getquotedstr(hdata, 'WFID'),
            'pointformat': getstr(hdata, 'PT_FMT'),
            'xunit': getquotedstr(hdata, 'XUNIT'),
            'yunit': getquotedstr(hdata, 'YUNIT'),
            'xzero': getnum(hdata, 'XZERO'),
            'xincr': getnum(hdata, 'XINCR'),
            'ptoff': getnum(hdata, 'PT_OFF'),
            'ymult': getnum(hdata, 'YMULT'),
            'yzero': getnum(hdata, 'YZERO'),
            'yoff': getnum(hdata, 'YOFF'),
            'npts': getnum(hdata, 'NR_PT')}

    # The only cases that this code (at this moment) not take into acount.
    if ((head['bytenum'] != 2) or (head['bitnum'] != 16) or
            cmp(head['encoding'], 'BINARY') or cmp(head['binformat'], 'RI') or
            cmp(head['pointformat'], 'Y')):
        FID.close()
        print('Unable to process IFS file.')
        exit(1)

    # Reading the <Block> part corresponding to the "CURVe" command [TekMan].
    # <Block> = ":CURVE #<x><yy..y><data>"
    # <x> number of bytes defining <yy..y>
    # <yy..y> number of bytes to "transfer"/read in the data part.
    # <data>: the data in binary
    #
    # Comment: It should be happend that: NR_PT times BYT_NR = <yy..y>

    # Skipping the #<x><yy...y> part of the <Block> bytes
    ii = hdata.find(':CURVE #')
    FID.seek(ii + 8)
    skip = int(FID.read(1))
    n1 = int(FID.read(skip))

    # information from the head needed to read and to convert the data
    npts = head['npts']
    yzero = head['yzero']
    ymult = head['ymult']
    xzero = head['xzero']
    xincr = head['xincr']
    ptoff = head['ptoff']
    yoff = head['yoff']

    dict_endian = {  # Dictionary to converts significant bit infor-
        'MSB': '>',  # mation to struct module definitions.
        'LSB': '<'
    }
    fmt = dict_endian[head['byteorder']] + str(npts) + 'h'
    n2 = struct.calcsize(fmt)

    # "n1" is the number of bytes to be readed directly from Tek-ISF-file.
    # Meanwhile "n2" is the number of bytes to be readed calculated through:
    #                    NumOfPoints x BytePerPoint
    if n1 != n2:
        print("WARNING: Something is not going as is was planned!!!")
    FID.close()

    FID = open(filename, 'rb')
    string_data = FID.read(n2)
    data = struct.unpack(fmt, string_data)

    # Absolute values of data obtained as is defined in [Tek-Man] WFMPre:PT_Fmt
    # command description.
    v = [yzero + ymult * (y - yoff) for y in data]
    x = [xzero + xincr * (i - ptoff) for i in range(npts)]

    FID.close()
    return x, v, head


def convert(input_file, output_file):
    x, v, head = isfread(input_file)
    sample_interval = Context(prec=15).create_decimal(head['xincr']).normalize()
    with open(output_file, mode='w') if output_file else sys.stdout as pwlfile:
        timestamp = Decimal("0")
        for val in v:
            timestamp += sample_interval
            pwlfile.write(time_to_str(timestamp) + " " + str(round(val, 12)) + "\n")


def main(argv):
    input_file = None
    output_file = None

    usage = 'isf_to_pwl.py -i <input file> -o <output file>'

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["input_file=", "output_file="])
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

    if input_file is None:
        print(usage)
        sys.exit(2)

    convert(input_file, output_file)


if __name__ == "__main__":
    main(sys.argv[1:])
