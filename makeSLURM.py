#!/usr/bin/env python3

"""
script to generate SLURM file for RPKI validator & router testing
generates a SLURM file with an arbitrary number of prefix assertions
specifically, we'll generate prefix/ASN combo with comment.
We'll use the private ASN range (4200000000 - 4294967294) and the IPv6 doc range (2001:DB8::/32)
We'll create a unique ASN / v6 prefix pair, so we're limited to 94,967,294 (the size of the private ASN range)
"""

import json
from argparse import ArgumentParser
from collections import defaultdict
import ipaddress
from math import ceil, log
from sys import exit

# find out how many entries to make
parser = ArgumentParser(description="Generate a SLURM files with <COUNT> number of prefix assertions")

parser.add_argument('count', type=int, help="the number of assertions to generate")

args = parser.parse_args()

count = args.count

if args.count > 94967294:
    answer = input("You asked for more entries that I can make.  Continue with max (94967294) (y/n)?")
    if answer.lower().strip()[0] == "y":
        count = 94967294
    else:
        exit("sorry.  I'm a simple script.  I can only make a SLURM file with a maximum of 94967294 entries.")


def genV6list(incount):
    """
    generate a list of IPv6 prefixes based on the number of entries we need
    it will be easier to make a list initially bigger than needed (ie- the minimum number of prefixes
    that will meet the requirement), then cut it down.
    For example, if we need 33 SLURM entries, we'll create a prefix list of 64, because that is the smallest
    binary increment that satisfies the requirement
    :param incount:
    :return: list of prefixes
    """
    mask_diff = ceil(log(incount, 2))
    listOfNetworks = list(ipaddress.ip_network('2001:DB8::/32').subnets(prefixlen_diff=mask_diff))
    return listOfNetworks[0:incount]


def genTuples(inListOfNetworks):
    """
    generate a list of tuples (ASN, prefix, comment)
    :param incount: number of entries to make
    :param inListOfNetworks: list of IPv6 networks
    :return: list of tuples
    """
    range_end = len(inListOfNetworks) + 4200000000
    listOfEntries = []
    for i in range(4200000000, range_end):
        adjusted_index = i - 4200000000
        entry = (i, str(inListOfNetworks[adjusted_index]), "comment_" + str(i))
        listOfEntries.append(entry)
    return listOfEntries


def genSLURM_dict(intuples):
    """
    now that we have a list of tuples, we need to form a dictionary which will then be dumped as a
    properly formatted SLURM JSON file
    :param intuples:
    :return: SLURMdict
    """
    listToAppend = []
    slurmDict = defaultdict()
    slurmDict['slurmVersion'] = 1
    slurmDict['validationOutputFilters'] = {'prefixFilters': [], 'bgpsecFilters': []}
    slurmDict['locallyAddedAssertions'] = []
    for entry in intuples:
        dictToAppend = {'asn': entry[0], 'prefix': entry[1], 'comment': entry[2]}
        listToAppend.append(dictToAppend)
    slurmDict['locallyAddedAssertions'] = {'prefixAssertions': listToAppend, 'bgpsecAssertions': []}
    return slurmDict


def createSLURM(inDict):
    """
    create the SLURM file
    :param inDict:
    :return: nothing, create file
    """
    filename = "SLURM_" + str(len(inDict['locallyAddedAssertions']['prefixAssertions']))
    with open(filename, 'w') as outfile:
        json.dump(inDict, outfile)


def main():
    v6List = genV6list(count)
    slurm_tuples = genTuples(v6List)
    slurmDict = genSLURM_dict(slurm_tuples)
    createSLURM(slurmDict)


main()
