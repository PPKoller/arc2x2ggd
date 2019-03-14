#!/usr/bin/env python
import gegede.builder
from argoncube2x2ggd.Tools import localtools as ltools
from gegede import Quantity as Q

class DetectorHallBuilder(gegede.builder.Builder):

    def configure(self, halfDimension=None, dx=None, dy=None, dz=None,
                        material=None, rotation=None, **kwds):
        if halfDimension is None:
            halfDimension = {}
            halfDimension['dx'] = dx
            halfDimension['dy'] = dy
            halfDimension['dz'] = dz
        self.halfDimension = halfDimension
        self.material = material 
        self.rotation = rotation

    def construct(self, geom):
        main_lv, main_hDim = ltools.main_lv(self, geom, "Box")        
        self.add_volume(main_lv)
        
        # sub builders
        sb = self.get_builder()
        det_lv = sb.get_volume()
        det_dim = ltools.getShapeDimensions(det_lv, geom)
        displace = -1*(self.halfDimension['dy'] - det_dim[2]) 
        pos = [Q("0m"),displace,Q("0m")]
        #rot = [Q("0deg"),Q("0deg"),Q("0deg")]
      
        det_pos = geom.structure.Position( det_lv.name+'_pos', pos[0], pos[1], pos[2] )
        det_rot = geom.structure.Rotation( det_lv.name+'_rot', self.rotation[0], self.rotation[1], self.rotation[2] )
        det_pla = geom.structure.Placement( det_lv.name+'_pla', volume=det_lv, pos=det_pos, rot=det_rot )
        main_lv.placements.append( det_pla.name )
        
