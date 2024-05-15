#################################################################################
#               Python Binary to header file converter                          #
#-------------------------------------------------------------------------------#
#   Author  :   VenkataDurgaPrasad                                              #
#################################################################################

import argparse
import sys
import os

Hdata = []
HDataCnt = 0

def log(msg, *argv):
    if V == 1:
        print (msg)
        for arg in argv:
            print (arg)

def Bin2Header(args):
    global Hdata
    global HDataCnt
    fSize = os.stat(args.input)
    ReadLen = 0
    #log ("File size: {}" .format(fSize.st_size))
    Hdata.append('uint32_t gu32Len = {};\n'.format(fSize.st_size))
    HDataCnt+=1
    Hdata.append('uint8_t gau8Buffer[] = {\ \n')
    HDataCnt+=1
    with open(args.input, 'rb') as in_file:
        while True:
            hexdata = in_file.read(1).hex()
            if len(hexdata) == 0:
                break
            ReadLen+=1
            temp = '0x{}'.format(hexdata)
            Hdata.append(temp)
            HDataCnt+=1
            if ReadLen < fSize.st_size:
                Hdata.append(', ')
                HDataCnt+=1
            if (ReadLen % 16) == 0:
                Hdata.append('\n')
                HDataCnt+=1
        Hdata.append('};\n')
        HDataCnt+=1
        in_file.close()
        #log ("Total datacnt= {}" .format(HDataCnt))
    return 0



def main():
    parser = argparse.ArgumentParser(description='Binary to header file generator')
    parser.add_argument('-i', '--input', required=True , help='Input file')
    parser.add_argument('-o', '--output', required=True , help='Output file')
    parser.add_argument('-v', '--verbose', required=False, action='store_true', help='verbosity')

    args = parser.parse_args()
    if not args:
        return 1

    global V
    if args.verbose:
        V=1
    else:
        V=0

    log ("Input file: \"{}\"" .format(args.input))
    log ("Output file: \"{}\"" .format(args.output))
    log ("converting bin to header...")
    Bin2Header(args)
    log ("Writing header file...")
    with open(args.output, 'w') as f:
        for x in range (0, HDataCnt):
            f.write(Hdata[x])
    log ("Header file \"{}\" created" .format(args.output))

    return 0

if __name__ == '__main__':
    sys.exit(main())


