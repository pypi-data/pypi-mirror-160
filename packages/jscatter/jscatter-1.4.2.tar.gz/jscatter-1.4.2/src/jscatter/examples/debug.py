# -*- coding: utf-8 -*-
#  this file is intended to used in the debugger
# write a script that calls your function to debug it

import numpy as np
import jscatter as js

#
# Look at raw calibration measurement
calibration = js.sas.sasImage(js.examples.datapath+'/calibration.tiff')
bc=calibration.center
calibration.mask4Polygon([bc[0]+8,bc[1]],[bc[0]-8,bc[1]],[bc[0]-8+60,0],[bc[0]+8+60,0])
# mask center
calibration.maskCircle(calibration.center, 18)
# mask outside shadow
calibration.maskCircle([500,320], 280,invert=True)
# calibration.show(axis='pixel',scale='log')
cal=calibration.radialAverage()

# lattice from crystallographic data in cif file.
agbe=js.sf.latticeFromCIF(js.examples.datapath + '/1507774.cif',size=[0,0,0])
sfagbe=js.sf.latticeStructureFactor(cal.X, lattice=agbe,
                                   domainsize=50, rmsd=0.001, lg=1, hklmax=17,wavelength=0.15406)

# simplified model of planes
ag = js.sas.AgBeReference(q=sfagbe.X, wavelength=0.13414, n=np.r_[1:14], domainsize=50)

p=js.grace()
p.plot(cal)
# add scaling and background (because of unscaled raw data)
p.plot(sfagbe.X,190*sfagbe.Y+1.9,sy=0,li=[1,3,4])
p.plot(ag.X, ag.Y*4+1.9, sy=0, li=[1,3,5])
p.yaxis(scale='log',label='I(q) / counts/pixel')
p.xaxis(scale='log',label='q / nm|S-1',min=0.7,max=20)
p.title('AgBe reference measurements')

