#!/usr/bin/env python
import gegede.builder
from arc2x2ggd.Tools import localtools as ltools
from gegede import Quantity as Q

class EndCapBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, dz=None, rmax=None, rmin=None,
                   material=None, NElements=None, rotation=None, **kwds ):
        halfDimension = {}
        halfDimension['rmin'] = rmin
        halfDimension['rmax'] = rmax
        halfDimension['dz'] = dz

        self.halfDimension, self.material = ( halfDimension, material )
        self.NElements = NElements

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        main_lv = None
        main_hDim = None
        
        main_lv, main_hDim = ltools.main_lv( self, geom, "Tubs")

        self.add_volume( main_lv )

        '''
        # place sub-builders
        sb = self.get_builder()
        sb_lv = sb.get_volume()
        rotation = geom.structure.Rotation( sb.name+'_rot', '0.0deg', '0.0deg', '0.0deg' )

        sb_pos = geom.structure.Position(self.name+sb_lv.name+'_pos',
                                         Q('0m'), Q('0m'), Q('0m'))
        sb_pla = geom.structure.Placement(self.name+sb_lv.name+'_pla',
                                        volume=sb_lv, pos=sb_pos, rot=rotation)
        main_lv.placements.append(sb_pla.name)
        '''
