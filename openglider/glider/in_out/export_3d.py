import math
import numpy
from dxfwrite import DXFEngine as dxf

from openglider.vector import normalize, norm
#from openglider.graphics import Graphics3D, Line


def export_obj(glider, path, midribs=0, numpoints=None, floatnum=6):
    other = glider.copy_complete()
    if numpoints:
        other.numpoints = numpoints
    other.recalc()
    ribs = other.return_ribs(midribs)

    panels = []
    points = []
    numpoints = len(ribs[0])
    for i in range(len(ribs)):
        for j in range(numpoints):
            # Create two Triangles from one rectangle:
            # Start counting from 1; i->row; j->line
            panels.append([i * numpoints + j + 1, i * numpoints + j + 2, (i + 1) * numpoints + j + 2])
            panels.append([(i + 1) * numpoints + j + 1, i * numpoints + j + 1, (i + 1) * numpoints + j + 2])
            # Calculate normvectors
            first = ribs[i + (i < len(ribs) - 1)][j] - ribs[i - (i > 0)][j]  # Y-Axis
            second = ribs[i][j - (j > 0)] - ribs[i][j + (j < numpoints - 1)]
            try:
                points.append((ribs[i][j], normalize(numpy.cross(first, second))))
            except ValueError:
                raise ValueError("vector of length 0 at: i={0}, j={1}: {2}".format(i, j, first))
    # TODO: check!?
    panels = panels[:2 * (len(ribs) - 1) * numpoints - 2]
    # Write file
    with open(path, "w") as outfile:
        for point in points:
            #point = point[0] * [-1, -1, -1], point[1] * [-1, -1, -1]
            # Write Normvector
            outfile.write("vn {0} {1} {2}\n".format(*map(lambda x: round(-x, floatnum), point[1])))
            # Write point
            outfile.write("v {0} {1} {2}\n".format(*map(lambda x: round(-x, floatnum), point[0])))
        for polygon in panels:
            outfile.write("f {0} {1} {2}//{0} {1} {2}\n".format(*polygon))
    return True


def export_json(glider, path=None, midribs=0, numpoints=None, wake_panels=1, wake_length=0.2, *other):
    """
    export json geometry file for panelmethod calculation
    """
    import json  # TODO
    new_glider = glider.copy()
    if numpoints is None:  # Reset in any case to have same xvalues on upper/lower
        numpoints = new_glider.numpoints
    new_glider.numpoints = numpoints

    ribs = []
    for rib in new_glider.ribs:
        # make dicts!
        this_rib = [{"data": p, "wake": False} for p in rib.profile_3d.data]
        for i in range(wake_panels):
            this_rib.append({"data": rib.align([1+(i+1)*wake_length, 0]), "wake": True})
        ribs.append(this_rib)

    panels = [[{"position": i*(numpoints+wake_panels-1)+j} for j in range(numpoints+wake_panels-1)] for i in range(len(ribs))]

    for i in range(len(ribs)):
        for j in range(numpoints+wake_panels-1):
            panels["is_wake"] = j < wake_panels
            panels["nodes"] = [ribs[i][j],
                               ribs[i][j+1],
                               ribs[i+1][j+1],
                               ribs[i+1][j]],
            neighbours = panels["neighbours"] = [None for __ in range(4)]
            neighbours[0] = panels[i][j+1]["position"]
            neighbours[1] = 0
            neighbours[2] = 1
            neighbours[3] = 2

    panels = []
    for i in range(len(new_glider.ribs)-1):
        # compute panels
        for j in range(2*numpoints + wake_panels):  # 2*numpoints+1 points per rib + wake
            panel = {"is_wake": j < wake_panels,
                     "node_no": [i*(2*numpoints+1+wake_panels)+j,
                                 i*(2*numpoints+1+wake_panels)+j+1,
                                 (i+1)*(2*numpoints+1+wake_panels)+j+1,
                                 (i+1)*(2*numpoints+1+wake_panels)+j],
                     "neighbours": [i*(2*numpoints+wake_panels)+j+1,
                                    i*()],
                     }
            panels.append(panel)


    # TODO: compute neighbours

    polygons, points = new_glider.return_polygons(num=midribs)
    config = {"numpoints": len(points),
              "numpanels": len(polygons),
              "cases": [[1, 0, 1]]}  # TODO: insert vinf
    #panels = [{"node_no": nodes, "is_wake": True, "neighbours": [0, 1, 2, 3]} for nodes in polygons]

    with open(path, "w") as json_file:
        json.dump({"config": config, "nodes": points.tolist(), "panels": panels}, json_file, indent=2)

    return True


def export_dxf(glider, path="", midribs=0, numpoints=None, *other):
    outfile = dxf.drawing(path)
    other = glider.copy_complete()
    if numpoints:
        other.numpoints = numpoints
    other.recalc()
    ribs = other.return_ribs(midribs)
    panels = []
    points = []
    outfile.add_layer('RIBS', color=2)
    for rib in ribs:
        outfile.add(dxf.polyface(rib * 1000, layer='RIBS'))
        outfile.add(dxf.polyline(rib * 1000, layer='RIBS'))
    return outfile.save()


def export_apame(glider, path="", midribs=0, numpoints=None, *other):
    other = glider.copy_complete()
    if numpoints:
        other.numpoints = numpoints
    other.recalc()
    ribs = other.return_ribs(midribs)
    #write config
    outfile = open(path, "w")
    outfile.write("APAME input file\nVERSION 3.0\n")
    outfile.write("AIRSPEED " + str(other.data["GESCHWINDIGKEIT"]) + "\n")
    outfile.write("DENSITY 1.225\nPRESSURE 1.013e+005\nMACH 0\nCASE_NUM 1\n")  # TODO: Multiple cases
    outfile.write(str(math.tan(1 / other.data["GLEITZAHL"])) + "\n0\n")
    outfile.write("WINGSPAN " + str(other.span) + "\n")
    outfile.write("MAC 2") # TODO: Mean Choord
    outfile.write("SURFACE " + str(other.area) + "\n")
    outfile.write("ORIGIN\n0 0 0\n")
    outfile.write("METHOD 0\nERROR 1e-007\nCOLLDIST 1e-007\n")
    outfile.write("FARFIELD " + str(5) + "\n")  # TODO: farfield argument
    outfile.write("COLLCALC 0\nVELORDER 2\nRESULTS 1\n1  1  1  1  1  1  1  1  1  1  1  1  1\n\n")
    outfile.write("NODES " + str(len(ribs) * len(ribs[0])) + "\n")

    for rib in ribs:
        for point in rib:
            for coord in point:
                outfile.write(str(coord) + "\t")
            outfile.write("\n")

    outfile.write("\nPANELS " + str((len(ribs) - 1) * (len(ribs[0]) - 1)) + "\n")  # TODO: ADD WAKE + Neighbours!
    for i in range(len(ribs) - 1):
        for j in range(other.numpoints):
            # COUNTER-CLOCKWISE!
            outfile.write(u"1 {0!s}\t{1!s}\t{2!s}\t{3!s}\n".format(i * len(ribs[0]) + j + 1,
                                                                   (i + 1) * len(ribs[0]) + j + 1,
                                                                   (i + 1) * len(ribs[0]) + j + 2,
                                                                   i * len(ribs[0]) + j + 2))

    return outfile.close()


