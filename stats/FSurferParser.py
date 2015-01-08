'''
Last modified on Aug 1, 2014

@author: Edmund Wong
'''

import os
import sys
import csv
import glob
import getopt

help_message = """
Provides command line tool for parsing FreeSurfer output aseg.stats files.

Commands
--------
-h, --help
    Prints out this message.

*Mandatory
-i The input directory containing all recon-all FreeSurfer output directories
-o The full filename and path to output csv file
"""


class Usage(Exception):
    def __init__(self, msg=help_message):
        self.msg = msg


def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
    except getopt.error, msg:
        raise Usage()
    for option, value in opts:
        if option in ("-h"):
            raise Usage()
        if option in ("-i"):
            FSinput = value
        if option in ("-o"):
            outputDir = value

    os.chdir(FSinput)

    # Automatic Segmentation: Volume (mm^3)
    createFSCsv("aseg.stats", "aseg.csv", 4, 3, outputDir)

    # LH Cortical Parcellation: Gray Matter Volume (mm^3)
    createFSCsv("lh.aparc.stats", "lh_parc_grayVol.csv", 0, 3, outputDir)

    # RH Cortical Parcellation: Gray Matter Volume (mm^3)
    createFSCsv("rh.aparc.stats", "rh_parc_grayVol.csv", 0, 3, outputDir)

    # LH Cortical Parcellation: Surface Area (mm^2)
    createFSCsv("lh.aparc.stats", "lh_parc_surfArea.csv", 0, 2, outputDir)

    # RH Cortical Parcellation: Surface Area (mm^2)
    createFSCsv("rh.aparc.stats", "rh_parc_surfArea.csv", 0, 2, outputDir)

    # LH Cortical Parcellation: Average Thickness (mm)
    createFSCsv("lh.aparc.stats", "lh_parc_avgThickness.csv", 0, 4, outputDir)

    # RH Cortical Parcellation: Average Thickness (mm)
    createFSCsv("rh.aparc.stats", "rh_parc_avgThickness.csv", 0, 4, outputDir)

    # LH Cortical Parcellation: Integrated Rectified Mean Curvature (mm^-1)
    createFSCsv("lh.aparc.stats", "lh_parc_MeanCurv.csv", 0, 6, outputDir)

    # RH Cortical Parcellation: Integrated Rectified Mean Curvature (mm^-1)
    createFSCsv("rh.aparc.stats", "rh_parc_MeanCurv.csv", 0, 6, outputDir)


def createFSCsv(statsfile, outCsvName, label_col, val_col, outputDir):

    wholeList = list()
    for fsFile in glob.glob("*/stats/" + statsfile):
        subList = list()
        subList.append("Subject")
        f = open(fsFile, "r")
        for line in f:
            if (line[0] != "#"):
                lll = line.split()
                subList.append(lll[label_col])
        wholeList.append(subList)
        break

    for fsFile in glob.glob("*/stats/" + statsfile):
        subList = list()
        f = open(fsFile, "r")
        subList.append(fsFile[0:15])
        for line in f:
            if (line[0] != "#"):
                lll = line.split()
                subList.append(lll[val_col])
        wholeList.append(subList)

    with open(outputDir + "/" + outCsvName, 'wb') as fp:
        a = csv.writer(fp, delimiter=',')
        data = wholeList
        a.writerows(data)

    print "Success. See output file at " + outputDir + "/" + outCsvName


if __name__ == "__main__":
    sys.exit(main())
