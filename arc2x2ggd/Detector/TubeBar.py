#!/usr/bin/env python
import gegede.builder
from arc2x2ggd.Tools import localtools as ltools
from gegede import Quantity as Q

class TubeBarBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, rmin=None, rmax=None, dz=None,
                    material=None,  auxParams=None, **kwds ):
        """
        :param halfDimension: halfDimension for the rectangular bar.
        :type halfDimension: dictionary
        :param material: material for the tube bar.
        :type material: defined on World.py.
        :param auxParams: Dictionary to add aux parameters.
        :type auxParams: dictionary
        :returns: None
        """
        if halfDimension == None:
            halfDimension = {}
            halfDimension['rmin'] = rmin
            halfDimension['rmax'] = rmax
            halfDimension['dz'] = dz

        self.halfDimension = halfDimension
        self.material, self.auxParams = ( material, auxParams )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        """
        Construct the geometry for Rectangular Bar.
        :returns: None
        """
        main_lv, main_hDim = ltools.main_lv( self, geom, "Tubs")

        if self.auxParams != None:
            ltools.addAuxParams( self, main_lv )

        self.add_volume( main_lv )
