'''
Last modified on Jan 8, 2015

@author: Edmund Wong
'''

import os
import glob
import sys
import getopt

help_message = """
Provides interface to run Freesurfer batch processing on Minerva LSF job scheduler.
Includes capability to run parcellation of Hippocampal subfields
Allocates for full 24-hour walltime using 12 server nodes.

Commands
--------
-h, --help
    Prints out this message.

*Mandatory
-i The input directory containing all structural nii.gz files
-o The FreeSurfer output directory
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
            inputDir = value
        if option in ("-o"):
            outputdir = value

    mylist = glob.glob(inputDir + "/*.nii.gz")

    for structScan in mylist:
        subID = structScan[:-7] + "_FSurfer"
        subID = subID[43:]
        lsf_file = outputdir + subID + "_run.lsf"
        with open(lsf_file, 'w') as bp:
            bp.write("#!/bin/bash" + os.linesep)
            bp.write("module load freesurfer" + os.linesep)
            bp.write(". $FREESURFER_HOME/SetUpFreeSurfer.sh" + os.linesep + os.linesep)
            bp.write("#BSUB -P scavenger" + os.linesep)
            bp.write("#BSUB -q scavenger" + os.linesep)
            bp.write("#BSUB -n 12" + os.linesep)
            bp.write("#BSUB -W 24:00" + os.linesep)
            bp.write("#BSUB -a openmp" + os.linesep)
            bp.write("#BSUB -o %J.out" + os.linesep + os.linesep)
            bp.write("recon-all -i " + structScan + " -subjid " + subID + " -sd " + outputdir + " -all -hippo-subfields" + os.linesep)
        os.system("bsub <" + lsf_file)

if __name__ == "__main__":
    sys.exit(main())
