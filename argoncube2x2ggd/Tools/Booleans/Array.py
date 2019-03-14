#!/usr/bin/env python
import gegede.builder
from argoncube2x2ggd.Tools import localtools as ltools
from gegede import Quantity as Q

class ArrayBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, material=None, InsideGap=None,
                    AuxParams=None, TranspV=None, UserPlace=None, Boolean=None, **kwds ):
        self.halfDimension, self.material = ( halfDimension, material )
        self.InsideGap, self.TranspV = ( InsideGap, TranspV )
        self.UserPlace, self.Boolean = ( UserPlace, Boolean )
        self.AuxParams = AuxParams

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")

        TranspV = [0,0,1]
        if  self.TranspV != None:
            TranspV = self.TranspV
            ltools.placeBooleanBuilders( self, geom, main_lv, TranspV )
