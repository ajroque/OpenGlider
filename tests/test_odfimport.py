#! /usr/bin/python2
# -*- coding: utf-8; -*-
#
# (c) 2013 booya (http://booya.at)
#
# This file is part of the OpenGlider project.
#
# OpenGlider is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# OpenGlider is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OpenGlider.  If not, see <http://www.gnu.org/licenses/>.


__author__ = 'simon'
import openglider.Import.ODFImport2 as ODFImport
import unittest
import openglider.Graphics as Graph
import numpy

cells = ODFImport.import_ods("/home/simon/OpenGlider/tests/demokite.ods")


num = 10
ribs = []
for cell in cells:
    for y in range(num):
        ribs.append(cell.midrib(y*1./num).data)
ribs.append(cells[-1].midrib(1.).data)
# ribs is [[point1[x,y,z],[point2[x,y,z]],[point1[x,y,z],point2[x,y,z]]]

# num*cells+1 ribs

points = len(ribs[0])
ribs = numpy.concatenate(ribs)
polygons = []

for i in range(len(cells)*num):  # without +1, because we us i+1 below
    for k in range(points-1):  # same reason as above
        polygons.append(Graph.Polygon([i*points+k, i*points+k+1, (i+1)*points+k+1, (i+1)*points+k]))

Graph.Graphics3D(polygons, ribs)
#Graph.Graphics3D([Graph.Line(x.data) for x in ribs])
"""
class TestODF(unittest.TestCase):
    def setUp(self):
        self.odf = ODFImport.OdfImport("testglider.ods")

    def test_sheetimport(self):
        print(ODFImport.sheettolist(self.odf[0]))

if __name__ == '__main__':
        unittest.main(verbosity=2)
        """