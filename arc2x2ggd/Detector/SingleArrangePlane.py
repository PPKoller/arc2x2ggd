#!/usr/bin/env python
import gegede.builder
from arc2x2ggd.Tools import localtools as ltools
from gegede import Quantity as Q


class SingleArrangePlaneBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, dx=None, dy=None, dz=None,
                    material=None, NElements=None, BeginGap=None,
                    InsideGap=None, rotation=None, TranspV=None, SubBPos=None, **kwds ):
        if halfDimension == None:
            halfDimension = {}
            halfDimension['dx'] = dx
            halfDimension['dy'] = dy
            halfDimension['dz'] = dz
        self.halfDimension, self.material = ( halfDimension, material )
        self.NElements, self.BeginGap = ( NElements, BeginGap )
        self.InsideGap, self.rotation  = ( InsideGap, rotation )
        self.TranspV, self.SubBPos = ( TranspV, SubBPos )
        pass

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        self.add_volume( main_lv )

        if self.NElements != None:
            TranspV = [1,0,0]
            if  self.TranspV != None:
                TranspV = self.TranspV
            ltools.placeBuilders( self, geom, main_lv, TranspV )
        else:
            print( "**Warning, no Elements to place inside "+ self.name)
