#!/usr/bin/env python
import gegede.builder
from arc2x2ggd.Tools import localtools as ltools
from gegede import Quantity as Q

class TopBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, dz=None, rmax=None, rmin=None, material=None, shifts=None, **kwds ):
        self.rmin, self.rmax, self.dz = (rmin, rmax, dz)
        self.material = material
        self.shifts = shifts

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        main_shape = geom.shapes.Tubs( self.name, rmin=self.rmin, rmax=self.rmax, dz=self.dz )
        main_lv = geom.structure.Volume('vol'+main_shape.name, material=self.material, shape=main_shape)
        self.add_volume( main_lv )   

        # place the connectors
        sbs = self.get_builders()
        midcon_lv  = sbs[0].get_volume()
        #edgecon_lv = sbs[1].get_volume()

        # place middle connectors
        midZ = -1*main_shape.dz + self.shifts[0][1]
        midR = self.shifts[0][0]

        sb_pos1 = geom.structure.Position(self.name+midcon_lv.name+ '_pos1', midR, Q('0m'), midZ)     
        sb_rot1 = geom.structure.Rotation(self.name+midcon_lv.name+ '_rot1', '0.0deg', '0.0deg', '90.0deg')                            
        sb_pla1 = geom.structure.Placement(self.name+midcon_lv.name+'_pla1', volume=midcon_lv, pos=sb_pos1, rot=sb_rot1)
        main_lv.placements.append(sb_pla1.name)

        sb_pos2 = geom.structure.Position(self.name+midcon_lv.name+ '_pos2', Q('0m'), midR, midZ)     
        sb_rot2 = geom.structure.Rotation(self.name+midcon_lv.name+ '_rot2', '0.0deg', '0.0deg', '0.0deg')                            
        sb_pla2 = geom.structure.Placement(self.name+midcon_lv.name+'_pla2', volume=midcon_lv, pos=sb_pos2, rot=sb_rot2)
        main_lv.placements.append(sb_pla2.name)

        sb_pos3 = geom.structure.Position(self.name+midcon_lv.name+ '_pos3', -1*midR, Q('0m'), midZ)                           
        sb_pla3 = geom.structure.Placement(self.name+midcon_lv.name+'_pla3', volume=midcon_lv, pos=sb_pos3, rot=sb_rot1)
        main_lv.placements.append(sb_pla3.name)

        sb_pos4 = geom.structure.Position(self.name+midcon_lv.name+ '_pos4', Q('0m'), -1*midR, midZ)                             
        sb_pla4 = geom.structure.Placement(self.name+midcon_lv.name+'_pla4', volume=midcon_lv, pos=sb_pos4, rot=sb_rot2)
        main_lv.placements.append(sb_pla4.name)
