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
import numpy as np


def main():
    # Set deepfindHome to the location of this file
    deepfindHome = dirname(abspath(__file__))
    deepfindHome = os.path.split(deepfindHome)[0] + '/'
    sys.path.append(deepfindHome)

    from deepfinder.utils.params import ParamsGenTarget
    from deepfinder.training import TargetBuilder
    import deepfinder.utils.common as cm
    import deepfinder.utils.objl as ol

    # Define arguments:
    parser = argparse.ArgumentParser(description='Annotate a tomogram.')
    parser.add_argument('-p', action='store', dest='path_params', help='path to params file')
    args = parser.parse_args()

    if args.path_params == None:  # if no args are passed, then open GUI
        gui_folder = 'pyqt/generate_target/'
        gui_script = 'gui_target.py'

        cmd = 'cd ' + deepfindHome + gui_folder + ' ; python ' + gui_script
        os.system(cmd)

    else:
        params = ParamsGenTarget()
        params.read(args.path_params)
        # params.display()

        objl = ol.read_xml(params.path_objl)

        # Initialize target generation task:
        tbuild = TargetBuilder()

        if params.path_initial_vol != '':
            vol_initial = cm.read_array(params.path_initial_vol)
        else:
            vol_initial = np.zeros(params.tomo_size, dtype=np.int8)

        if params.strategy == 'shapes':
            target = tbuild.generate_with_shapes(objl, vol_initial, params.mask_list)
        else:
            target = tbuild.generate_with_spheres(objl, vol_initial, params.radius_list)

        cm.write_array(target, params.path_target)


if __name__ == "__main__":
    main()
