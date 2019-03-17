#!/usr/bin/env python
import gegede.builder
from arc2x2ggd.Tools import localtools as ltools
from gegede import Quantity as Q

class BottomBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, dz=None, rmax=None, rmin=None,
                    shift=None, material=None, **kwds ):
        self.rmin, self.rmax, self.dz = (rmin, rmax, dz)
        self.material = material
        self.shift = shift

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        # container
        main_shape = geom.shapes.Tubs( self.name, rmin=self.rmin, rmax=self.rmax, dz=self.dz )
        main_lv = geom.structure.Volume('vol'+main_shape.name, material=self.material, shape=main_shape)
        self.add_volume( main_lv )

        # place the legs and connectors
        sbs = self.get_builders()
        leg_lv = sbs[0].get_volume()
        con_lv = sbs[1].get_volume()

        # place legs
        leg_pos1 = geom.structure.Position(self.name+leg_lv.name+ '_pos1', shift, Q('0m'), Q('0m'))     
        leg_rot1 = geom.structure.Rotation(self.name+leg_lv.name+ '_rot1', '0.0deg', '0.0deg', '0.0deg')                            
        leg_pla1 = geom.structure.Placement(self.name+leg_lv.name+'_pla1', volume=leg_lv, pos=leg_pos1, rot=leg_rot1)
        main_lv.placements.append(leg_pla1.name)

        leg_pos2 = geom.structure.Position(self.name+leg_lv.name+ '_pos2', Q('0m'), shift, Q('0m'))     
        leg_rot2 = geom.structure.Rotation(self.name+leg_lv.name+ '_rot2', '0.0deg', '0.0deg', '0.0deg')                            
        leg_pla2 = geom.structure.Placement(self.name+leg_lv.name+'_pla2', volume=leg_lv, pos=leg_pos2, rot=leg_rot2)
        main_lv.placements.append(leg_pla2.name)

        leg_pos3 = geom.structure.Position(self.name+leg_lv.name+ '_pos3', -1*shift, Q('0m'), Q('0m'))     
        leg_rot3 = geom.structure.Rotation(self.name+leg_lv.name+ '_rot3', '0.0deg', '0.0deg', '0.0deg')                            
        leg_pla3 = geom.structure.Placement(self.name+leg_lv.name+'_pla3', volume=leg_lv, pos=leg_pos3, rot=leg_rot3)
        main_lv.placements.append(leg_pla3.name)

        leg_pos4 = geom.structure.Position(self.name+leg_lv.name+ '_pos4', Q('0m'), -1*shift, Q('0m'))     
        leg_rot4 = geom.structure.Rotation(self.name+leg_lv.name+ '_rot4', '0.0deg', '0.0deg', '0.0deg')                            
        leg_pla4 = geom.structure.Placement(self.name+leg_lv.name+'_pla4', volume=leg_lv, pos=leg_pos4, rot=leg_rot4)
        main_lv.placements.append(leg_pla4.name)
