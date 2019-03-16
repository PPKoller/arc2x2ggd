#!/usr/bin/env python
import gegede.builder
from arc2x2ggd.Tools import localtools as ltools
from gegede import Quantity as Q

class CryostatFlangeBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, dz1=None, dz2=None, rmax=None, rmin1=None, rmin2=None,
                    material=None, positions=None, **kwds ):
        self.rmin1, self.rmin2, self.rmax, self.dz1, self.dz2 = (rmin1, rmin2, rmax, dz1, dz2)
        self.material = material

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        # construct the plate, subtract out insertion plate
        fl1_shape = geom.shapes.Tubs( self.name+'FlangeComponent1', rmin=self.rmin1, rmax=self.rmax, dz=self.dz1 )
        fl2_shape = geom.shapes.Tubs( self.name+'FlangeComponent2', rmin=self.rmin2, rmax=self.rmax, dz=self.dz2 )
        
        relpos = geom.structure.Position(self.name+'FlangeComponent2Rel_pos', Q('0m'), Q('0m'), -1*fl1_shape.dz-fl2_shape.dz)

        # make union of these 
        boolean_shape = geom.shapes.Boolean( self.name, type='union', first=fl1_shape, second=fl2_shape, pos=relpos)
        boolean_lv = geom.structure.Volume('vol'+boolean_shape.name, material=self.material, shape=boolean_shape)
        
        self.add_volume( boolean_lv )      

        # place the insertion plate
        sb = self.get_builder()
        sb_lv = sb.get_volume()
        
        sb_pos = geom.structure.Position(self.name+sb_lv.name+'_pos',
                                             Q('0m'), Q('0m'), Q('0m'))     
        sb_rot = geom.structure.Rotation(self.name+sb_lv.name+'_rot',
                                             '0.0deg', '0.0deg', '0.0deg')                            
        sb_pla = geom.structure.Placement(self.name+sb_lv.name+'_pla',
                                              volume=sb_lv, pos=sb_pos, rot=sb_rot)
        boolean_lv.placements.append(sb_pla.name)
