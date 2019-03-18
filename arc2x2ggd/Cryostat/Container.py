#!/usr/bin/env python
import gegede.builder
from arc2x2ggd.Tools import localtools as ltools
from gegede import Quantity as Q
import numpy as np

class ContainerBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, dz=None, rmax=None, rmin=None,
                    positions=None, material=None, connectionshifts=None,
                    inletshifts=None, **kwds ):
        self.rmin, self.rmax, self.dz = (rmin, rmax, dz)
        self.material = material
        self.positions = positions
        self.connectionshifts = connectionshifts
        self.inletshifts = inletshifts

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        # container
        cont_shape = geom.shapes.Tubs( self.name, rmin=self.rmin, rmax=self.rmax, dz=self.dz )
        cont_lv = geom.structure.Volume('vol'+cont_shape.name, material=self.material, shape=cont_shape)
        self.add_volume( cont_lv )

        # we will handle the connections and inlets seperately
        sbs = self.get_builders()
        sbs_aux = sbs[-2:]
        inlet_lv = sbs_aux[0].get_volume()
        conn_lv  = sbs_aux[1].get_volume()
        sbs = sbs[:len(self.positions)]

        # place the first components
        for sb, pos in zip(sbs, self.positions):
            sb_lv = sb.get_volume()
            sb_pos = geom.structure.Position(self.name+sb_lv.name+'_pos',
                                             pos[0], pos[1], pos[2])     
            sb_rot = geom.structure.Rotation(self.name+sb_lv.name+'_rot',
                                             '0.0deg', '0.0deg', '0.0deg')                            
            sb_pla = geom.structure.Placement(self.name+sb_lv.name+'_pla',
                                              volume=sb_lv, pos=sb_pos, rot=sb_rot)
            cont_lv.placements.append(sb_pla.name)

        # place the connections
        connR = self.connectionshifts[2]
        connAng = self.connectionshifts[1]
        connZ1 = self.connectionshifts[0]
        connZ2 = self.connectionshifts[3]
        # hard coding here!
        connR2 = connR - Q('9cm')

        pos = [connR*np.cos(connAng), connR*np.sin(connAng), connZ1]  
        rot1 = Q('90.deg') - connAng
        rot2 = Q('90.deg') + connAng

        conn1_pos = geom.structure.Position(self.name+conn_lv.name+'1_pos', pos[0], pos[1], pos[2])     
        conn1_rot = geom.structure.Rotation(self.name+conn_lv.name+'1_rot', '90.0deg', -1*rot1, '0.0deg')                            
        conn1_pla = geom.structure.Placement(self.name+conn_lv.name+'1_pla', volume=conn_lv, pos=conn1_pos, rot=conn1_rot)
        cont_lv.placements.append(conn1_pla.name)

        conn2_pos = geom.structure.Position(self.name+conn_lv.name+'2_pos', pos[0], -1*pos[1], pos[2])     
        conn2_rot = geom.structure.Rotation(self.name+conn_lv.name+'2_rot', '90.0deg', -1*rot2, '0.0deg')                            
        conn2_pla = geom.structure.Placement(self.name+conn_lv.name+'2_pla', volume=conn_lv, pos=conn2_pos, rot=conn2_rot)
        cont_lv.placements.append(conn2_pla.name)

        conn3_pos = geom.structure.Position(self.name+conn_lv.name+'3_pos', connR2, Q('0m'), connZ2)     
        conn3_rot = geom.structure.Rotation(self.name+conn_lv.name+'3_rot', '0.0deg', '-120.0deg', '0.0deg')                            
        conn3_pla = geom.structure.Placement(self.name+conn_lv.name+'3_pla', volume=conn_lv, pos=conn3_pos, rot=conn3_rot)
        cont_lv.placements.append(conn3_pla.name)

        # place the inlets
        inletR   = self.inletshifts[2]
        inletAngs = self.inletshifts[1]
        inletZ   = self.inletshifts[0]

        pos = []
        rot = []
        for ang in inletAngs:
            pos.append([inletR*np.cos(ang), inletR*np.sin(ang), inletZ])  
            rot.append(Q('90deg') + ang)

        for i in range(0,4):            
            inlet_pos = geom.structure.Position(self.name+inlet_lv.name+str(i+1)+'_pos', pos[i][0], -1*pos[i][1], pos[i][2])     
            inlet_rot = geom.structure.Rotation(self.name+inlet_lv.name+str(i+1)+'_rot', '90.0deg', -1*rot[i], '0.0deg')                            
            inlet_pla = geom.structure.Placement(self.name+inlet_lv.name+str(i+1)+'_pla', volume=inlet_lv, pos=inlet_pos, rot=inlet_rot)
            cont_lv.placements.append(inlet_pla.name)



