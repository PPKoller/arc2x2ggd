#!/usr/bin/env python
import gegede.builder
from arc2x2ggd.Tools import localtools as ltools
from gegede import Quantity as Q

# This builder constructs the container for the cryostat.
# This builder also constructs components of the top flange
# It's easier to construct these here since they wrap around 
# the main body.

class ContainerBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, dz=None, rmax=None, rmin=None,
                    positions=None, material=None, **kwds ):
        self.rmin, self.rmax, self.dz = (rmin, rmax, dz)
        self.material = material
        self.positions = positions

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        # container
        cont_shape = geom.shapes.Tubs( self.name, rmin=self.rmin, rmax=self.rmax, dz=self.dz )
        cont_lv = geom.structure.Volume('vol'+cont_shape.name, material=self.material, shape=cont_shape)
        self.add_volume( cont_lv )

        # place the flange and outer wall
        sbs = self.get_builders()

        assert(len(sbs) == len(self.positions))
        for sb, pos in zip(sbs, self.positions):
            sb_lv = sb.get_volume()
            sb_pos = geom.structure.Position(self.name+sb_lv.name+'_pos',
                                             pos[0], pos[1], pos[2])     
            sb_rot = geom.structure.Rotation(self.name+sb_lv.name+'_rot',
                                             '0.0deg', '0.0deg', '0.0deg')                            
            sb_pla = geom.structure.Placement(self.name+sb_lv.name+'_pla',
                                              volume=sb_lv, pos=sb_pos, rot=sb_rot)
            cont_lv.placements.append(sb_pla.name)

