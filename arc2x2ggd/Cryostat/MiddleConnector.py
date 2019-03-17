#!/usr/bin/env python
import gegede.builder
from arc2x2ggd.Tools import localtools as ltools
from gegede import Quantity as Q

class MiddleConnectorBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, dx=None, dy=None, dz=None, corner=None, material=None, **kwds ):
        self.dx, self.dy, self.dz = ( dx, dy, dz )
        self.corner = corner
        self.material = material

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        # construct the middle of the plate
        mid_shape = geom.shapes.Box( self.name+'MidComp', dx=self.dx, dy=self.dy, dz=self.dz)
        # construct corner
        cornerdx = 0.5*( self.corner*self.corner*2 )**(0.5)
        corner_shape = geom.shapes.Box( self.name+'CornerComp', dx=cornerdx, dy=cornerdx, dz=self.dz)

        relpos1 = geom.structure.Position(self.name+'Corner1Rel_pos', Q('0m'),    mid_shape.dy, Q('0m'))
        relpos2 = geom.structure.Position(self.name+'Corner2Rel_pos', Q('0m'), -1*mid_shape.dy, Q('0m'))
        relrot = geom.structure.Rotation(self.name+'CornerRel_rot', Q('0deg'), Q('0deg'), Q('45deg'))

        # union
        boolean_shape1 = geom.shapes.Boolean( self.name+'Union1', type='union', first=mid_shape, second=corner_shape, pos=relpos1, rot=relrot)
        boolean_shape2 = geom.shapes.Boolean( self.name+'Union2', type='union', first=mid_shape, second=corner_shape, pos=relpos2, rot=relrot)
        # this is only to fix visualization... 
        boolean_shape3 = geom.shapes.Boolean( self.name+'Union3', type='union', first=boolean_shape1, second=boolean_shape2)

        boolean_lv = geom.structure.Volume('vol'+boolean_shape3.name, material=self.material, shape=boolean_shape3)
        self.add_volume( boolean_lv )
