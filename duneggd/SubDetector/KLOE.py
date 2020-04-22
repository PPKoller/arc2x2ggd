#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class KLOEBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, halfDimension=None, Material=None,
                  BField=None, CentralBField=Q("0.0T"), 
                  BuildSTT=False,  BuildGAR=True, **kwds):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.BuildSTT=BuildSTT
        self.BuildGAR=BuildGAR
        
        # The overall logical volume
        self.LVHalfLength=Q("3.1m")
        self.LVRadius=Q("3.6m")
        self.LVMaterial="Air"
        # the CentralBField is really the only configurable parameter
        # since KLOE is already built
        self.CentralBField=CentralBField
        self.SolenoidCoilShellRmin=Q("2.59m")
        # barrel yoke
        self.BarrelHalfLength=Q("2.15m")
        self.BarrelRmax=Q("3.30m")
        self.BarrelRmin=Q("2.93m")
        self.BarrelMaterial="Iron"
        # endcap yoke
        ## endcap B field will be a function of radius...
        # part A is a TUBS  2.58<|x|<2.99m, rmin=.96m, rmax=3.07m
        self.EndcapAZStart=Q("2.58m")
        self.EndcapAZEnd=Q("2.99m")
        self.EndcapARmax=Q("3.07m")
        self.EndcapARmin=Q("0.96m")
        
        # part B is a TUBS, 2.15<|x|<2.58m, rmin=2.78m, rmax=3.30m
        self.EndcapBZStart=Q("2.15m")
        self.EndcapBZEnd=Q("2.58m")
        self.EndcapBRmax=Q("3.30m")
        self.EndcapBRmin=Q("2.78m")

        # part C is a TUBS, 2.15<|x|<2.58m, rmin=0.84m, rmax=1.34m
        self.EndcapCZStart=Q("2.15m")
        self.EndcapCZEnd=Q("2.58m")
        self.EndcapCRmax=Q("1.34m")
        self.EndcapCRmin=Q("0.84m")

        # part D is a TUBS, 1.96<|x|<2.15m, rmin=0.512m, rmax=1.73m
        self.EndcapDZStart=Q("1.96m")
        self.EndcapDZEnd=Q("2.15m")
        self.EndcapDRmax=Q("1.73m")
        self.EndcapDRmin=Q("0.51m")



    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        print( "KLOEBuilder::construct()")
        print( "main_lv = "+ main_lv.name)
        self.add_volume( main_lv )
        self.build_yoke(main_lv,geom)
        self.build_solenoid(main_lv,geom)
        self.build_ecal(main_lv,geom)
        self.build_tracker(main_lv,geom)
        self.build_muon_system(main_lv,geom)
        print( "printing main_lv: "+ str(main_lv))
            
            
#        TranspV = [0,0,1]
#        begingap = ltools.getBeginGap( self )

        # initial position, based on the dimension projected on transportation vector

#        pos = [Q('0m'),Q('0m'),-main_hDim[2]]
        pos = [Q('0m'),Q('0m'),Q('0m')]
#        print( "KLOE subbuilders")
#        for i,sb in enumerate(self.get_builders()):
#            sb_lv = sb.get_volume()
#            print( "Working on ", i, sb_lv.name)
#            sb_dim = ltools.getShapeDimensions( sb_lv, geom )

#            pos[2] = pos[2] + sb_dim[2] + self.InsideGap[i]
            # defining position, placement, and finally insert into main logic volume.
#            pos_name=self.name+sb_lv.name+'_pos_'+str(i)
#            pla_name=self.name+sb_lv.name+'_pla_'+str(i)
#            print( "Position name", pos_name)
#            print( "Placement name", pla_name)
#            sb_pos = geom.structure.Position(pos_name,pos[0], pos[1], pos[2])
#            sb_pla = geom.structure.Placement(pla_name,volume=sb_lv, pos=sb_pos)
#            print( "Appending ",sb_pla.name," to main_lv=",main_lv.name)
#            main_lv.placements.append(sb_pla.name)
    
    def build_yoke(self,main_lv,geom):
        
        #build barrel
        barrel_shape=geom.shapes.Tubs('KLOEYokeBarrel', 
                                      rmin=self.BarrelRmin, 
                                      rmax=self.BarrelRmax, 
                                      dz=self.BarrelHalfLength)
        barrel_lv=geom.structure.Volume('KLOEYokeBarrel_volume', 
                                        material=self.BarrelMaterial, 
                                        shape=barrel_shape)
        ## set magnitude of BarrelBField based on conserved B.dA
        BarrelBField=self.CentralBField*self.SolenoidCoilShellRmin**2/(self.BarrelRmax**2 - self.BarrelRmin**2)
        
#        BField="(0.0 T, 0.0 T, %f T)"%(-BarrelBField/Q("1.0T"))
        BField="(%f T, 0.0 T, 0.0 T)"%(-BarrelBField/Q("1.0T"))
        print( "Setting KLOE Barrel Bfield to "+str(BField))
        barrel_lv.params.append(("BField",BField))


        pos = [Q('0m'),Q('0m'),Q('0m')]
        barrel_pos=geom.structure.Position("KLOEYokeBarrel_pos",
                                           pos[0],pos[1], pos[2])
        barrel_pla=geom.structure.Placement("KLOEYokeBarrel_pla",
                                            volume=barrel_lv,
                                            pos=barrel_pos)
        print( "appending "+barrel_pla.name)
        main_lv.placements.append(barrel_pla.name)
        
        # build endcap
        partv=['A','B','C','D']

        zstartv=[self.EndcapAZStart,self.EndcapBZStart,self.EndcapCZStart,self.EndcapDZStart]
        zendv=[self.EndcapAZEnd,self.EndcapBZEnd,self.EndcapCZEnd,self.EndcapDZEnd]
        rmaxv=[self.EndcapARmax,self.EndcapBRmax,self.EndcapCRmax,self.EndcapDRmax]
        rminv=[self.EndcapARmin,self.EndcapBRmin,self.EndcapCRmin,self.EndcapDRmin]
        for zstart,zend,rmax,rmin,part in zip(zstartv,zendv,rmaxv,rminv,partv):
            name='KLOEYokeEndcap'+part
            for side in ['L','R']:
                name='KLOEYokeEndcap'+part+side
                hl=(zend-zstart)/2.0
                ec_shape=geom.shapes.Tubs(name, 
                                          rmin=rmin, 
                                          rmax=rmax, 
                                          dz=hl)
                ec_lv=geom.structure.Volume(name+'_volume', 
                                            material=self.BarrelMaterial, 
                                            shape=ec_shape)
                pos = [Q('0m'),Q('0m'),Q('0m')]
                pos[2]=(zstart+zend)/2.0
                if side=='L':
                    pos[2]=-pos[2]
                ec_pos=geom.structure.Position(name+"_pos",
                                               pos[0],pos[1], pos[2])
                ec_pla=geom.structure.Placement(name+"_pla",
                                                volume=ec_lv,
                                                pos=ec_pos)
                print( "appending "+ec_pla.name)
                main_lv.placements.append(ec_pla.name)

        

    def build_solenoid(self,main_lv,geom):
        # K.D. Smith, et al., 
        # IEEE Transactions on Applied Superconductivity, v7, n2, June 1997
        # the solenoid has the following major parts
        # cryostat endcaps
        # outer cryostat wall
        # inner crostat wall
        # inner and outer radiation screens
        # coil shell
        # coil

        #self.SolenoidHalfLength=Q("2.15m")
        #self.SolenoidRmin=Q("2.44m") # cryostat inner wall
        #self.SolenoidRmax=Q("2.85m") # cryostat outer wall
        #self.SolenoidRcen=Q("2.60m") # location of the coil's center

        SolenoidHL=Q("2.15m") # halflength of solenoid to outer edge of cryostat        
        # cryostat endcaps
        # rmin=2.43m, rmax=2.88m, thickness=40mm, xcenter=2.15m-40mm/2
        SolenoidECRmin=Q("2.43m")
        SolenoidECRmax=Q("2.88m")
        SolenoidECDz=Q("40mm")
        SolenoidECZloc=SolenoidHL-SolenoidECDz/2.0
        SolenoidECMaterial='Aluminum'

        for side in ['L','R']:
            name='KLOESolenoidCryostatEndcap'+side
            ec_shape=geom.shapes.Tubs(name, 
                                      rmin=SolenoidECRmin, 
                                      rmax=SolenoidECRmax, 
                                      dz=SolenoidECDz/2.0)
            ec_lv=geom.structure.Volume(name+'_volume', 
                                        material=SolenoidECMaterial, 
                                        shape=ec_shape)
            pos = [Q('0m'),Q('0m'),Q('0m')]
            pos[2]=SolenoidECZloc
            if side=='L':
                pos[2]=-pos[2]
            ec_pos=geom.structure.Position(name+"_pos",
                                           pos[0],pos[1], pos[2])
            ec_pla=geom.structure.Placement(name+"_pla",
                                            volume=ec_lv,
                                            pos=ec_pos)        
            print( "appending "+ec_pla.name)
            main_lv.placements.append(ec_pla.name)

        # cryostat inner and outer walls
        SolenoidCryostatRmax=SolenoidECRmax
        SolenoidCryostatRmin=SolenoidECRmin
        SolenoidCryostatHL=SolenoidECZloc=SolenoidHL-SolenoidECDz
        SolenoidCryostatDz=Q("12mm")+Q("3mm") # include radiation screen in wall
        for wall in ['Inner','Outer']:
            name='KLOESolenoidCryostat'+wall+'Wall'
            
            rmax=SolenoidCryostatRmax
            rmin=rmax-SolenoidCryostatDz
            if wall=='Inner':
                rmin=SolenoidCryostatRmin
                rmax=rmin+SolenoidCryostatDz
            hl=SolenoidCryostatHL
            shape=geom.shapes.Tubs(name, 
                                      rmin=rmin, 
                                      rmax=rmax, 
                                      dz=hl)
            lv=geom.structure.Volume(name+'_volume', 
                                        material=SolenoidECMaterial, 
                                        shape=shape)
            pos = [Q('0m'),Q('0m'),Q('0m')]

            pos=geom.structure.Position(name+"_pos",
                                           pos[0],pos[1], pos[2])
            pla=geom.structure.Placement(name+"_pla",
                                            volume=lv,
                                            pos=pos)        
            print( "appending "+pla.name)
            main_lv.placements.append(pla.name)
            

        # coil shell
        
        SolenoidCoilShellRmin=self.SolenoidCoilShellRmin
        SolenoidCoilShellDz=Q("10mm")+Q("1mm") # 1mm Al layer between two coil layers included here
        name='KLOESolenoidCoilShell'

        rmin=SolenoidCoilShellRmin        
        rmax=rmin+SolenoidCoilShellDz

        hl=SolenoidCryostatHL-Q("1cm") # make it a little shorter than the cryostat, 1cm is a wild guess
        shape=geom.shapes.Tubs(name, 
                               rmin=rmin, 
                               rmax=rmax, 
                               dz=hl)
        lv=geom.structure.Volume(name+'_volume', 
                                material=SolenoidECMaterial, 
                                 shape=shape)
        pos = [Q('0m'),Q('0m'),Q('0m')]
        
        pos=geom.structure.Position(name+"_pos",
                                    pos[0],pos[1], pos[2])
        pla=geom.structure.Placement(name+"_pla",
                                     volume=lv,
                                     pos=pos)        
        print( "appending "+pla.name)
        main_lv.placements.append(pla.name)
        
        
        #the coil itself
        SolenoidCoilRmin=SolenoidCoilShellRmin+SolenoidCoilShellDz
        SolenoidCoilDz=Q("10mm") # 1mm Al layer between two coil layers included here
        SolenoidCoilMaterial='Copper' # of course it's some mix, maybe not even including copper. This is a placeholder.
        name='KLOESolenoidCoil'

        rmin=SolenoidCoilRmin        
        rmax=rmin+SolenoidCoilDz

        hl=SolenoidCryostatHL-Q("1cm") # make it a little shorter than the cryostat, 1cm is a wild guess
        shape=geom.shapes.Tubs(name, 
                               rmin=rmin, 
                               rmax=rmax, 
                               dz=hl)
        lv=geom.structure.Volume(name+'_volume', 
                                material=SolenoidCoilMaterial, 
                                 shape=shape)
        pos = [Q('0m'),Q('0m'),Q('0m')]
        
        pos=geom.structure.Position(name+"_pos",
                                    pos[0],pos[1], pos[2])
        pla=geom.structure.Placement(name+"_pla",
                                     volume=lv,
                                     pos=pos)        
        print( "appending "+pla.name)
        main_lv.placements.append(pla.name)

    def build_ecal(self,main_lv,geom):
        # References
        # M. Adinolfi et al., NIM A 482 (2002) 364-386
        # and a talk at the June 2017 ND workshop
        #
        # ECAL is a Pb/SciFi/epoxy sandwich in the volume ratio 42:48:10
        # with an average density of 5.3g/cc
        #
        # fibers are coupled to lightguides at both ends and readout by PMTs
        #
        # BARREL
        # there is a barrel section that is nearly cylindrical, with 24 modules
        # each covering 15 degrees. The modules are 4.3m long, 23cm thick, 
        # trapezoids with bases of 52 and 59 cm.
        
        KLOEBarrelECALHL=Q("2.15m")
        KLOEBarrelECALDepth=Q("23cm")
        KLOEBarrelECALSegmentation=24
        KLOEBarrelECALRmin=Q("2.0m")
        KLOEEcalMaterial='KLOEEcal'
#        segmentation_radians=2*math.pi/KLOEBarrelECALSegmentation
        dphi=Q("360 deg")/KLOEBarrelECALSegmentation

        for iseg in range(0,KLOEBarrelECALSegmentation):
            
            name="KLOEBarrelECAL_"+str(iseg)
            sphi=Q("0 deg")+iseg*dphi          
            
            shape=geom.shapes.Tubs(name, 
                                   rmin=KLOEBarrelECALRmin, 
                                   rmax=KLOEBarrelECALRmin+KLOEBarrelECALDepth, 
                                   dz=KLOEBarrelECALHL,
                                   sphi=sphi, dphi=dphi)
            lv=geom.structure.Volume(name+'_volume', 
                                     material=KLOEEcalMaterial, 
                                     shape=shape)
            pos = [Q('0m'),Q('0m'),Q('0m')]
            
            pos=geom.structure.Position(name+"_pos",
                                        pos[0],pos[1], pos[2])
            pla=geom.structure.Placement(name+"_pla",
                                         volume=lv,
                                         pos=pos)
            print( "appending "+pla.name)
            main_lv.placements.append(pla.name)


        # ENDCAPs
        # there are two endcaps which are 23 cm thick, roughly 2m outer radius,
        # 0.208m inner radius and divided into 32 modules 
        # which run vertically, and curve 90degrees at the end to be read out
        # this is nontrivial to model and will take some work and improvements
        # to gegede
        # just model as a disk with a hole

        KLOEEndcapECALDepth=Q("0.23m")
        KLOEEndcapECALStartZ=Q("1.69m")
        KLOEEndcapECALRmax=Q("2.0m")
        KLOEEndcapECALRmin=Q("20.8cm")
        
        for side in ['L','R']:
            name='KLOEEndcapECAL'+side
            shape=geom.shapes.Tubs(name, 
                                   rmin=KLOEEndcapECALRmin, 
                                   rmax=KLOEEndcapECALRmax, 
                                   dz=KLOEEndcapECALDepth/2.0)
            lv=geom.structure.Volume(name+'_volume', 
                                     material=KLOEEcalMaterial, 
                                    shape=shape)
            pos = [Q('0m'),Q('0m'),Q('0m')]
            pos[2]=KLOEEndcapECALStartZ+KLOEEndcapECALDepth/2.0
            if side=='L':
                pos[2]=-pos[2]
            print( "pos[2]="+str(pos[2]))
            pos=geom.structure.Position(name+"_pos",
                                        pos[0],pos[1], pos[2])
            pla=geom.structure.Placement(name+"_pla",
                                         volume=lv,
                                         pos=pos)
            print( "appending "+pla.name)
            main_lv.placements.append(pla.name)

    def build_tracker(self,main_lv,geom):
        # this is where we will use subbuilders
        name="KLOETrackingRegion"
        KLOETrackingRegionRmin=Q("0m")
        KLOETrackingRegionRmax=Q("2.0m")
        KLOETrackingRegionHL=Q("1.69m")

        # build tracking region logical volume        
        shape=geom.shapes.Tubs(name, 
                               rmin=KLOETrackingRegionRmin, 
                               rmax=KLOETrackingRegionRmax,
                               dz=KLOETrackingRegionHL)
        lv=geom.structure.Volume(name+'_volume', 
                                 material='Air', 
                                 shape=shape)


#        BField="(0.0 T, 0.0 T, %f T)"%(self.CentralBField/Q("1.0T"))
        BField="(%f T, 0.0 T, 0.0 T)"%(self.CentralBField/Q("1.0T"))
        print( "Setting KLOE Central Tracker Bfield to "+str(BField))
        lv.params.append(("BField",BField))
        
        
        # now build the STT inside
        stt_builder=self.get_builder("KLOESTT")
        print "self.BuildSTT==",self.BuildSTT
        print "stt_builder: ",stt_builder
        if (stt_builder!=None) and (self.BuildSTT==True):
            rot = [Q("0deg"),Q("90deg"),Q("0deg")]
            loc = [Q('0m'),Q('0m'),Q('0m')]
            stt_lv=stt_builder.get_volume()
            stt_pos=geom.structure.Position(name+"_KLOESTT_pos",
                                            loc[0],loc[1],loc[2])
            stt_rot=geom.structure.Rotation(name+"_KLOESTT_rot",
                                            rot[0],rot[1],rot[2])
            stt_pla=geom.structure.Placement(name+"_KLOESTT_pla",
                                             volume=stt_lv,pos=stt_pos,
                                             rot=stt_rot)
            lv.placements.append(stt_pla.name)
        
        # or, build the GArTPC
        gar_builder=self.get_builder("KLOEGAR")
        print "self.BuildGAR==",self.BuildGAR
        print "gar_builder: ",gar_builder
        if (gar_builder!=None) and (self.BuildGAR==True):
            rot = [Q("0deg"),Q("0deg"),Q("0deg")]
            loc = [Q('0m'),Q('0m'),Q('0m')]
            gar_lv=gar_builder.get_volume()
            gar_pos=geom.structure.Position(name+"_KLOEGAR_pos",
                                            loc[0],loc[1],loc[2])
            gar_rot=geom.structure.Rotation(name+"_KLOEGAR_rot",
                                            rot[0],rot[1],rot[2])
            gar_pla=geom.structure.Placement(name+"_KLOEGAR_pla",
                                             volume=gar_lv,pos=gar_pos,
                                             rot=gar_rot)
            lv.placements.append(gar_pla.name)
        


        # now place the tracking volume
        pos = [Q('0m'),Q('0m'),Q('0m')]
        pos=geom.structure.Position(name+"_pos",
                                    pos[0],pos[1], pos[2])
        pla=geom.structure.Placement(name+"_pla",
                                     volume=lv,
                                     pos=pos)
        print( "appending "+pla.name)

        main_lv.placements.append(pla.name)


            
    def build_muon_system(self,main_lv,geom):
        pass
