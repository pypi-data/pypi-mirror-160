'''Processing library for PhyAAt dataset ans medeling.

Author: Nikesh Bajaj
Homepage: https://phyaat.github.io, http://nikeshbajaj.in
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, re, random,copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
from scipy import signal
from scipy.signal import butter, lfilter
from joblib import Parallel, delayed
from scipy import stats
from copy import deepcopy
import spkit as sp

#from .artifact_correction import RemoveArtftICA_CBI_Kur_Iso
from . import utils


class Subject(object):
    def __init__(self,subfiles):
        assert 'sigFile' in subfiles.keys()
        assert 'txtFile' in subfiles.keys()
        self.subID = subfiles['sigFile'].split('/')[-2]
        D,S = ReadFile_DS(subfiles)
        self.rawData = {}
        self.rawData['D'] = D
        self.rawData['S'] = S
        self.processed = {}
        self.processed['D'] = D
        self.EEG_proc_level = 0
        self.feature_extraction_count = 0
        self.Xy = {}
    def filter_EEG(self,band =[0.5],btype='highpass',order=5,method='lfilter',fs=128.0,verbose=0,use_joblib=False,n_jobs=-1,useRaw=False):
        '''
        Filter EEG Channels with given filter specifications:
        ----------------------------------------------------
         btype: 'highpass', 'lowpass', 'bandpass', 'bandstop'
         band: [fc1,fc2]  - cut-off frequencies for bandpass and bandstop
               [fc]       - cut-off frequency for lowpass and highpass

         method: 'lfilter', 'filtfilt', 'SOS'
         order:  order of filter (default=5)
         use_joblib: if true, attempt to use joblib for parallel processing of multichannel, if fails, apply filtering one by one
                   : default False, since most system fails to use joblib
        '''
        if useRaw:
            self.processed['D'] = FilterEEG_D(self.rawData['D'],col=range(1,15),band=band,btype=btype,order=order,fs=fs,
                              method=method,verbose=verbose,use_joblib=use_joblib,n_jobs=n_jobs)
        else:
            self.processed['D'] = FilterEEG_D(self.processed['D'],col=range(1,15),band=band,btype=btype,order=order,fs=fs,
                              method=method,verbose=verbose,use_joblib=use_joblib,n_jobs=n_jobs)
        self.EEG_proc_level+=1
    def correct(self,method='ICA',Corr=0.8,KurThr=2,ICAMed='extended-infomax',AF_ch_index =[0,13], F_ch_index=[1,2,11,12],
                        wv='db3', thr_method ='ipr', IPR=[25,75], beta=0.1, k1=10,k2=100, est_wmax=100,
                        theta_a=np.inf, bf=2, gf=0.8, OptMode='soft', wpd_mode='symmetric', wpd_maxlevel=None, factor=1.0,
                        packetwise=False, WPD=True, lvl=[], fs=128.0, use_joblib=False,
                         winsize=128,hopesize=None,verbose=0, window=['hamming',True],winMeth='custom',useRaw=False):
        '''
        Remove Artifacts from EEG using  ATAR Algorithm or ICA
        ------------------------------------------------------
        method: 'ATAR' 'ICA',
        =====================

        # For ICA  parameters (5)
        ---------------------------
        ICAMed : (default='extended-infomax') ['fastICA','infomax','extended-infomax','picard']
        KurThr : (default=2) threshold on kurtosis to eliminate artifact, ICA component with kurtosis above threshold are removed.
        Corr   : (default=0.8), correlation threshold, above which ica components are removed.

        Details:
        ICA based approach uses three criteria
         - (1) Kurtosis based artifacts - mostly for motion artifacts
         - (2) Correlation Based Index (CBI) for eye movement artifacts
         - (3) Correlation of any independent component with many EEG channels

        To remove Eye blink artifact, a correlation of ICs are computed with AF and F

        For case of 14-channels Emotiv Epoc
        ch_names = ['AF3','F7
        PreProntal Channels =['AF3','AF4'], Fronatal Channels = ['F7','F3','F4','F8']
        AF_ch_index =[0,13] :  (AF - First Layer of electrodes towards frontal lobe)
        F_ch_index =[1,2,11,12] : (F - second layer of electrodes)

        if AF_ch_index or F_ch_index is None, CBI is not applied

        for more detail chcek
        import spkit as sp
        help(sp.eeg.ICA_filtering)


        # ATAR Algorithm Parameters
        ---------------------------
        ## default setting of parameters are as follow:
        wv='db3',thr_method ='ipr',IPR=[25,75],beta=0.1,k1=10,k2 =100,est_wmax=100,
        theta_a=np.inf,bf=2,gf=0.8,OptMode ='soft',wpd_mode='symmetric',wpd_maxlevel=None,factor=1.0,
        packetwise=False,WPD=True,lvl=[],fs=128.0,use_joblib=False

        check Ref[1] and jupyter-notebook for details on parameters:
        - https://nbviewer.org/github/Nikeshbajaj/Notebooks/blob/master/spkit/SP/ATAR_Algorithm_EEG_Artifact_Removal.ipynb

        # Common Parameters
        -------------------
        winsize=128, hopesize=None, window=['hamming',True], ReconMethod='custom' (winMeth)
        winsize: 128, window size to processe
        hopesize: 64, overlapping samples, if None, hopesize=winsize//2
        window: ['hamming',True], set window[1]=False to avoid windowing

        References:
        # ATAR
        - [1] Bajaj, Nikesh, et al. "Automatic and tunable algorithm for EEG artifact removal using wavelet decomposition with applications in predictive modeling during auditory tasks." Biomedical Signal Processing and Control 55 (2020): 101624.
        - check jupyter-notebook as tutorial here:
        - https://nbviewer.org/github/Nikeshbajaj/Notebooks/blob/master/spkit/SP/ATAR_Algorithm_EEG_Artifact_Removal.ipynb

        # [2] ICA
         - https://nbviewer.org/github/Nikeshbajaj/Notebooks/blob/master/spkit/SP/ICA_based_Artifact_Removal.ipynb

        '''
        if hopesize is None: hopesize=winsize//2

        if useRaw:
            D = deepcopy(self.rawData['D'])
        else:
            D = deepcopy(self.processed['D'])

        X = np.array(D.iloc[:,1:15]).astype(float)

        if method=='ICA':
            #XR = RemoveArtftICA_CBI_Kur_Iso(X,winsize=winsize,CorrP=Corr,KurThr=KurThr,ICAMed=ICAMed,verbose=verbose,
            #                  window=window,hopesize=hopesize,winMeth=winMeth)
            XR = sp.eeg.ICA_filtering(X,winsize=winsize,ICA_method=ICAMed,kur_thr=KurThr,corr_thr=Corr,AF_ch_index =[0,13],
                 F_ch_index=[1,2,11,12],verbose=True,window=window,hopesize=hopesize,winMeth=winMeth)
        elif method=='ATAR':
            XR = sp.eeg.ATAR(X.copy(),wv=wv, thr_method =thr_method, IPR=IPR, beta=beta, k1=k1,k2=k2, est_wmax=est_wmax,
                            theta_a=theta_a, bf=bf, gf=gf, OptMode=OptMode, wpd_mode=wpd_mode, wpd_maxlevel=wpd_maxlevel, factor=factor,
                            packetwise=packetwise, WPD=WPD, lvl=lvl, fs=fs, use_joblib=use_joblib,
                            winsize=winsize,window=window,hopesize=hopesize,ReconMethod=winMeth,verbose=verbose)
        else:
            print('other metheds are not updated yet, use method="ICA" or "ATAR"')
            assert False

        D.iloc[:XR.shape[0],1:15] = XR
        self.processed['D'] = D
        self.EEG_proc_level+=1
        if verbose: print('')

    def getXy_eeg(self,task=1,features='rhythmic',eSample=[0,0],redo=False,split='serial',
             splitAt=100,normalize=False,log10p1=True,flat=True,filter_order=5,filter_method='lfilter',method='welch',window='hann',
              scaling='density',detrend='constant',period_average='mean',winsize=-1,hopesize=None,fs=128,
              fBands=[],Sum=True, Mean=False, SD=False, use_joblib=False,n_jobs=-1,verbose=0,use_v0=True, useRaw=False,
              include_win_ind=False,redo_warn=True):
        '''
        task    :: int: {1,2,3,4,-1}, if task=-1, it will return label for all tasks e.g. y-shape=(n,4), each column for each task
            task=1 : Attention Level Prediction
            task=2 : Noise Level Prediction
            task=3 : Semanticity Prediction
            task=4 : LWR classification
            task=-1: All four

        features:: str: 'rhythmic', ['wavelet', 'spectorgram', .. ] not implemented yet
                 : 'rhythmic', returns power of 6 frequency bands for each channel for each window or segment

        eSample :: list: [0,0], Extra samples before and after segment, [64,64] will add 64 samples before start and 64 after ends
                 : helpful for ERP analysis

        redo  :: bool: False, to save the computational repetititon. If features from required segments are already extracted,
              will not be extracted again, unless redo=True. If features are extracted for task 1 (listening segments),
              then for task 2 and task 3, not required to compute again, but for task 4 or task=-1, it would compute again.
              If you processed the raw signal again, set redo=True to extract features again.

        split:: str: 'serial', 'random' : Serial split will split the segments in serial temporal order. First 'splitAt' segments
               will be in training set, rest will be in testing set. 'random' split will shuffle the order of segments first
               then split. 'serial' split is to evaluate the predictive of future instances (testing segments) from
               past instances (training segments).

        normalize:: bool: False, if normalize the power of each band to observe the spatial power distribuation of EEG in one band.
            normalizing will loose the relative differences in power among different bands, since sum of total power in
            a band across all the channel will be 1.
        log10p1:: bool: True, compute logrithim power, using log(x+1) to avoid small values getting very high negative values

        flat:: bool: True, to flatten the features from 6x14 to 84, if False, will return shape of features (n,6,14) else (n,84)

        winsize: int -1 or +int, if -1, features will be extracted using Segment-wise framwork or window-wise framework.
                 If winsize=-1: output shape of X will (n,nf), where n = number of segments
                 If winsize>1 : output shape of X will (m,nf), where m = total number of windows from all the segments
                 For details please refere to the article.

        hopesize: if None, =winsize//2, overlapping samples if winsize>1 (window-wise feature extraction)

        Parameters for Computation of spectral power
        -------------------------------------------
        filter_order: 5, order of IIR filter
        filter_method = 'lfilter', 'filtfilt', 'SOS'
        method : 'welch' or None, method for periodogram
        window : 'hann', or scipy.signal.get_window input string e.g. 'ham','box'
        scaling: 'density'--V**2/Hz 'spectrum'--V**2
        detrend: False, 'constant', 'linear'
        average: 'mean', 'median'   #periodogram average method



        use_v0: if True, old version of Rhythmic Feature Extraction is used with limited control over parameters,
                in which case following parameters will be ignored:
                filter_method='lfilter', fBands=[],Sum=True, Mean=False, SD=False, use_joblib=False,n_jobs=-1,verbose=0
                To make use of above parameters, use use_v0=False.


        Paprameters for Rhythmic features: When use_v0==False
        =======================================================
        # For different filtering method
        -------------------------------
        filter_method = 'lfilter', 'filtfilt', 'SOS'

        # For Custum Frequency Bands
        ---------------------------
        fBands = list of frequency bands, if empty then fBands =[[None,4],[4,8],[8,14],[14,30],[30,47],[47, None]]
            for lowpass, use [None, fc] and for highpass use [fc, None]
            example:
            fBands =[[None,8],[8,16],[24,None]] for three custum frequency bands

        # For aggregating Power as Sum, Mean or/and SD
        -------------------------------------------------
        (Sum=True,Mean=False,SD=False) To compute, sum of total power, mean of total power or/and SD of total power in specified frequency band
         - At least one of them should be True
         - For more than one true, features are concatenated as additional axis in order of Sum, Mean, SD

         # To use parallel processing for fast computation
         use_joblib=False,n_jobs=-1

         Output
         ======
         X_train,y_train,X_test,y_test

         shape:  X_train, X_test:  (nW, len(fBands), nch)
                 where nW is number of windows used. if winsize==-1, then nW=nSegments, feature are extracted segment-wise
                 len(fBands) is number of frequency bands specified in fBands, if empty list was passed, then 6 frequency bands are used by default
                 nch is number of channels
            if more than one of (Sum,Mean,SD) is True, then shapes are:
                 X_train, X_test:  (nW,aggN ,len(fBands), nch)
                 where aggN=2 or three, and they are ordered as [Sum,Mean,SD]
            if flat True:
                Then last two dimensions are flattened, e.g. (nW, len(fBands)*nch) or (nW,aggN,len(fBands)*nch)

        shape:  y_train, y_test: (nW,) corresponding label for chosen task (1,2,3,4)
                if winsize>16, and include_win_ind=True,
                y_train, y_test: (nW,2), where first column will be label of corresponding task, and second column will be
                index of a window within a segment

                For example: if a listening segment is 5 sec long and selected winsize=128, (1sec), with 0.5sec overlapping, then there will
                5+4 =9 windows within this segment, for each window, index will be such as  0,1,2,3, ...8. and it will start again from 0 for
                next segment.

                This can be useful for temporal models such as RNN, where you like to provid all the windows of one segment as a sequence

            if task =-1:
                shape = (nW,5), where first 4-columns are labels for first four tasks (At_level, Noise_level, Semanticity, LWR)
                5th column is a sequence of window within a segment, which is useful only when winsize>16, else 5th column will be all zeros



        '''
        if self.feature_extraction_count>1:
            if redo_warn:
                print('If you are running feature extraction with DIFFERENT parameters again to recompute, set redo=True, else function will return pre-computed features, if exist')
                print('To suppress this warning2, set redo_warn=False')

        if winsize>1: hopesize =winsize//2

        if task in [4,-1] and 'task' in self.Xy.keys() and self.Xy['task'] not in [4,-1]:
            redo = True

        if redo or 'X_train' not in self.Xy.keys():
            D = self.rawData['D'] if useRaw else self.processed['D']
            #D = self.processed['D'] if 'D' in self.processed.keys() else
            L,W,R,Scores,cols = Segments(D,self.rawData['S'],LabelCol =-2,eSample=eSample,verbose=verbose==2)

            if split=='random':
                Ind = np.arange(len(L))
                np.random.shuffle(Ind)
                L  = [L[ind] for ind in Ind]
                Scores = [Scores[ind] for ind in Ind]
                if len(W)!=len(L):
                    Ind = np.arange(len(W))
                    np.random.shuffle(Ind)
                W = [W[ind] for ind in Ind]
                if len(R)!=len(W):
                    Ind = np.arange(len(R))
                    np.random.shuffle(Ind)
                R = [R[ind] for ind in Ind]

            if task!=4 and task!=-1:
                Xt,yt = Extract_featuresEEG(Sg=[L[:splitAt]],Scores=Scores[:splitAt],feature=features,offset=eSample[0],
                            winsize=winsize,hopesize=hopesize,normalize=normalize,log10p1=log10p1,flat=flat,fs=fs,
                            order=filter_order,filter_method=filter_method,method=method,window=window,
                            scaling=scaling, average=period_average,detrend=detrend,
                            fBands=fBands,Sum=Sum, Mean=Mean, SD=SD, use_joblib=use_joblib,n_jobs=n_jobs,verbose=verbose,use_v0=use_v0)

                Xs,ys = Extract_featuresEEG(Sg=[L[splitAt:]],Scores=Scores[splitAt:],feature=features,offset=eSample[0],
                            winsize=winsize,hopesize=hopesize,normalize=normalize,log10p1=log10p1,flat=flat,fs=fs,
                            order=filter_order,filter_method=filter_method,method=method,window=window,
                            scaling=scaling, average=period_average,detrend=detrend,
                            fBands=fBands,Sum=Sum, Mean=Mean, SD=SD, use_joblib=use_joblib,n_jobs=n_jobs,verbose=verbose,use_v0=use_v0)
            else:
                Xt,yt = Extract_featuresEEG(Sg=[L[:splitAt],W[:splitAt],R[:splitAt]],Scores=Scores[:splitAt],
                        feature=features,offset=eSample[0],winsize=winsize,hopesize=hopesize,
                        normalize=normalize,log10p1=log10p1,flat=flat,fs=fs,order=filter_order,filter_method=filter_method,method=method,
                        window=window,scaling=scaling, average=period_average,detrend=detrend,
                        fBands=fBands,Sum=Sum, Mean=Mean, SD=SD, use_joblib=use_joblib,n_jobs=n_jobs,verbose=verbose,use_v0=use_v0)
                Xs,ys = Extract_featuresEEG(Sg=[L[splitAt:],W[splitAt:],R[splitAt:]],Scores=Scores[splitAt:],
                        feature=features,offset=eSample[0],winsize=winsize,hopesize=hopesize,
                        normalize=normalize,log10p1=log10p1,flat=flat,fs=fs,order=filter_order,filter_method=filter_method,method=method,
                        window=window,scaling=scaling, average=period_average,detrend=detrend,
                        fBands=fBands,Sum=Sum, Mean=Mean, SD=SD, use_joblib=use_joblib,n_jobs=n_jobs,verbose=verbose,use_v0=use_v0)

            self.Xy = {'X_train':Xt,'y_train':yt,'X_test':Xs,'y_test':ys,'task':task}

        Xt,yt = self.Xy['X_train'], self.Xy['y_train']
        Xs,ys = self.Xy['X_test'], self.Xy['y_test']

        if task==-1:
            y_train = yt
            y_test  = ys
            X_train = copy.deepcopy(Xt)
            X_test  = copy.deepcopy(Xs)
            return X_train,y_train,X_test,y_test

        if task==4:# LWR task
            if include_win_ind and winsize>0:
                y_train = yt[:,3:].astype(int)
                y_test  = ys[:,3:].astype(int)
            else:
                y_train = yt[:,3].astype(int)
                y_test  = ys[:,3].astype(int)
            X_train = copy.deepcopy(Xt)
            X_test  = copy.deepcopy(Xs)
        else:
            ind1 = np.where(yt[:,3]==0)[0]
            ind2 = np.where(ys[:,3]==0)[0]
            X_train = copy.deepcopy(Xt[ind1])
            X_test  = copy.deepcopy(Xs[ind2])
            if task==3: #Semanticity
                if include_win_ind and winsize>0:
                    y_train = yt[ind1][:,[2,4]].astype(int)
                    y_test  = ys[ind2][:,[2,4]].astype(int)
                else:
                    y_train = yt[ind1,2].astype(int)
                    y_test  = ys[ind2,2].astype(int)
            elif task==2: #Noise level
                if include_win_ind and winsize>0:
                    y_train = yt[ind1][:,[1,4]].astype(int)
                    y_test  = ys[ind2][:,[1,4]].astype(int)
                else:
                    y_train = yt[ind1,1].astype(int)
                    y_test  = ys[ind2,1].astype(int)
            elif task==1:
                if include_win_ind and winsize>0:
                    y_train = yt[ind1][:,[0,4]].astype(int)
                    y_test  = ys[ind2][:,[0,4]].astype(int)
                else:
                    y_train = yt[ind1,0].astype(int)
                    y_test  = ys[ind2,0].astype(int)

        self.feature_extraction_count+=1
        return X_train,y_train,X_test,y_test
    def getLWR(self,eSample = [0,0],verbose=True,useRaw=False):
        if useRaw:
            L,W,R,Score,cols = Segments(self.rawData['D'],self.rawData['S'],LabelCol=-2,eSample =eSample,verbose=verbose)
        else:
            L,W,R,Score,cols = Segments(self.processed['D'],self.rawData['S'],LabelCol=-2,eSample =eSample,verbose=verbose)
        return L,W,R,Score,cols
    def getEEG(self,useRaw=False):
        '''
        return EEG Channels

        if useRaw True, extract from rawData else from processed
        '''
        return self.rawData['D'].iloc[:,1:15].astype(float) if useRaw else self.processed['D'].iloc[:,1:15].astype(float)
    def updateEEG(self,XE,update_full=True):
        if update_full:
            #Given XE should have same size as original EEG signals
            assert self.processed['D'].iloc[:,1:15].shape== XE.shape
            self.processed['D'].iloc[:,1:15]= XE
        else:
            self.processed['D'].iloc[:XE.shape[0],1:XE.shape[1]+1]= XE
    def getPPG(self,useRaw=False):
        '''
        return PPG signals

        if useRaw True, extract from rawData else from processed
        '''
        return self.rawData['D'].iloc[:,15:18].astype(float) if useRaw else self.processed['D'].iloc[:,15:18].astype(float)
    def updatePPG(self,XP,update_full=True):
        if update_full:
            #Given XE should have same size as original EEG signals
            assert self.processed['D'].iloc[:,15:18].shape== XP.shape

            self.processed['D'].iloc[:,15:18]= XP
        else:
            self.processed['D'].iloc[:XP.shape[0],15:XP.shape[1]+1]= XP
    def getGSR(self,useRaw=False):
        '''
        return GSR signals

        if useRaw True, extract from rawData else from processed
        '''
        return self.rawData['D'].iloc[:,19:21].astype(float) if useRaw else self.processed['D'].iloc[:,19:21].astype(float)
    def updateGSR(self,XG,update_full=True):
        if update_full:
            #Given XE should have same size as original EEG signals
            assert self.processed['D'].iloc[:,19:21].shape== XG.shape

            self.processed['D'].iloc[:,19:21]= XG
        else:
            self.processed['D'].iloc[:XG.shape[0],19:XG.shape[1]+1]= XG
    def getlabels(self):
        return self.processed['D'].iloc[:,21:-1]
    def getAtScores(self):
        return self.rawData['S']['Correctness'].astype(float)

def Extract_featuresEEG(Sg,Scores,feature='rhythmic',offset=0,winsize=-1,hopesize=None,normalize=False,log10p1=True,
                        flat=True,fs=128,order=5,method='welch',window='hann',scaling='density',detrend='constant',filter_method='lfilter',
                        average='mean',fBands=[],Sum=True, Mean=False, SD=False, use_joblib=False,n_jobs=-1,verbose=0,use_v0=False):
    '''
    method : welch, None
    scaling: 'density'--V**2/Hz 'spectrum'--V**2
    detrend: False, 'constant', 'linear'
    average: 'mean', 'median'   #periodogram average method
    '''
    if verbose>2:
        print('fbands',fBands,'SumMeanSD',Sum,Mean,SD)

    X,y = getXySg(Sg=Sg,scores=Scores,normalize=normalize,log10p1=log10p1,flat=flat,offset=offset,
                      winsize=winsize,hopesize=hopesize,fs=fs,order=order,filter_method=filter_method,method=method,window=window,
                                scaling=scaling,average=average,detrend=detrend,
                                fBands=fBands,Sum=Sum, Mean=Mean, SD=SD,
                                use_joblib=use_joblib,n_jobs=n_jobs,verbose=verbose,use_v0=use_v0)
    return X,y

def getXySg(Sg,scores,normalize=False,log10p1=True,flat=True,offset=0,winsize=-1,hopesize=None,fs=128,order=5,filter_method='lfilter',
           method='welch',window='hann',scaling='density',detrend='constant',average='mean',fBands=[],
           Sum=True, Mean=False, SD=False,
           use_joblib=False,n_jobs=-1,verbose=0,use_v0=False):
    '''
    method : welch, None
    scaling: 'density'--V**2/Hz 'spectrum'--V**2
    detrend: False, 'constant', 'linear'
    average: 'mean', 'median'   #periodogram average method
    '''
    #Sum=True
    #Mean=SD=False
    # Atleast one of them to be computed
    assert Sum+Mean+SD

    X,y = [],[]
    for k in range(len(Sg)):
        Sgk = Sg[k]
        assert len(Sgk)==len(scores)
        for i in range(len(Sgk)):
            utils.ProgBar(i,N=len(Sgk),title=f'Sg - {k}|    ',style=2,L=50,selfTerminate=False)
            E = Sgk[i][:,1:15].astype(float)
            if E.shape[0]>64: # if segment is atleast 0.5 sec long
                if winsize>16:
                    win = np.arange(winsize)
                    w_idx = 0
                    while win[-1]<E.shape[0]:
                        utils.ProgBar(i,N=len(Sgk),title=f'Sg - {k}| win-{w_idx}  ',style=2,L=50,selfTerminate=False)
                        Ei = E[win,:]
                        if use_v0:
                            Px,Pm,Pd = RhythmicDecomposition(Ei,fs=fs,order=order,method=method,win=window,
                                Sum=Sum,Mean=Mean,SD =SD,scaling=scaling, average=average,detrend=detrend)
                        else:
                            Px,Pm,Pd = RhythmicDecomposition_V2(Ei,fs=fs,order=order,method=method,win=window,
                                Sum=Sum,Mean=Mean,SD =SD,scaling=scaling, average=average,detrend=detrend,fBands=fBands,use_joblib=use_joblib, n_jobs=n_jobs,verbose=verbose)

                        if normalize:
                            if Sum: Px = Px/Px.sum(0)
                            if Mean: Pm = Pm/Pm.sum(0)
                            if SD: Pd = Pd/Pd.sum(0)
                        if log10p1:
                            if Sum:Px = np.log10(Px+1)
                            if Mean: Pm = np.log10(Pm+1)
                            if SD: Pd = np.log10(Pd+1)
                        if flat:
                            if Sum:Px = Px.reshape(-1)
                            if Mean: Pm = Pm.reshape(-1)
                            if SD: Pd = Pd.reshape(-1)

                        if Sum+Mean+SD>1:
                            Pxf = []
                            if Sum: Pxf.append(Px)
                            if Mean: Pxf.append(Pm)
                            if SD: Pxf.append(Pd)
                            X.append(Pxf)
                        elif (Sum+Mean+SD)==1:
                            if Sum: X.append(Px)
                            if Mean: X.append(Pm)
                            if SD: X.append(Pd)
                        #Lables
                        A =  scores[i]
                        N =  Sgk[i][offset+8,-4]
                        S =  Sgk[i][offset+8,-3]
                        T =  Sgk[i][offset+8,-2]
                        y.append([A,N,S,T,w_idx])
                        win+=hopesize
                        w_idx+=1

                    if win[-1]-E.shape[0]<hopesize:
                        Ei = E[-winsize:,:]
                        if use_v0:
                            Px,Pm,Pd = RhythmicDecomposition(Ei,fs=fs,order=order,method=method,win=window,
                                Sum=Sum,Mean=Mean,SD =SD,scaling=scaling, average=average,detrend=detrend)
                        else:
                            Px,Pm,Pd = RhythmicDecomposition_V2(Ei,fs=fs,order=order,method=method,win=window,
                                Sum=Sum,Mean=Mean,SD =SD,scaling=scaling, average=average,detrend=detrend,fBands=fBands,use_joblib=use_joblib, n_jobs=n_jobs,verbose=verbose)

                        if normalize:
                            if Sum: Px = Px/Px.sum(0)
                            if Mean: Pm = Pm/Pm.sum(0)
                            if SD: Pd = Pd/Pd.sum(0)
                        if log10p1:
                            if Sum:Px = np.log10(Px+1)
                            if Mean: Pm = np.log10(Pm+1)
                            if SD: Pd = np.log10(Pd+1)
                        if flat:
                            if Sum:Px = Px.reshape(-1)
                            if Mean: Pm = Pm.reshape(-1)
                            if SD: Pd = Pd.reshape(-1)

                        if Sum+Mean+SD>1:
                            Pxf = []
                            if Sum: Pxf.append(Px)
                            if Mean: Pxf.append(Pm)
                            if SD: Pxf.append(Pd)
                            X.append(Pxf)
                        elif (Sum+Mean+SD)==1:
                            if Sum: X.append(Px)
                            if Mean: X.append(Pm)
                            if SD: X.append(Pd)
                        #Lables
                        A =  scores[i]
                        N =  Sgk[i][offset+8,-4]
                        S =  Sgk[i][offset+8,-3]
                        T =  Sgk[i][offset+8,-2]
                        y.append([A,N,S,T,w_idx])
                else:
                    if use_v0:
                        Px,Pm,Pd = RhythmicDecomposition(E,fs=fs,order=order,method=method,win=window,
                                Sum=Sum,Mean=Mean,SD =SD,scaling=scaling, average=average,detrend=detrend)
                    else:
                        Px,Pm,Pd= RhythmicDecomposition_V2(E,fs=fs,order=order,method=method,win=window,
                                Sum=Sum,Mean=Mean,SD =SD,scaling=scaling,average=average,detrend=detrend,fBands=fBands,use_joblib=use_joblib, n_jobs=n_jobs,verbose=verbose)
                    if normalize:
                        if Sum: Px = Px/Px.sum(0)
                        if Mean: Pm = Pm/Pm.sum(0)
                        if SD: Pd = Pd/Pd.sum(0)
                    if log10p1:
                        if Sum:Px = np.log10(Px+1)
                        if Mean: Pm = np.log10(Pm+1)
                        if SD: Pd = np.log10(Pd+1)
                    if flat:
                        if Sum:Px = Px.reshape(-1)
                        if Mean: Pm = Pm.reshape(-1)
                        if SD: Pd = Pd.reshape(-1)
                    if Sum+Mean+SD>1:
                        Pxf = []
                        if Sum: Pxf.append(Px)
                        if Mean: Pxf.append(Pm)
                        if SD: Pxf.append(Pd)
                        X.append(Pxf)
                    elif (Sum+Mean+SD)==1:
                        if Sum: X.append(Px)
                        if Mean: X.append(Pm)
                        if SD: X.append(Pd)
                    #Lables
                    A =  scores[i]
                    N =  Sgk[i][offset+8,-4]
                    S =  Sgk[i][offset+8,-3]
                    T =  Sgk[i][offset+8,-2]
                    y.append([A,N,S,T,0])

        print('')

    return np.array(X),np.array(y).astype(float)

def ReadFilesPath(DirFol,verbose=False):
    sFiles =[]
    tFiles =[]
    SubFiles = {}
    for dirName, subdirList, fileList in os.walk(DirFol):
        #print('-%s' % dirName)
        for fname in fileList:
            #print(fname)
            if 'Signal' in fname or 'Text' in fname:
                sb = int(fname.split('_')[0][1:])
                if sb not in SubFiles.keys(): SubFiles[sb]={}
                if 'Signal' in fname:
                    sfile = os.path.join(dirName, fname).replace('\\','/')
                    sFiles.append(sfile)
                    SubFiles[sb]['sigFile'] = sfile
                    if verbose: print('Sig  :',fname)
                if 'Text' in fname:
                    tfile = os.path.join(dirName, fname).replace('\\','/')
                    tFiles.append(tfile)
                    SubFiles[sb]['txtFile'] = tfile
                    if verbose: print('Text :',fname)

    print("Total Subjects : ", len(SubFiles))
    return SubFiles

def ReadFile_DS(DSfiles):
    assert 'sigFile' in DSfiles.keys()
    assert 'txtFile' in DSfiles.keys()
    D = pd.read_csv(DSfiles['sigFile'],delimiter=",")
    S = pd.read_csv(DSfiles['txtFile'],delimiter=",")
    return D,S

def FilterEEG_D(D,col=range(1,15),band =[0.5],btype='highpass',order=5,fs =128.0,method='lfilter',verbose=0,use_joblib=False,n_jobs=-1):
    Di = deepcopy(D)
    ECol = ['AF3','F7','F3','FC5','T7','P7','O1','O2','P8','T8','FC6','F4','F8','AF4']
    cols = list(Di)
    for i in col: assert cols[i] in ECol

    E   = np.array(Di.iloc[:,1:15]).astype(float)
    #b,a = butter(order,np.array(band)/(0.5*fs),btype=btype)
    #Ef  = np.array(Parallel(n_jobs=-1)(delayed(lfilter)(b,a,E[:,i]) for i in range(E.shape[1]))).T
    Ef = filter_X(E,band=band,btype=btype,method=method,fs=fs,order=order,verbose=verbose,use_joblib=use_joblib,n_jobs=n_jobs)
    Di.iloc[:Ef.shape[0],1:15] = Ef
    return Di

#def FilterEEG_X(X,band =[0.5],btype='highpass',order=5,fs =128.0):
#    b,a = butter(order,np.array(band)/(0.5*fs),btype=btype)
#    Xf  = np.array(Parallel(n_jobs=-1)(delayed(lfilter)(b,a,X[:,i]) for i in range(X.shape[1]))).T
#    return Xf
def FilterEEG_X(X,band =[0.5],btype='highpass',order=5,fs =128.0,method='lfilter',verbose=0,use_joblib=False,n_jobs=-1):
    #b,a = butter(order,np.array(band)/(0.5*fs),btype=btype)
    #Xf  = np.array(Parallel(n_jobs=-1)(delayed(lfilter)(b,a,X[:,i]) for i in range(X.shape[1]))).T
    Xf  = filter_X(X,band=band,btype=btype,fs=fs, order=order,method=method,verbose=verbose,use_joblib=use_joblib,n_jobs=n_jobs)
    return Xf

def filter_X(X,band=[0.5],btype='highpass',fs=128, order=5,method='lfilter',verbose=0,use_joblib=False,n_jobs=-1):
    """
       Filter a signal using IIR Butterworth with method.
       A forward-backward digital filter using cascaded second-order sections
       BA:
     input
     -----
     X :  multichannel signal (n,ch)
     btype: 'highpass', 'lowpass', 'bandpass', 'bandstop'
     band: [fc1,fc2]  - cut-off frequencies for bandpass and bandstop
           [fc]       - cut-off frequency for lowpass and highpass

     method: 'lfilter', 'filtfilt', 'SOS'
     order:  order of filter (default=5)
     use_joblib: if true, attempt to use joblib for parallel processing of multichannel, if fails, apply filtering one by one
               : default False, since most system fails to use joblib

    """
    #freqs, filter_type = _signal_filter_sanitize(lowcut=lowcut, highcut=highcut, sampling_rate=sampling_rate)

    #freqs = [fc_low,fc_high]
    assert btype in ['lowpass','highpass','bandpass','bandstop']
    assert method in ['lfilter','filtfilt','SOS']
    if verbose: print(X.shape, 'channels axis = 1')
    if verbose>1: print(f'Applying {btype} filter of order {order} with cut-off freq {band} using {method} method')
    freqs = np.array(band) / (0.5*fs)
    if method=='SOS':
        #print(freqs)
        sos = scipy.signal.butter(order, freqs, btype=btype, output="sos")
    else:
        #b,a = scipy.signal.butter(order,np.array(band)/(0.5*fs),btype=btype)
        b,a = scipy.signal.butter(order,freqs,btype=btype)

    if method=='SOS':
        if len(X.shape)>1:
            if use_joblib:
                try:
                    Xf  = np.array(Parallel(n_jobs=n_jobs)(delayed(scipy.signal.sosfiltfilt)(sos,X[:,i]) for i in range(X.shape[1]))).T
                except:
                    print('joblib paraller failed computing with loops- turn off --> use_joblib=False')
                    Xf = np.array([scipy.signal.sosfiltfilt(sos, X[:,i]) for i in range(X.shape[1])]).T
            else:
                Xf = np.array([scipy.signal.sosfiltfilt(sos, X[:,i]) for i in range(X.shape[1])]).T
        else:
            Xf = scipy.signal.sosfiltfilt(sos, X)
    elif method=='filtfilt':
        if len(X.shape)>1:
            if use_joblib:
                try:
                    Xf  = np.array(Parallel(n_jobs=n_jobs)(delayed(scipy.signal.filtfilt)(b,a,X[:,i]) for i in range(X.shape[1]))).T
                except:
                    print('joblib paraller failed computing with loops- turn off --> use_joblib=False')
                    Xf = np.array([scipy.signal.filtfilt(b,a, X[:,i]) for i in range(X.shape[1])]).T
            else:
                Xf = np.array([scipy.signal.filtfilt(b,a, X[:,i]) for i in range(X.shape[1])]).T
        else:
            Xf = scipy.signal.filtfilt(b,a, X)
    else:#lfilter
        if len(X.shape)>1:
            if use_joblib:
                try:
                    Xf  = np.array(Parallel(n_jobs=n_jobs)(delayed(scipy.signal.lfilter)(b,a,X[:,i]) for i in range(X.shape[1]))).T
                except:
                    print('joblib paraller failed computing with loops- turn off --> use_joblib=False')
                    Xf  = np.array([scipy.signal.lfilter(b,a,X[:,i]) for i in range(X.shape[1])]).T
            else:
                Xf  = np.array([scipy.signal.lfilter(b,a,X[:,i]) for i in range(X.shape[1])]).T
        else:
            Xf  = scipy.signal.lfilter(b,a,X)
    return Xf

def filter_powerline(X,fs=128, powerline=50):
    '''
    Equivilent to lowpass butterworth filter of order 1
    '''
    if fs >= 100:
        b = np.ones(int(fs / powerline))
    else:
        b = np.ones(2)
    a = [len(b)]

    if len(X.shape)>1:
        Xf = np.array([scipy.signal.filtfilt(b,a, X[:,i], method="pad") for i in range(X.shape[1])]).T
    else:
        Xf = scipy.signal.filtfilt(b, a, X, method="pad")
    return Xf

def Segments(D,S,LabelCol =-2,eSample = [0,0],verbose=True):
    '''
    input:
    D :  pd.DataFrame of signal file
    #D = pd.read_csv(sigFile,delimiter=",")

    S :  pd.DataFrame of text file
    #S = pd.read_csv(txtFile,delimiter=",")

    eSample :  extra samples - 64 samples before and after = [64,64] (default [0,0])

    LabelCol: Column to read label (default -2)

    verbose : verbosity
    '''
    #D = pd.read_csv(sFiles[SubID],delimiter=",")
    #S = pd.read_csv(tFiles[SubID],delimiter=",")
    cols = list(D)

    assert cols[LabelCol]=='Label_T'
    assert list(S)[-1]=='Correctness'

    L,W,R,cols = _ExtractSegments(D,statsCol =LabelCol,eSample = eSample,verbose=verbose)
    Score = list(S.iloc[:,-1])
    if verbose: print('# Scores : ', len(Score))
    return L,W,R,Score,cols

def _ExtractSegments(D, statsCol =-2,eSample = [0,0],verbose=True):
    col = list(D)
    D = np.array(D)
    #----Listening Segments
    aud = np.where(D[:,statsCol]==0)[0]
    f = np.where(aud[:-1]!=aud[1:]-1)[0] +1
    f = np.hstack([0,f,aud.shape[0]])
    #print(aud)
    #print(f)

    s1x,s2x = eSample[0],eSample[1]

    AudSeg = []
    for i in range(f.shape[0]-1):
        ai = aud[f[i]:f[i+1]]
        s1,s2 = s1x,s2x
        if ai[0]-s1<0:
            s1,pr = ai[0], print('limited extra samples in A seg# '+str(i)) if verbose else None
        if ai[-1]+s2>D.shape[0]:
            s2,pr =D.shape[0]-ai[-1]-1, print('limited extra samples in A seg# '+str(i)) if verbose else None
        ai = np.hstack([np.arange(ai[0]-s1,ai[0]),ai,np.arange(ai[-1]+1,ai[-1]+s2+1)])
        seg = D[ai,:]
        AudSeg.append(seg)

    #----Writing Segments
    wrt = np.where(D[:,statsCol]==1)[0]
    f = np.where(wrt[:-1]!=wrt[1:]-1)[0] +1
    f = np.hstack([0,f,wrt.shape[0]])

    WrtSeg = []
    for i in range(f.shape[0]-1):
        wi =  wrt[f[i]:f[i+1]]
        s1,s2 = s1x,s2x
        if wi[0]-s1<0:
            s1,pr = wi[0], print('limited extra samples in W seg# '+str(i)) if verbose else None
        if wi[-1]+s2>D.shape[0]:
            s2,pr =D.shape[0]-wi[-1]-1, print('limited extra samples in W seg# '+str(i)) if verbose else None
        wi =  np.hstack([np.arange(wi[0]-s1,wi[0]),wi,np.arange(wi[-1]+1,wi[-1]+s2+1)])
        #print(wi[0],wi[-1])
        seg = D[wi,:]
        WrtSeg.append(seg)

    #----Noting Segments
    non = np.where(D[:,statsCol]==2)[0]
    f = np.where(non[:-1]!=non[1:]-1)[0] +1
    f = np.hstack([0,f,non.shape[0]])

    ResSeg = []
    for i in range(f.shape[0]-1):
        ri = non[f[i]:f[i+1]]
        s1,s2 = s1x,s2x
        if ri[0]-s1<0:
            s1,pr = ri[0], print('limited extra samples in R seg# '+str(i)) if verbose else None
        if ri[-1]+s2>D.shape[0]:
            s2,pr =D.shape[0]-ri[-1]-1, print('limited extra samples in R seg#'+str(i)) if verbose else None
        ri =  np.hstack([np.arange(ri[0]-s1,ri[0]),ri,np.arange(ri[-1]+1,ri[-1]+s2+1)])
        #print(ri[0],ri[-1])
        seg = D[ri,:]
        ResSeg.append(seg)

    if verbose:
        print('# Listening Segmnts : ', len(AudSeg))
        print('# Writing Segmnts   : ', len(WrtSeg))
        print('# Resting Segmnts   : ', len(ResSeg))
    return AudSeg,WrtSeg,ResSeg,col

def RhythmicDecomposition(E,fs=128.0,order=5,method='welch',win='hann',Sum=True,Mean=False,SD =False,
                          scaling='density', average='mean',detrend='constant'):

    #average :  method to average the periodograms, mean or median
    '''
    method : welch, None
    scaling: 'density'--V**2/Hz 'spectrum'--V**2
    average: 'mean', 'median'
    detrend: False, 'constant', 'linear'
    '''

    # Delta, Theta, Alpha, Beta, Gamma1, Gamma2
    fBands =[[4],[4,8],[8,14],[14,30],[30,47],[47]]
    #delta=[0.2-4] else filter is unstable-------------------------UPDATED 19feb2019

    Px = np.zeros([len(fBands),E.shape[1]])
    Pm = np.zeros([len(fBands),E.shape[1]])
    Pd = np.zeros([len(fBands),E.shape[1]])
    if Sum or Mean or SD:
        k=0
        for freqs in fBands:
            #print(np.array(freqs)/(0.5*fs))
            btype='bandpass'
            if len(freqs)==1:
                btype='lowpass' if freqs[0]==4 else 'highpass'
                b,a = butter(order,np.array(freqs[0])/(0.5*fs),btype=btype)
            else:
                b,a = butter(order,np.array(freqs)/(0.5*fs),btype=btype)

            #b,a = butter(order,np.array(freqs)/(0.5*fs),btype='bandpass')
            B = np.array(Parallel(n_jobs=-1)(delayed(lfilter)(b,a,E[:,i]) for i in range(E.shape[1])))
            P = np.array(Parallel(n_jobs=-1)(delayed(Periodogram)(B[i,:],fs=fs,method=method,win=win,scaling=scaling,
                                 average=average,detrend=detrend) for i in range(B.shape[0])))
            if Sum: Px[k,:] = np.sum(np.abs(P),axis=1).astype(float)
            if Mean: Pm[k,:] = np.mean(np.abs(P),axis=1).astype(float)
            if SD: Pd[k,:] = np.std(np.abs(P),axis=1).astype(float)
            k+=1

    return Px,Pm,Pd


def RhythmicDecomposition_V2(E,fs=128.0,order=5,filter_method='lfilter',method='welch',win='hann',Sum=True,Mean=False,SD =False,
                          scaling='density', average='mean',detrend='constant',fBands=[],use_joblib=False, n_jobs=-1,verbose=0):

    #average :  method to average the periodograms, mean or median
    '''
    method : welch, None
    scaling: 'density'--V**2/Hz 'spectrum'--V**2
    average: 'mean', 'median'
    detrend: False, 'constant', 'linear'
    '''

    # Delta, Theta, Alpha, Beta, Gamma1, Gamma2
    if len(fBands)==0: fBands =[[None,4],[4,8],[8,14],[14,30],[30,47],[47, None]]
    #delta=[0.2-4] else filter is unstable-------------------------UPDATED 19feb2019

    Px = np.zeros([len(fBands),E.shape[1]])
    Pm = np.zeros([len(fBands),E.shape[1]])
    Pd = np.zeros([len(fBands),E.shape[1]])
    if Sum or Mean or SD:
        k=0
        for freqs in fBands:
            #print(np.array(freqs)/(0.5*fs))
            if freqs[0] is None:
                btype='lowpass'
                band = [freqs[1]]
            elif freqs[1] is None:
                btype= 'highpass'
                band = [freqs[0]]
            else:
                btype='bandpass'
                band = freqs

            B = filter_X(E,band=band,btype=btype,fs=fs,order=order,method=filter_method,verbose=verbose,use_joblib=use_joblib,n_jobs=n_jobs)
            if use_joblib:
                try:
                    P = np.array(Parallel(n_jobs=n_jobs)(delayed(Periodogram)(B[:,i],fs=fs,method=method,win=win,scaling=scaling,
                                     average=average,detrend=detrend) for i in range(B.shape[1])))
                except:
                    P = np.array([Periodogram(B[:,i],fs=fs,method=method,win=win,scaling=scaling,
                                         average=average,detrend=detrend) for i in range(B.shape[1])])
            else:
                P = np.array([Periodogram(B[:,i],fs=fs,method=method,win=win,scaling=scaling,
                                     average=average,detrend=detrend) for i in range(B.shape[1])])

            if Sum: Px[k,:] = np.sum(np.abs(P),axis=1).astype(float)
            if Mean: Pm[k,:] = np.mean(np.abs(P),axis=1).astype(float)
            if SD: Pd[k,:] = np.std(np.abs(P),axis=1).astype(float)
            k+=1

    return Px,Pm,Pd

def Periodogram(x,fs=128,method ='welch',win='hann',scaling='density', average='mean',detrend='constant'):
    '''
    #scaling = 'density'--V**2/Hz 'spectrum'--V**2
    #average = 'mean', 'median'
    #detrend = False, 'constant', 'linear'
    '''
    if method ==None:
        f, Pxx = scipy.signal.periodogram(x,fs,win,scaling=scaling,detrend=detrend)
    elif method =='welch':
        f, Pxx = scipy.signal.welch(x,fs,win,nperseg=np.clip(len(x),0,256),scaling=scaling,average=average,detrend=detrend)
    return np.abs(Pxx)

# for "spkit" wavelet filtering
#=============================
def wavelet_filtering_win(x,winsize=128,wv='db3',threshold='optimal',below=True,k=1.5,mode='elim',wpd_mode='symmetric',
                wpd_maxlevel=None,packetwise=False,WPD=True,lvl=[],verbose=False,sf=1,
                hopesize=None, wintype='hamming',windowing_before=False,IPR=[0.25, 0.75]):
    '''
    Wavelet Filtering applied to smaller windows
    --------------------------------------------
    Same as wavelet_filtering fumction, applied to smaller overlapping windows and reconstructed by overlap-add method
    for documentation, check help(wavelet_filtering)
    '''
    if hopesize is None: hopesize = winsize//2
    M   = winsize
    H   = hopesize
    hM1 = (M+1)//2
    hM2 = M//2

    xt  = np.hstack([np.zeros(hM2),x,np.zeros(hM1)])

    pin  = hM1
    pend = xt.size-hM1
    wh   = signal.get_window(wintype,M)
    if verbose: print('Windowing before apply : ',windowing_before)

    xR   = np.zeros(xt.shape)
    pf=0
    while pin<=pend:
        if verbose:
            if 100*pin/float(pend)>=pf+1:
                pf = 100*pin/float(pend)
                pbar = '|'+'#'*int(pf)+' '*(99-int(pf))+'|'
                print(str(np.round(pf,2))+'%'+pbar,end='\r', flush=True)
        xi = xt[pin-hM1:pin+hM2]
        if windowing_before: xi *=wh

        xr = sp.wavelet_filtering(xi,wv=wv,threshold=threshold,filter_out_below=below,k=k,mode=mode,wpd_mode=wpd_mode,wpd_maxlevel=wpd_maxlevel,
               packetwise=packetwise,WPD=WPD,lvl=lvl,verbose=0,sf=sf,IPR=IPR)

        if not(windowing_before): xr *=wh

        xR[pin-hM1:pin+hM2] += H*xr  ## Overlap Add method
        pin += H
    xR = xR[hM2:-hM1]/sum(wh)

    return xR


#--------Not in use yet---------------------
# def FeatureExtraction(E,fs=128.0,Rhythmic =False,order=5,method=None,window='flattop',Aggregate = False,
#                       binsize=1,sqSum=False,meanAgg = False):
#     if Rhythmic:
#         Px = RhythmicDecomposition_(E,fs=fs,order=order,method=method,win=window,Aggregate=Aggregate,meanAgg=meanAgg)
#     else:
#         Px = SpectralFeature(E,fs=fs,binsize=binsize,sqSum=sqSum,window=window,Aggregate=Aggregate)

#     return Px
# def FeatureExtractionV1(E,fs=128.0,Rhythmic =False,order=5,method=None,window='flattop',Aggregate = False,
#                       binsize=1,sqSum=False,return_mean=False,scaling='density',PxAverage='mean',detrend='constant'):
#     if Rhythmic:
#         Px,Pm,Pd = RhythmicDecomposition(E,fs=fs,order=order,method=method,win=window,Sum=True,Mean=True,
#                                    SD=False,scaling=scaling,average=PxAverage,detrend=detrend)
#         if Aggregate: Px = np.mean(Px,axis=1)
#         if return_mean: Px = Pm
#     else:
#         Px = SpectralFeature(E,fs=fs,binsize=binsize,sqSum=sqSum,window=window,Aggregate=Aggregate)

#     return Px
# def RhythmicDecomposition_(E,fs=128.0,order =5,method='welch',win='hann',Aggregate = False,meanAgg = False):

#     # Delta, Theta, Alpha, Beta, Gamma1, Gamma2
#     fBands =[[0.2,4],[4,8],[8,14],[14,30],[30,47],[47,64-0.1]]
#     fBands =[[4],[4,8],[8,14],[14,30],[30,47],[47]]
#     #delta=[0.2-4] else filter is unstable-------------------------UPDATED 19feb2019

#     Px=[]
#     for freqs in fBands:
#         #print(np.array(freqs)/(0.5*fs))
#         btype='bandpass'
#         if len(freqs)==1:
#             btype='lowpass' if freqs[0]==4 else 'highpass'
#             b,a = butter(order,np.array(freqs[0])/(0.5*fs),btype=btype)
#         else:
#             b,a = butter(order,np.array(freqs)/(0.5*fs),btype=btype)

#         #b,a = butter(order,np.array(freqs)/(0.5*fs),btype='bandpass')
#         B = np.array(Parallel(n_jobs=-1)(delayed(lfilter)(b,a,E[:,i]) for i in range(E.shape[1])))
#         P = np.array(Parallel(n_jobs=-1)(delayed(Periodogram)(B[i,:],fs=fs,method =method,win =win) for i in range(B.shape[0])))
#         if Aggregate:
#             Px.append(np.mean(np.abs(P)))
#         else:
#             if meanAgg:
#                 Px.append(np.mean(np.abs(P),axis=1))
#             else:
#                 Px.append(np.sum(np.abs(P),axis=1))
#     return np.array(Px).astype(float)
# def PeriodogramV(X,fs=128,method ='welch',win='hann'):
#     P = np.array(Parallel(n_jobs=-1)(delayed(Periodogram)(X[:,i],fs=fs,method =method,win =win) for i in range(X.shape[1])))
#     Px =np.sum(np.abs(P),axis=1)
#     return Px
# def SpectralFeature(E,fs=128.0,binsize=1,sqSum=False, window='flattop',Aggregate = False):
#     #P = np.array(Parallel(n_jobs=-1)(delayed(Periodogram)(E[:,i],fs=fs,method =method,win =win) for i in range(E.shape[1])))
#     Px = np.array(Parallel(n_jobs=-1)(delayed(SpectrumeHz)(E[:,i],fs=fs,window =window,binsize=binsize, sqSum=sqSum) for i in range(E.shape[1])))

#     if Aggregate:
#         Px = np.mean(Px,axis=0)
#     else:
#         Px = np.hstack(Px)
#     return Px
# def SpectrumeHz(x,fs=128,window='flattop',binsize=-1,sqSum=False):
#     f, Pxx = scipy.signal.periodogram(x,fs=fs,window=window,scaling='spectrum')
#     if binsize>-1:
#         Px =[]
#         #binsize
#         for i in np.arange(0,fs//2,binsize):
#             if sqSum:
#                 pxi = np.power(np.abs(Pxx[(f>=i) & (f<i+1)]),2)
#             else:
#                 pxi = np.abs(Pxx[(f>=i) & (f<i+1)])

#             Px.append(sum(pxi))

#         if sum(f>=i)>sum([(f>=i) & (f<i+1)][0]):
#             if sqSum:
#                 pxi = np.power(np.abs(Pxx[(f>=i)]),2)
#             else:
#                 pxi = np.abs(Pxx[(f>=i)])

#             Px[-1] = sum(pxi)

#         return np.array(Px)
#     else:
#         return abs(Pxx)
#print('PhyAAt Processing lib Loaded...')
