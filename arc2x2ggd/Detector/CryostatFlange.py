#!/usr/bin/env python
import gegede.builder
from arc2x2ggd.Tools import localtools as ltools
from gegede import Quantity as Q

class CryostatFlangeBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, dz1=None, dz2=None, rmax=None, rmin1=None, rmin2=None,
                    material=None, positions=None, subtraction=None, **kwds ):
        self.rmin1, self.rmin2, self.rmax, self.dz1, self.dz2 = (rmin1, rmin2, rmax, dz1, dz2)
        self.material = material
        self.subtraction = subtraction

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        # construct the plate, subtract out insertion plate
        fl1_shape = geom.shapes.Tubs( self.name+'FlangeComponent1', rmin=self.rmin1, rmax=self.rmax, dz=self.dz1 )
        fl2_shape = geom.shapes.Tubs( self.name+'FlangeComponent2', rmin=self.rmin2, rmax=self.rmax, dz=self.dz2 )
        flsub_shape = geom.shapes.Box( self.name+'FlangeComponent3', dx=self.subtraction[0], dy=self.subtraction[1], dz=self.subtraction[2])
        
        relpos1 = geom.structure.Position(self.name+'FlangeSubtractionRel_pos', Q('0m'), Q('0m'), Q('0m'))
        relpos2 = geom.structure.Position(self.name+'FlangeComponent2Rel_pos', Q('0m'), Q('0m'), -1*fl1_shape.dz-fl2_shape.dz)

        # subtract insertion plate
        boolean_shape1 = geom.shapes.Boolean( self.name+'FlangeSubtraction', type='subtraction', first=fl1_shape, second=flsub_shape, pos=relpos1)
        # make union of these 
        boolean_shape2 = geom.shapes.Boolean( self.name, type='union', first=boolean_shape1, second=fl2_shape, pos=relpos2)
        boolean_lv = geom.structure.Volume('vol'+boolean_shape2.name, material=self.material, shape=boolean_shape2)
        
        self.add_volume( boolean_lv )      
