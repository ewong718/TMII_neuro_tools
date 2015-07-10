
'''
Created on Feb 19, 2015

@author: edmundwong
'''

from __future__ import division
from sklearn import svm
import pandas as pd
import sys

def main():
    
    #Variables
    XLSpath = '/Users/edmundwong/Downloads/MDD_v_HC_FreeSurfer_Bootstrap_Machine_Learning_covar.xlsx'
    SheetName = 'Demographic_Clinical_Freesurfer'
    NoSubs = 84
    ft_table_range_start_idx = 2
    ft_table_range_end_idx = 14
    
    #Isolating the data to be analysed
    vol = pd.read_excel(XLSpath, sheetname=SheetName)
    vol = vol[0:NoSubs]
     
    #Initiating Xfull
    Xfull = []
    for idx in range(0,NoSubs):
        vrow = list(vol.iloc[ idx, ft_table_range_start_idx: ft_table_range_end_idx])
        Xfull.append(vrow)
        
        
    #Initiating yfull
    yfull = [ int(x) for x in list(vol.ix[:,1]) ]
    

    no_correct = 0
    no_wrong = 0
    
    #SVM leave-One out cross validation process
    for idx in range(0,NoSubs):
        print "Test# " + str(idx+1) + "/" + str(NoSubs)
        
        X = Xfull[:idx] + Xfull[idx+1 :]
        y = yfull[:idx] + yfull[idx+1 :]
        tset = Xfull[idx]
        testActualGroupVal = yfull[idx]
        
        clf = svm.SVC()
        clf = svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=3,
        gamma=0.0, kernel='rbf', max_iter=-1, probability=False, random_state=None,
        shrinking=True, tol=0.001, verbose=False)
        
        clf.fit(X, y)        
   
        #Print result of iteration (testing)
        outcome = clf.predict(tset)
        print outcome
        
        if outcome == testActualGroupVal:
            no_correct += 1
            print 'Correct.'
            print ''            
        else:
            no_wrong += 1
            print 'Wrong.'
            print ''
            
    #Print overall results
    print "Total Correct: " + str(no_correct)
    print "Total Wrong: " + str(no_wrong)
    print "Accuracy: " + str(round((no_correct/(no_correct + no_wrong))*100,2)) + "%"

    
if __name__ == '__main__':
    sys.exit(main())