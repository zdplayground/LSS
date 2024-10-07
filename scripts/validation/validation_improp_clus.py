import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import os
import sys
import argparse

import fitsio
from astropy.table import join,Table
import healpy as hp

from LSS.imaging import densvar
from LSS import common_tools as common



parser = argparse.ArgumentParser()
parser.add_argument("--basedir", help="base directory for catalogs",default='/dvs_ro/cfs/cdirs/desi/survey/catalogs/')
parser.add_argument("--version", help="catalog version",default='test')
parser.add_argument("--survey", help="e.g., main (for all), DA02, any future DA",default='DA2')
parser.add_argument("--tracers", help="all runs all for given survey",default='all')
parser.add_argument("--extra_dir",help="string to add on the end of the directory path for the location of unblinded clustering catalogs",default='nonKP/')
parser.add_argument("--weight_col", help="column name for weight",default='WEIGHT_SYS')
parser.add_argument("--mapmd", help="set of maps to use",default='validate')
parser.add_argument("--verspec",help="version for redshifts",default='kibo-v1')
parser.add_argument("--data",help="LSS or mock directory",default='LSS')
parser.add_argument("--ps",help="point size for density map",default=1,type=float)
parser.add_argument("--test",help="if yes, just use one map from the list",default='n')
parser.add_argument("--nran",help="number of random files to use",default=1)
parser.add_argument("--dpi",help="resolution in saved density map in dots per inch",default=90,type=int)
args = parser.parse_args()

nside,nest = 256,True


indir = args.basedir+args.survey+'/'+args.data+'/'+args.verspec+'/LSScats/'+args.version+'/'
outdir = indir+'plots/imaging/'
outdir = outdir.replace('dvs_ro','global')
outdir_txt = outdir+'ngalvsysfiles/'
print('writing to '+outdir)

if not os.path.exists(outdir_txt):
    os.makedirs(outdir_txt)



tps = [args.tracers]
#fkpfac_dict = {'ELG_LOPnotqso':.25,'BGS_BRIGHT':0.1,'QSO':1.,'LRG':0.25}
if args.tracers == 'all':
    tps = ['LRG','ELG_LOPnotqso','QSO','BGS_BRIGHT-21.5']
    

zdw = ''#'zdone'

regl = ['S','N']
clrs = ['r','b']

all_maps = ['CALIB_G',
 'CALIB_R',
 'CALIB_Z',
 'STARDENS',
 'HALPHA',
 'EBV',
 'EBV_CHIANG_SFDcorr',
 'EBV_MPF_Mean_FW15',
 'EBV_SGF14',
 'BETA_ML',
 'HI',
 'KAPPA_PLANCK',
 'PSFDEPTH_G',
 'PSFDEPTH_R',
 'PSFDEPTH_Z',
 'GALDEPTH_G',
 'GALDEPTH_R',
 'GALDEPTH_Z',
 'PSFDEPTH_W1',
 'PSFDEPTH_W2',
 'PSFSIZE_G',
 'PSFSIZE_R',
 'PSFSIZE_Z']


 
all_dmaps = [('EBV','EBV_MPF_Mean_FW15'),('EBV','EBV_SGF14')]


sky_g = np.zeros(256*256*12)
sky_r = np.zeros(256*256*12)
sky_z = np.zeros(256*256*12)
f = fitsio.read('/dvs_ro/cfs/cdirs/desi/users/rongpu/imaging_mc/ism_mask/sky_resid_map_256_north.fits')
pixr = f['HPXPIXEL']
pix_nest = hp.ring2nest(256,pixr)
for i in range(0,len(f)):
    pix = pix_nest[i]#f['HPXPIXEL'][i]
    sky_g[pix] = f['sky_median_g'][i]
    sky_r[pix] = f['sky_median_r'][i]
    sky_z[pix] = f['sky_median_z'][i]
f = fitsio.read('/dvs_ro/cfs/cdirs/desi/users/rongpu/imaging_mc/ism_mask/sky_resid_map_256_south.fits')
pix = f['HPXPIXEL']
pix_nest = hp.ring2nest(256,pix)
for i in range(0,len(f)):
    pix = pix_nest[i]#f['HPXPIXEL'][i]
    sky_g[pix] = f['sky_median_g'][i]
    sky_r[pix] = f['sky_median_r'][i]
    sky_z[pix] = f['sky_median_z'][i]


sag = np.load('/dvs_ro/cfs/cdirs/desi/survey/catalogs/extra_regressis_maps/sagittarius_stream_256.npy')
do_lrgmask = 'n'
if args.mapmd == 'all':
    maps = all_maps
    dmaps = all_dmaps
    dosag = 'y'
    dosky_g = 'y'
    dosky_r = 'y'
    dosky_z = 'y'
    do_ebvnew_diff = 'y'
    do_lrgmask = 'y'
    do_ebvnocib_diff = 'y'
    

if do_lrgmask == 'y':
    lrg_mask_frac = np.zeros(256*256*12)
    ranmap = np.zeros(256*256*12)
    ranmap_lmask = np.zeros(256*256*12)
    randir = '/dvs_ro/cfs/cdirs/desi/target/catalogs/dr9/0.49.0/randoms/resolve/'
    ran = fitsio.read(randir+'randoms-1-0.fits',columns=['RA','DEC'])
    ran_lrgmask = fitsio.read('/dvs_ro/cfs/cdirs/desi/survey/catalogs/main/LSS/randoms-1-0lrgimask.fits')
    th,phi = common.radec2thphi(ran['RA'],ran['DEC'])
    ranpix = hp.ang2pix(256,th,phi,nest=True)
    for pix,mvalue in zip(ranpix,ran_lrgmask['lrg_mask']):
        ranmap[pix] += 1
        if mvalue > 1:
            ranmap_lmask[pix] += 1
    sel = ranmap > 0
    lrg_mask_frac[sel] = ranmap_lmask[sel]/ranmap[sel]


if args.test == 'y':
    maps = [maps[0]] 
    #print(maps)


nbin = 10

def get_pix(ra, dec):
    return hp.ang2pix(nside, np.radians(-dec+90), np.radians(ra), nest=nest)
    
def plot_reldens(parv,pixlg,pixlgw,pixlr,titl='',cl='k',xlab='',yl = (0.8,1.1),desnorm=False):
    wp = pixlr > 0
    wp &= pixlgw*0 == 0
    wp &= parv != hp.UNSEEN

    rh,bn = np.histogram(parv[wp],bins=nbin,weights=pixlr[wp],range=(np.percentile(parv[wp],.1),np.percentile(parv[wp],99.9)))
    dh,_ = np.histogram(parv[wp],bins=bn,weights=pixlg[wp])
    dhw,_ = np.histogram(parv[wp],bins=bn,weights=pixlgw[wp])
    norm = sum(rh)/sum(dh)
    sv = dh/rh*norm
    normw = sum(rh)/sum(dhw)
    svw = dhw/rh*normw

    meancomp = np.mean(1/dcomp)#np.mean(dt_reg['FRACZ_TILELOCID'])
    ep = np.sqrt(dh/meancomp)/rh*norm #put in mean completeness factor to account for completeness weighting
    
    chi2 = np.sum((svw-1)**2./ep**2.)
    chi2nw = np.sum((sv-1)**2./ep**2.)
    bc = []
    for i in range(0,len(bn)-1):
        bc.append((bn[i]+bn[i+1])/2.)
    labnw = r' no imsys weights, $\chi^2$='+str(round(chi2nw,3))
    labw = r'with imsys weights, $\chi^2$='+str(round(chi2,3))
    #print(lab)    
    plt.errorbar(bc,svw,ep,fmt='o',label=labw,color=cl)
    plt.plot(bc,sv,'-',color=cl,label=labnw)
    plt.legend()
    plt.xlabel(xlab)
    plt.ylabel('Ngal/<Ngal> ')

    plt.title(titl+' '+args.weight_col)
    plt.grid()
    plt.ylim(yl[0],yl[1])
    print(xlab,'weighted: '+str(chi2),'unweighted: '+str(chi2nw))
    fname = outdir_txt + 'ngalvs_'+xlab+titl.replace(' ','')+'.txt'
    fname = fname.replace(' - ','')
    fname = fname.replace('<','')
    fo = open(fname,'w')
    for i in range(0,len(bc)):
        fo.write(str(bc[i])+' '+str(svw[i])+' '+str(sv[i])+' '+str(ep[i])+'\n')
    fo.close()
    print('wrote to '+fname)
    return chi2,chi2nw
        

    

for tp in tps:
    
    depthmd = 'GAL'
    if tp == 'QSO':
        depthmd = 'PSF'
    if args.mapmd == 'validate':
        maps = ['STARDENS','EBV_CHIANG_SFDcorr','HI',depthmd+'DEPTH_G',depthmd+'DEPTH_R',depthmd+'DEPTH_Z','PSFDEPTH_W1','PSFDEPTH_W2','PSFSIZE_G','PSFSIZE_R','PSFSIZE_Z']
        dmaps = []
        dosag = 'n'
        dosky_g = 'n'
        dosky_r = 'n'
        dosky_z = 'n'
        do_ebvnew_diff = 'y'
        do_lrgmask = 'n'
        do_ebvnocib_diff = 'n'
        print('doing validation for '+tp)
        
    if tp[:3] == 'ELG' or tp[:3] == 'BGS':
        if 'PSFDEPTH_W1' in maps:
            maps.remove('PSFDEPTH_W1')
    if tp[:3] == 'ELG' or tp[:3] == 'BGS' or tp[:3] == 'LRG':
        if 'PSFDEPTH_W2' in maps:
            maps.remove('PSFDEPTH_W2')

    fcd_ngc = indir+args.extra_dir+tp+zdw+'_NGC_clustering.dat.fits'
    fcd_sgc = indir+args.extra_dir+tp+zdw+'_SGC_clustering.dat.fits'
    dn = fitsio.read(fcd_ngc)
    ds = fitsio.read(fcd_sgc)
    dtot = np.concatenate([dn,ds])
    del dn
    del ds
    
    ranl = []
    for ii in range(0,args.nran):
    
        fcr_ngc = indir+args.extra_dir+tp+zdw+'_'+str(ii)+'_NGC_clustering.ran.fits'
        fcr_sgc = indir+args.extra_dir+tp+zdw+'_'+str(ii)+'_SGC_clustering.ran.fits'
        rn = fitsio.read(fcr_ngc)
        ranl.append(rn)
        rs = fitsio.read(fcrs_sgc)
        ranl.append(rs)
        del rn
        del rs

    rtot = np.concatenate(ranl)


    zcol = 'Z'
    
    mf = {'N':fitsio.read(indir+'hpmaps/'+tpr+zdw+'_mapprops_healpix_nested_nside256_N.fits'),\
    'S':fitsio.read(indir+'hpmaps/'+tpr+zdw+'_mapprops_healpix_nested_nside256_S.fits')}
    zbins = [(0.4,0.6),(0.6,0.8),(0.8,1.1)]
    if tp[:3] == 'ELG':
        zbins = [(0.8,1.1),(1.1,1.6)]
    if tp == 'QSO':
        zbins = [(0.8,1.6),(1.6,2.1),(0.8,2.1)]
    if tp[:3] == 'BGS':
        zbins = [(0.1,0.4)]
    for zb in zbins:
        zmin = zb[0]
        zmax = zb[1]
        selz = dt[zcol] > zmin
        selz &= dt[zcol] < zmax
        zr = str(zmin)+'<z<'+str(zmax)       

        for reg,cl in zip(regl,clrs):
            if args.mapmd == 'validate':
                fo = open(outdir+tp+zr+'_densclusvsall'+'_'+reg+'_'+args.mapmd+args.weight_col+'_chi2.txt','w')
            sel_reg_d = dt['PHOTSYS'] == reg
            sel_reg_r = rt['PHOTSYS'] == reg
            dt_reg = dt[sel_reg_d&selz]
            rt_reg = rt[sel_reg_r&selz]
            
            #reset for every loop through the maps        
            nside,nest = 256,True
            figs = []
            chi2tot = 0
            nmaptot = 0

            dpix = get_pix(dt_reg['RA'],dt_reg['DEC'])
            rpix = get_pix(rt_reg['RA'],rt_reg['DEC'])

            norm_n = np.ones(len(dpix))
            norm_nw = np.ones(len(dpix))
            
            pixlg = np.zeros(nside*nside*12)
            pixlgw = np.zeros(nside*nside*12)
    
            for ii in range(0,len(dpix)):
                pixlg[dpix[ii]] += dt_reg[ii]['WEIGHT_FKP']*dt_reg[ii]['WEIGHT']/dt_reg[ii][args.weight_col]
                pixlgw[dpix[ii]] += dt_reg[ii]['WEIGHT_FKP']*dt_reg[ii]['WEIGHT']
            pixlr = np.zeros(nside*nside*12)
            for ii in range(0,len(rpix)):
                pixlr[rpix[ii]] += rt_reg[ii]['WEIGHT_FKP']*rt_reg[ii]['WEIGHT']

            
            if dosag == 'y' and reg == 'S':
        
                parv = sag
                mp = 'sagstream'
                fig = plt.figure()
                chi2,chi2nw = plot_reldens(parv,pixlg,pixlgw,pixlr,cl=cl,titl=args.survey+' '+tp+zr+' '+reg,xlab=mp,yl=yl,desnorm=desnorm)
                chi2tot += chi2
                nmaptot += 1
                figs.append(fig)
    
            if do_lrgmask == 'y':
                fig = plt.figure()
                parv = lrg_mask_frac
                mp = 'fraction of area in LRG mask'
                
                chi2,chi2nw  = plot_reldens(parv,pixlg,pixlgw,pixlr,cl=cl,xlab=mp,titl=args.survey+' '+tp+zr+' '+reg,yl=yl,desnorm=desnorm)
                figs.append(fig)
                chi2tot += chi2
                nmaptot += 1


            if dosky_g == 'y':
                fig = plt.figure()
                parv = sky_g
                mp = 'g_sky_res'
                
                chi2,chi2nw  = plot_reldens(parv,pixlg,pixlgw,pixlr,cl=cl,xlab=mp,titl=args.survey+' '+tp+zr+' '+reg,yl=yl,desnorm=desnorm)
                figs.append(fig)
                chi2tot += chi2
                nmaptot += 1

            if dosky_r == 'y':
                fig = plt.figure()
                parv = sky_r
                mp = 'r_sky_res'
                
                chi2,chi2nw  = plot_reldens(parv,pixlg,pixlgw,pixlr,cl=cl,xlab=mp,titl=args.survey+' '+tp+zr+' '+reg,yl=yl,desnorm=desnorm)
                figs.append(fig)
                chi2tot += chi2
                nmaptot += 1

            if dosky_z == 'y':
                fig = plt.figure()
                parv = sky_z
                mp = 'z_sky_res'
                
                chi2,chi2nw  = plot_reldens(parv,pixlg,pixlgw,pixlr,cl=cl,xlab=mp,titl=args.survey+' '+tp+zr+' '+reg,yl=yl,desnorm=desnorm)
                figs.append(fig)
                chi2tot += chi2
                nmaptot += 1


            for map_pair in dmaps:
                fig = plt.figure()
                m1 = mf[reg][map_pair[0]]
                m2 = mf[reg][map_pair[1]]
                sel = (m1 == hp.UNSEEN)
                sel |= (m2 == hp.UNSEEN)
                parv = m1-m2
                parv[sel] = hp.UNSEEN
                mp = map_pair[0]+' - '+map_pair[1]
                chi2,chi2nw  = plot_reldens(parv,pixlg,pixlgw,pixlr,cl=cl,yl=yl,xlab=mp,titl=args.survey+' '+tp+zr+' '+reg,desnorm=desnorm)
                chi2tot += chi2
                nmaptot += 1

                figs.append(fig)


        
            for mp in maps:
                fig = plt.figure()
                parv = mf[reg][mp]
                #print(mp)
                #if mp == 'STARDENS':
                #    parv = np.log(parv)
                if reg == 'S' or mp[:5] != 'CALIB':
                    chi2,chi2nw = plot_reldens(parv,pixlg,pixlgw,pixlr,cl=cl,yl=yl,xlab=mp,titl=args.survey+' '+tp+zr+' '+reg,desnorm=desnorm)
                    chi2tot += chi2
                    nmaptot += 1
                    figs.append(fig)
                    if args.mapmd == 'validate':
                        fo.write(str(mp)+' '+str(chi2)+' '+str(chi2nw)+'\n')
    
    
            if do_ebvnew_diff == 'y':
                #dirmap = '/dvs_ro/cfs/cdirs/desicollab/users/rongpu/data/ebv/v0/kp3_maps/'
                dirmap = '/global/cfs/cdirs/desicollab/users/rongpu/data/ebv/desi_stars/kp3_maps/'
                nside = 256#64
                nest = False
                eclrs = ['gr','rz']
                for ec in eclrs:
                    #ebvn = fitsio.read(dirmap+'v1_desi_ebv_'+ec+'_'+str(nside)+'.fits')
                    ebvn = fitsio.read(dirmap+'v1_desi_ebv_'+str(nside)+'.fits')
                    debv = ebvn['EBV_DESI_'+ec.upper()]-ebvn['EBV_SFD_'+ec.upper()]
                    parv = debv
                    fig = plt.figure()
                    chi2,chi2nw = plot_reldens(parv,hp.reorder(pixlg,n2r=True),hp.reorder(pixlgw,n2r=True),hp.reorder(pixlr,n2r=True),cl=cl,xlab='EBV_DESI_'+ec.upper()+' - EBV_SFD',titl=args.survey+' '+tp+zr+' '+reg,desnorm=desnorm)
                    figs.append(fig)
                    if args.mapmd == 'validate':
                        fo.write('EBV_DESI_'+ec.upper()+'-EBV_SFD'+' '+str(chi2)+' '+str(chi2nw)+'\n')

                    chi2tot += chi2
                    nmaptot += 1

            if do_ebvnocib_diff == 'y':
                #dirmap = '/dvs_ro/cfs/cdirs/desicollab/users/rongpu/data/ebv/v0/kp3_maps/'
                dirmap = '/global/cfs/cdirs/desicollab/users/rongpu/data/ebv/desi_stars/kp3_maps/'
                nside = 256#64
                nest = False
                eclrs = ['gr','rz']
                ebvnocib = hp.reorder(mf[reg]['EBV_CHIANG_SFDcorr'],n2r=True)
                for ec in eclrs:
                    #ebvn = fitsio.read(dirmap+'v1_desi_ebv_'+ec+'_'+str(nside)+'.fits')
                    ebvn = fitsio.read(dirmap+'v1_desi_ebv_'+str(nside)+'.fits')
                    debv = ebvn['EBV_DESI_'+ec.upper()]-ebvnocib#-ebvn['EBV_SFD_'+ec.upper()]
                    parv = debv
                    fig = plt.figure()
                    chi2,chi2nw = plot_reldens(parv,hp.reorder(pixlg,n2r=True),hp.reorder(pixlgw,n2r=True),hp.reorder(pixlr,n2r=True),cl=cl,xlab='EBV_DESI_'+ec.upper()+' - EBV_SFDnoCIB',titl=args.survey+' '+tp+zr+' '+reg,desnorm=desnorm)
                    figs.append(fig)
                    if args.mapmd == 'validate':
                        fo.write('EBV_DESI_'+ec.upper()+'-EBV_SFDnoCIB'+' '+str(chi2)+' '+str(chi2nw)+'\n')

                    chi2tot += chi2
                    nmaptot += 1
    
       
            tw = ''
            if args.test == 'y':
                tw = '_test'
            with PdfPages(outdir+tp+zr+'_densclusvsall'+tw+'_'+reg+'_'+args.mapmd+args.weight_col+'.pdf') as pdf:
                for fig in figs:
                    pdf.savefig(fig)
                    plt.close()
            
            print('results for '+tp+zr+' '+reg +' using '+args.weight_col+' weights')
            print('total chi2 is '+str(chi2tot)+' for '+str(nmaptot)+ ' maps')
            if args.mapmd == 'validate':
                fo.write('total chi2 is '+str(chi2tot)+' for '+str(nmaptot)+ ' maps\n')
                fo.close()

    print('done with '+tp)