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
        longcon_lv  = sbs[0].get_volume()
        innercon_lv = sbs[1].get_volume()

        # place long connectors
        midZ = -1*main_shape.dz + self.shifts[2]
        longR = self.shifts[0]
        rot1 = geom.structure.Rotation(self.name+longcon_lv.name+ '_rot', '0.0deg', '0.0deg', '0.0deg')  

        sb_pos1 = geom.structure.Position(self.name+longcon_lv.name+ '_pos1', -1*longR, Q('0m'), midZ)                               
        sb_pla1 = geom.structure.Placement(self.name+longcon_lv.name+'_pla1', volume=longcon_lv, pos=sb_pos1, rot=rot1)
        main_lv.placements.append(sb_pla1.name)

        sb_pos2 = geom.structure.Position(self.name+longcon_lv.name+ '_pos2', Q('0m'), Q('0m'), midZ)                                 
        sb_pla2 = geom.structure.Placement(self.name+longcon_lv.name+'_pla2', volume=longcon_lv, pos=sb_pos2, rot=rot1)
        main_lv.placements.append(sb_pla2.name)

        sb_pos3 = geom.structure.Position(self.name+longcon_lv.name+ '_pos3', longR, Q('0m'), midZ)                           
        sb_pla3 = geom.structure.Placement(self.name+longcon_lv.name+'_pla3', volume=longcon_lv, pos=sb_pos3, rot=rot1)
        main_lv.placements.append(sb_pla3.name)

        # place inner connectors
        innerR = self.shifts[1]
        steps = [-1*longR, Q('0m'), longR]
        rot2 = geom.structure.Rotation(self.name+innercon_lv.name+ '_rot1', '0.0deg', '0.0deg', '0.0deg')  
        rot3 = geom.structure.Rotation(self.name+innercon_lv.name+ '_rot2', '0.0deg', '0.0deg', '90.0deg')  

        i = 0
        for step in steps:
            i = i + 1
            sb_pos = geom.structure.Position(self.name+innercon_lv.name+ '_pos'+str(i), -1*innerR, step, midZ)
            sb_pla = geom.structure.Placement(self.name+innercon_lv.name+'_pla'+str(i), volume=innercon_lv, pos=sb_pos, rot=rot1)
            main_lv.placements.append(sb_pla.name)
        for step in steps:
            i = i + 1
            sb_pos = geom.structure.Position(self.name+innercon_lv.name+ '_pos'+str(i), innerR, step, midZ)
            sb_pla = geom.structure.Placement(self.name+innercon_lv.name+'_pla'+str(i), volume=innercon_lv, pos=sb_pos, rot=rot1)
            main_lv.placements.append(sb_pla.name)            




       