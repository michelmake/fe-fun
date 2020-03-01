#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 21:35:22 2020

@author: michelmake

Mesh class

"""

import os
import meshio


class Femesh:
    """Mesh class for finite element solver"""

    __author__ = "Michel Make"
    __copyright__ = "Copyright 2020, The FE-Flow Project"
    __credits__ = ["Michel Make"]
    __license__ = "GPL"
    __version__ = "0.0.0"
    __maintainer__ = "Michel"
    __email__ = "michelmake@protonmail.com"
    __status__ = "alpha"

    def __init__(self, file_name, interior_element_type):

        self.file_name = file_name
        self.interior_element_type = interior_element_type
        self.nn = None
        self.nsd = None

        self.points = []
        self.interior_cells = []
        self.interior_regions = []
        self.interior_ne = None
        self.interior_nen = None
        self.interior_element_type_id = None

        self.boundary_cells = []
        self.boundary_regions = []
        self.boundary_ne = None
        self.boundary_nen = None
        self.boundary_element_type = None
        self.boundary_element_type_id = None

        self.mesh = None

    def get_mesh(self):
        """Obtain the mesh for FE solver."""

        # Determine file type and throw exception when not support.
        filename, file_extension = os.path.splitext(self.file_name)
        assert (file_extension == '.msh'), 'Only .msh files are supported, \
            {} files are not supported'.format(file_extension)

        if file_extension == '.msh':
            file_format = 'gmsh'
        else:
            print('Other file formats than gmsh are not yet supported')

        # retrieve mesh using the meshio module
        self.mesh = meshio.read(self.file_name, file_format)

        # store the output in a mesh construct
        if self.interior_element_type == 'triangle':

            self.interior_element_type_id = 1
            self.boundary_element_type_id = 0

            self.boundary_element_type = 'line'

        self.nn = self.mesh.points.shape[0]
        self.nsd = self.mesh.points.shape[1]

        self.interior_regions = \
            self.mesh.cell_data['gmsh:physical'][self.interior_element_type_id]

        self.boundary_regions = \
            self.mesh.cell_data['gmsh:physical'][self.boundary_element_type_id]

        return

    def region_elements(self, element_region):

        print('this routine should return a list containing the element' +
              'numbers of the given region in the future.')

        return

    def coordinate(self, n):
        """Return coordinate of n-th node """

        return self.mesh.points[n]

    def element(self, n, element_type):
        """Return connectivity n-th element of
        element_type (interior or boundary)"""

        if element_type == 'interior':
            connectivity = self.mesh.cells[1][1][n]
        elif element_type == 'boundary':
            connectivity = self.mesh.cells[0][1][n]
        else:
            error_msg = 'Error: requesting connetivity of unkown element ' + \
                        'type: "{}". '.format(element_type) + \
                        'Allowed element_types are: "interior" and "boundary".'
            raise Exception(error_msg)

        return connectivity

    def number_of_elements(self, region_type):
        """Return the number of elements of given
        region_type (interior or boundary)"""

        # TODO: later on this routine should not only take interior or
        # boundary, but also specific regions (like specific subdomain of the
        # domain boundary).

        if region_type == 'interior':
            number_of_elements = self.mesh.cells[1][1].shape[0]
        elif region_type == 'boundary':
            number_of_elements = self.mesh.cells[0][1].shape[0]
        else:
            error_msg = 'Error: requesting number of elements of unkown' + \
                        'region type: "{}". '.format(region_type) + \
                        'Allowed element_regions are: "interior" and ' + \
                        '"boundary".'
            raise Exception(error_msg)
        return number_of_elements

    def number_of_element_nodes(self, region_type):
        """Return the number of element nodes of given
        region_type (interior or boundary)"""

        # TODO: later on this routine should not only take interior or
        # boundary, but also specific regions (like specific subdomain of the
        # domain boundary).

        if region_type == 'interior':
            number_of_elements = self.mesh.cells[1][1].shape[1]
        elif region_type == 'boundary':
            number_of_elements = self.mesh.cells[0][1].shape[1]
        else:
            error_msg = 'Error: requesting num. of element nodes of unkown' + \
                        'region type: "{}". '.format(region_type) + \
                        'Allowed element_regions are: "interior" and ' + \
                        '"boundary".'
            raise Exception(error_msg)
        return number_of_elements

    def get_element(self, element_id, region_id):
        """This is where i left it. Here somehow we need to extract the
        element information based on some input. Right now I'm thinking of
        using this function within a loop over NE and then set an array of
        element objects. This make me think that this function should be in a
        to be created element class. The function should take the mesh object
        and return stuff like element nodes and coordinates, boundary
        conditions element type etc. Later on things like individual quadrules
        etc could also be added"""

        if region_id in [1, 2, 3]:
            element = {'nodes', self.boundary_cells}

        return element
