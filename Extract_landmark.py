# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 10:44:18 2019

@author: sh3190
"""

import nibabel as nib, vtk, numpy as np
import os
def extract_landmarks(path, segmentation_filename, landmarks_filename, labels = [1,2]):
    # """ Extract landmarks from a LVSA nifti segmentation """
    # path: working directory
    # segmentation_filename: name of the segmentation file
    # landmarks_filename: output landmarks filename
    # labels: label numbers of the structures on which you want to compute the lankmarks
    
    # Load the segmentation nifti
    nim = nib.load(os.path.join('patient007_ED.nii'))
    affine = nim.affine
    seg = nim.get_data()
    # Extract the z axis from the nifti header
    lm = []
    z_axis = np.copy(nim.affine[:3, 2])

    # loop on all the segmentation labels of interest
    for l in labels:
        # Determine the z range
        z = np.nonzero(seg == l)[2]
        z_min, z_max = z.min(), z.max()
        z_mid = int(round(0.5 * (z_min + z_max)))

        # compute landmarks positions
        if z_axis[2] < 0:
            # z_axis starts from base
            zs = [z_min, z_mid, z_max]
        else:
            # z_axis starts from apex
            zs = [z_max, z_mid, z_min]

        for z in zs:
            x, y = [np.mean(i) for i in np.nonzero(seg[:, :, z] == l)]
            # x, y = [np.mean(i) for i in np.nonzero(seg[:, :, z, 0] == l)]
            # this might need to be changed depending on the segmentation data structure
            p = np.dot(affine, np.array([x, y, z, 1]).reshape((4, 1)))[:3, 0]
            lm.append(p)

    # Write the landmarks
    points = vtk.vtkPoints()
    for p in lm:
        points.InsertNextPoint(p[0], p[1], p[2])
    poly = vtk.vtkPolyData()
    poly.SetPoints(points)
    writer = vtk.vtkPolyDataWriter()
    writer.SetInputData(poly)
    writer.SetFileName(os.path.join('Y:','landmark'))
    writer.Write()
extract_landmarks('Y:/landmark', 'patient007_ED.nii', 'patient007_frame01_gt.nii.gz', labels = [1,2])