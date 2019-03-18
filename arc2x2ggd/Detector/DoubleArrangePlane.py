#!/usr/bin/env python

# this now doesn't assume a box geometry for the subbuilder

import gegede.builder
from arc2x2ggd.Tools import localtools as ltools
from gegede import Quantity as Q
import copy

class DoubleArrangePlaneBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, dx=None, dy=None, dz=None,
                    material=None, NElements1=None, InsideGap1=None,
                    TranspV1=None, Rotation1=None, NElements2=None,
                    InsideGap2=None, TranspV2=None, IndependentVolumes=None, SubBDim=None, **kwds ):
        if halfDimension == None:
            halfDimension = {}
            halfDimension['dx'] = dx
            halfDimension['dy'] = dy
            halfDimension['dz'] = dz
        self.halfDimension, self.material = ( halfDimension, material )
        self.NElements1, self.InsideGap1 = ( NElements1, InsideGap1 )
        self.NElements2, self.InsideGap2 = ( NElements2, InsideGap2 )
        self.TranspV1, self.Rotation1 = ( TranspV1, Rotation1 )
        self.TranspV2, self.IndependentVolumes = ( TranspV2, IndependentVolumes )
        self.SubBDim = SubBDim

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        self.add_volume( main_lv )

        # definition local Rotation
        Rotation1 = geom.structure.Rotation( self.name+'_rot1', str(self.Rotation1[0]),
                                            str(self.Rotation1[1]),  str(self.Rotation1[2]) )

        # get sub-builders and its logic volume
        sb = self.get_builder()
        el_lv = sb.get_volume()

        # get the sub-builder dimension, using its shape
        el_shape = geom.store.shapes.get(el_lv.shape)
        el_dim = [self.SubBDim[0], self.SubBDim[1], self.SubBDim[2]]

        # calculate half dimension of element plus the gap projected to the transportation vector
        sb_dim_v1 = [t*(d+0.5*self.InsideGap1) for t,d in zip(self.TranspV1,el_dim)]
        sb_dim_v2 = [t*(d+0.5*self.InsideGap2) for t,d in zip(self.TranspV2,el_dim)]

        # lower edge, the ule dimension projected on transportation vector
        low_end_v1  = [-t*d+ed for t,d,ed in zip(self.TranspV1,main_hDim,sb_dim_v1)]
        low_end_v2  = [-t*d+ed for t,d,ed in zip(self.TranspV2,main_hDim,sb_dim_v2)]

        for elem2 in xrange(self.NElements2):
            for elem1 in xrange(self.NElements1):
                # calculate the distance for n elements = i*2*halfdinemsion
                temp_v = [elem1*2*d1+elem2*2*d2 for d1,d2 in zip(sb_dim_v1,sb_dim_v2)]
                # define the position for the element based on edge
                temp_v = [te+l1+l2 for te,l1,l2 in zip(temp_v,low_end_v1,low_end_v2)]
                # defining position, placement, and finally insert into the ule.
                el_pos = geom.structure.Position(self.name+"_el"+str(elem1)+'_'+str(elem2)+'_pos',
                                                    temp_v[0], temp_v[1], temp_v[2])
                if  self.IndependentVolumes != None :
                    el_lv_temp = geom.structure.Volume( el_lv.name+str(elem1)+str(elem2),
                                        material=el_lv.material, shape=el_lv.shape, placements=el_lv.placements)
                else:
                    el_lv_temp = el_lv

                el_pla = geom.structure.Placement(self.name+"_el"+str(elem1)+'_'+str(elem2)+'_pla',
                                                    volume=el_lv_temp, pos=el_pos, rot =Rotation1)
                main_lv.placements.append(el_pla.name)
