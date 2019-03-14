#!/usr/bin/env python
import gegede.builder
from argoncube2x2ggd.Tools import localtools as ltools
from gegede import Quantity as Q

class TubsSubDetectorBuilder(gegede.builder.Builder):

    def configure( self, halfDimension=None, dz=None, rmax=None, rmin=None,
                    material=None, NElements=None, BeginGap=None,
                    InsideGap=None, rotation=None, auxParams=None,
                    TranspV=None, SubBPos=None, positions=None, **kwds ):
        if halfDimension == None:
            halfDimension = {}
            halfDimension['rmin'] = rmin
            halfDimension['rmax'] = rmax
            halfDimension['dz'] = dz
        self.halfDimension, self.material = ( halfDimension, material )
        self.NElements, self.BeginGap = ( NElements, BeginGap )
        self.InsideGap, self.rotation  = ( InsideGap, rotation )
        self.TranspV, self.SubBPos = ( TranspV, SubBPos )
        self.auxParams = auxParams
        self.positions = positions

    def construct( self, geom ):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Tubs")

        if self.auxParams != None:
            ltools.addAuxParams( self, main_lv )

        self.add_volume( main_lv )

        # sub-detectors
        rot = [Q("0deg"),Q("0deg"),Q("0deg")]
        for pos, sb in zip(self.positions, self.get_builders()):
            sb_lv = sb.get_volume()
            p = pos
            p[1] = -1*self.halfDimension['dz']+pos[1]
            print "NAME = ", sb_lv.name
            print "pos = ", p
            sb_pos = geom.structure.Position( sb_lv.name+'_pos', p[0], p[1], p[2] )
            sb_rot = geom.structure.Rotation( sb_lv.name+'_rot', self.rotation[0], self.rotation[1], self.rotation[2] )
            sb_pla = geom.structure.Placement( sb_lv.name+'_pla', volume=sb_lv, pos=sb_pos, rot=sb_rot )
            main_lv.placements.append(sb_pla.name)
            
