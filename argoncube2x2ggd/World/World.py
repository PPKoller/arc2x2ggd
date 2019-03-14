#!/usr/bin/env python
import gegede.builder
from gegede import Quantity as Q
from argoncube2x2ggd.Tools import localtools as ltools
from argoncube2x2ggd.Tools import materialdefinition as materials
from argoncube2x2ggd.Tools import transformationdefinition as transformations

class WorldBuilder(gegede.builder.Builder):

    def configure(self, halfDimension=None, material=None, detEncPosition=None, detEncRotation=None, **kwds):
        self.halfDimension = halfDimension
        self.material = material
        self.detEncPosition = detEncPosition
        self.detEncRotation = detEncRotation

    def construct(self, geom):
        # Construct materials and transformations now
        materials.define_materials(geom)
        transformations.define_transformations(geom)

        # world volume
        world_shape = geom.shapes.Box("world_shape", 
                                      dx=self.halfDimension['dx'], 
                                      dy=self.halfDimension['dy'], 
                                      dz=self.halfDimension['dz'])
        world_vol = geom.structure.Volume("world_vol", material=self.material, shape=world_shape)
        self.add_volume(world_vol)

        # sub volumes 
        sbs   = self.get_builders()
        dh_lv = sbs[0].get_volume()
        dh_dim = ltools.getShapeDimensions(dh_lv, geom)
        ground_lv = sbs[1].get_volume()
        ground_dim = ltools.getShapeDimensions(ground_lv, geom)

        ground_pos = [Q("0m"),-1*ground_dim[1],Q("0m")]
        rot1 = [Q("0deg"),Q("0deg"),Q("0deg")]

        ground_pos = geom.structure.Position( ground_lv.name+'_pos', ground_pos[0], ground_pos[1], ground_pos[2] )
        ground_rot = geom.structure.Rotation( ground_lv.name+'_rot', rot1[0], rot1[1], rot1[2] )
        ground_pla = geom.structure.Placement( ground_lv.name+'_pla', volume=ground_lv, pos=ground_pos, rot=ground_rot )
        world_vol.placements.append(ground_pla.name)

        dh_pos = [Q('0m'),dh_dim[1],Q('0m')]
        rot2 = [Q("0deg"),Q("0deg"),Q("0deg")]


        dethall_pos = geom.structure.Position(dh_lv.name+'_pos', dh_pos[0], dh_pos[1], dh_pos[2])
        dethall_rot = geom.structure.Rotation(dh_lv.name+'_rot', rot2[0], rot2[1], rot2[2])
        dethall_pla = geom.structure.Placement(dh_lv.name+'_pla', volume=dh_lv, pos=dethall_pos,rot=dethall_rot)
        world_vol.placements.append(dethall_pla.name)
