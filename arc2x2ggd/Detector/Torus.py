#!/usr/bin/env python
import gegede.builder
from arc2x2ggd.Tools import localtools as ltools
from gegede import Quantity as Q

class TorusBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, rmin=None, rmax=None, rtor=None, 
                         startphi=None, deltaphi=None, material=None, **kwds ):
        self.rmin, self.rmax = ( rmin, rmax )
        self.rtor = rtor
        self.startphi, self.deltaphi = ( startphi, deltaphi )
        self.material = material

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        # define the shape
        main_shape = geom.shapes.Torus( self.name, rmin=self.rmin, rmax=self.rmax, rtor=self.rtor,
                                        startphi=self.startphi, deltaphi=self.deltaphi )
        main_lv = geom.structure.Volume( "vol"+self.name, material=self.material, shape=main_shape )

        self.add_volume( main_lv )
