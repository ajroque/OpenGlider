import Graphics as G
import Profile
import Ribs

#ab=P.Profile2D()
#ab.Import("/home/lo/Dropbox/production/paragleiter/profile/nichtaufgeblasen.dat")
#prof=[[i[0],i[1],0.] for i in ab.Profile]
#G.Graphics3D(prof,[G.Line(range(len(prof)))])

##simon debug
p1=Profile.Profile2D()
p1.Import("/home/simon/Dropbox/para-lorenz/paragleiter/profile/nichtaufgeblasen.dat")

rib=Ribs.Rib(profile=p1,glide=7)
rib.AOA=4*3.141/180
rib.arcang=20*3.141/180
rib.zrot=0
print(rib.AOA)
rib.ReCalc()

prof=rib.profile3D.data
rib.AOA=3
rib.ReCalc()
prof2=rib.profile3D.data
G.Graphics3D(prof+prof2,[G.Line(range(len(prof))),G.Line(range(len(prof),len(prof)+len(prof2)))])
neu=rib.profile3D.Flatten()
print(neu)
#from .Ribs import Rib
##import .Profile

####Nothing here yet :(
"""
import Graphics as G
gobj = G.Line([[0,0,1],[0,0,2]])
print(gobj.coordinates)
gobj._SetColour('green')
print(gobj.colour)
>>>>>>> lo:__init__.py
"""