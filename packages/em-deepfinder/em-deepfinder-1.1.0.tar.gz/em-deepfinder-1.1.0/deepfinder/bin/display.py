#!/usr/bin/env python

# =============================================================================================
# DeepFinder - a deep learning approach to localize macromolecules in cryo electron tomograms
# =============================================================================================
# Copyright (C) Inria,  Emmanuel Moebel, Charles Kervrann, All Rights Reserved, 2015-2021, v1.0
# License: GPL v3.0. See <https://www.gnu.org/licenses/>
# =============================================================================================

import os
import sys
from os.path import dirname, abspath, join, basename
import argparse


def main():
    parser = argparse.ArgumentParser(description='Annotate a tomogram.')
    parser.add_argument('-t', action='store', dest='path_tomo', help='path to tomogram')
    parser.add_argument('-l', action='store', dest='path_lmap', help='path to label map')
    args = parser.parse_args()

    # Set deepfindHome to the location of this file
    deepfindHome = dirname(abspath(__file__))
    deepfindHome = os.path.split(deepfindHome)[0] + '/'

    gui_folder = 'pyqt/display/'
    gui_script = 'gui_display.py'

    gui_options = ''
    if args.path_tomo != None:
        gui_options += ' -t ' + args.path_tomo
    if args.path_lmap != None:
        gui_options += ' -l ' + args.path_lmap

    cmd = 'cd ' + deepfindHome + gui_folder + ' ; python ' + gui_script + gui_options

    os.system(cmd)


if __name__ == "__main__":
    main()
