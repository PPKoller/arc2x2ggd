#!/usr/bin/env python
# Copying useful class NestedDetectorBuilder
import gegede.builder
from arc2x2ggd.Tools import localtools as ltools
from gegede import Quantity as Q

class NestedSubDetectorBuilder(gegede.builder.Builder):

    ## The configure
    def configure(self, rmax=None, dx=None, dy=None, dz=None, material=None,
                    auxParams=None, Positions=None, **kwds):
        halfDimension = {}
        halfDimension['rmin'] = Q('0m')
        halfDimension['rmax'] = rmax
        halfDimension['dz'] = dz
        self.material, self.Positions = ( material, Positions )
        self.halfDimension, self.auxParams = ( halfDimension, auxParams )

    ## The construct
    def construct(self, geom):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Tubs")

        if self.auxParams != None:
            ltools.addAuxParams( self, main_lv )

        self.add_volume( main_lv )

        builders = self.get_builders()
        second_lv = builders[0].get_volume()
        second_loc = self.Positions[0]
        #third_lv = builders[1].get_volume()
        #third_loc = self.Positions[1]

        #third_pos = geom.structure.Position( third_lv.name+'_pos', third_loc[0], third_loc[1], third_loc[2] )
        #third_pla = geom.structure.Placement( third_lv.name+'_pla', volume=third_lv, pos=third_pos )
        #second_lv.placements.append( third_pla.name )

        second_pos = geom.structure.Position( second_lv.name+'_pos', second_loc[0], second_loc[1], second_loc[2] )
        second_pla = geom.structure.Placement( second_lv.name+'_pla', volume=second_lv, pos=second_pos )
        main_lv.placements.append( second_pla.name )
