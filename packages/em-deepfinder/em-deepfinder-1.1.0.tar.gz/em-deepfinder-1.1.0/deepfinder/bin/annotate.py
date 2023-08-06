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
    parser.add_argument('-o', action='store', dest='path_objl', help='output path for object list')
    parser.add_argument('-scipion', action='store_true', help='option for launching in scipion (hides some buttons)')
    args = parser.parse_args()

    # Set deepfindHome to the location of this file
    deepfindHome = dirname(abspath(__file__))
    deepfindHome = os.path.split(deepfindHome)[0] + '/'

    gui_folder = 'pyqt/annotation/'
    gui_script = 'gui_annotation.py'

    gui_options = ''
    if args.path_tomo != None:
        gui_options += ' -t ' + args.path_tomo
    if args.path_objl != None:
        gui_options += ' -o ' + args.path_objl
    if args.scipion:
        gui_options += ' -scipion '

    cmd = 'cd ' + deepfindHome + gui_folder + ' ; python ' + gui_script + gui_options

    os.system(cmd)


if __name__ == "__main__":
    main()
