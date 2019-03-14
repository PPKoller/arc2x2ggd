#!/usr/bin/env python
import gegede.builder
from argoncube2x2ggd.Tools import localtools as ltools
from gegede import Quantity as Q

class CrossSubDetectorBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, dx=None, dy=None, dz=None,
                    material=None, InsideGap=None, TranspP=None,
                    auxParams=None, RotLeft=None, RotRight=None, RotTop=None,
                    RotBottom=None, **kwds ):

        if halfDimension == None:
            halfDimension = {}
            halfDimension['dx'] = dx
            halfDimension['dy'] = dy
            halfDimension['dz'] = dz
        self.halfDimension, self.material = ( halfDimension, material )
        self.InsideGap, self.TranspP = InsideGap, TranspP
        self.RotLeft, self.RotRight = ( RotLeft, RotRight )
        self.RotTop, self.RotBottom = ( RotTop, RotBottom )
        self.auxParams = auxParams

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")

        if self.auxParams != None:
            ltools.addAuxParams( self, main_lv )

        self.add_volume( main_lv )

        builders = self.get_builders()
        sb_central = builders[0]
        sb_top = builders[1]
        sb_side = builders[2]

        ltools.placeCrossBuilders( main_lv, sb_central, sb_top, sb_side, self, geom )
