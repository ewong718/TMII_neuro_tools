'''
Created on Dec 22, 2014

@author: edmundwong
'''

import pandas as pd
import numpy as np
import pylab as P
import scipy.stats
from scipy import stats
from scipy.stats import norm
import os, sys
import numpy.random as random

os.chdir('/Users/edmundwong/Downloads')

def ttbs_sheet(sheetname):
    vol = pd.read_excel('MDD_FreeSurfer_DTI_Clinical_Master_Sheet.xlsx', sheetname=sheetname)
    allsel = np.array(vol.ix[:,2],dtype='float')>=0
    normsel = np.array(vol.ix[:,2],dtype='float')==0
    dissel = np.array(vol.ix[:,2],dtype='float')>0
    
    #transforms volume data into column-wise z-scores
    for cc in range(3,44):
        test = vol.ix[allsel,cc]
        mean = np.array([np.mean(test)])
        sd = np.array([np.std(test,ddof=1)])
        
        z = stats.zscore(test)
        if cc == 3:
            result = z
            mean_all = mean
            sd_all = sd
        elif cc > 3:
            result = np.column_stack([result,z])
            mean_all = np.concatenate((mean_all,mean))
            sd_all = np.concatenate([sd_all,sd])
    #result = vol.ix[allsel,3:]
    #return sd_all
    dat_f = result.flatten()
    nV = np.prod(dat_f.shape)
    
    Nperm=1000
    Tdist = []
    for pp in range(Nperm):
        bsind = np.random.random_integers(nV-1,size=(nV))
        SP = dat_f[bsind].reshape(result.shape)
        for pp2 in range(0,41):
            zz = SP[:,pp2]
            zz2 = zz*sd_all[pp2]+mean_all[pp2]
            if pp2 == 0:
                zz_all = zz2
            elif pp2 > 0:
                zz_all = np.column_stack([zz_all,zz2])
        SP = zz_all
        Tres = scipy.stats.ttest_ind(SP[dissel],SP[normsel],equal_var=False)
        Tdist.append(Tres[0])
    Tnull = np.array(Tdist).flatten()
    #print Tnull
    h0 = np.median(Tnull)
    Ttests = []
    nomP = []
    for seg_ii in np.arange(SP.shape[1]):
        tt = scipy.stats.ttest_ind(vol.ix[dissel,3+seg_ii].as_matrix(),vol.ix[normsel,3+seg_ii].as_matrix(),equal_var=False) 
        Ttests.append(tt[0])
        nomP.append(tt[1])
    Ttests = list(np.array(Ttests).flatten())
    corP = [1-scipy.stats.percentileofscore(np.abs(Tnull-h0),np.abs(Ttests[seg_ii]-h0))*.01 for seg_ii in np.arange(SP.shape[1])]
    labels = [str(ll) for ll in vol.columns[3:]]
    print nomP
    return corP
    return
    return zip(labels,nomP,corP)


def main():
    sheetnames = pd.ExcelFile('MDD_FreeSurfer_DTI_Clinical_Master_Sheet.xlsx').sheet_names[0:-1]
    print sheetnames
    #for ss in sheetnames:
    bspcor = ttbs_sheet('Segmentation')
        #print ss
    print pd.DataFrame(bspcor)


if __name__ == '__main__':
    sys.exit(main())