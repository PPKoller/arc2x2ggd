#!/usr/bin/env python
import gegede.builder
from arc2x2ggd.Tools import localtools as ltools
from gegede import Quantity as Q

class RectBarBuilder(gegede.builder.Builder):

    def configure( self, halfDimension=None, dx=None, dy=None, dz=None,
                         material=None,  auxParams=None, **kwds ):
        self.material, self.auxParams = ( material, auxParams )
        if halfDimension == None:
            halfDimension = {}
            halfDimension['dx'] = dx
            halfDimension['dy'] = dy
            halfDimension['dz'] = dz
        self.halfDimension = halfDimension

    def construct( self, geom ):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")

        if self.auxParams != None:
            ltools.addAuxParams( self, main_lv )

        self.add_volume( main_lv )
