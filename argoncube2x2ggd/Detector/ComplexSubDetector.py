#!/usr/bin/env python
import gegede.builder
from argoncube2x2ggd.Tools import localtools as ltools
from gegede import Quantity as Q

class ComplexSubDetectorBuilder(gegede.builder.Builder):

    def configure( self, halfDimension=None, dx=None, dy=None, dz=None, rmax=None, rmin=None,
                    material=None, NElements=None, BeginGap=None,
                    InsideGap=None, rotation=None, auxParams=None, Sensitive=None,
                    TranspV=None, shape=None, **kwds ):
        if halfDimension == None and shape == "Tubs":
            halfDimension = {}
            halfDimension['rmin'] = rmin
            halfDimension['rmax'] = rmax
            halfDimension['dz'] = dz
        else:
            halfDimension = {}
            halfDimension['dx'] = dx
            halfDimension['dy'] = dy
            halfDimension['dz'] = dz
        self.halfDimension, self.material = ( halfDimension, material )
        self.NElements, self.BeginGap = ( NElements, BeginGap )
        self.InsideGap, self.rotation  = ( InsideGap, rotation )
        self.auxParams = auxParams
        self.TranspV = TranspV
        self.shape = shape

    def construct( self, geom ):
        if self.shape == "Tubs":
            main_lv, main_hDim = ltools.main_lv( self, geom, "Tubs")
        else: main_lv, main_hDim = ltools.main_lv( self, geom, "Box")

        if self.auxParams != None:
            ltools.addAuxParams( self, main_lv )

        self.add_volume( main_lv )
        print self.rotation
        if self.NElements != None:
            TranspV = [0,0,1]
            if  self.TranspV != None:
                TranspV = self.TranspV
            ltools.placeComplexBuilders( self, geom, main_lv, TranspV )
        else:
            print( "**Warning, no Elements to place inside "+ self.name)
