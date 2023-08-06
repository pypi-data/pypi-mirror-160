import pandas as pd
import numpy as np
import glob
import os
import os.path as path
from matplotlib import pyplot as plt
from glob import glob
import mne
import scipy
from scipy import stats
from scipy import fft
from tqdm import tqdm_notebook
import eeglib
from multiprocessing import Pool
import multiprocessing
import time
import pickle


power_band = {'alpha': (8, 13), 'beta': (13, 35), 'delta': (1, 4), 'gamma': (35, 50), 'theta': (4, 8)}


class Features_extraction:
    
    
    def sampEns(data):
        list = []
        for i in range(len(data)):
            list.append(eeglib.features.sampEn(data[i]))

        return np.asarray(list)
    
    def mean(data):
        return np.mean(data,axis=-1)

    def std(data):
        return np.std(data,axis=-1)

    def var(data):
            return np.var(data,axis=-1)

    def minim(data):
            return np.min(data,axis=-1)

    def maxim(data):
            return np.max(data,axis=-1)

    def argminim(data):
            return np.argmin(data,axis=-1)

    def argmaxim(data):
            return np.argmax(data,axis=-1)

    def mean_square(data):
            return np.mean(data**2,axis=-1)

    def rms(data): #root mean square
            return  np.sqrt(np.mean(data**2,axis=-1))

    def dasd(data): #difference absolute standard deviation
        dasd = np.sqrt(np.mean(np.square(np.diff(data,axis=-1)),axis=-1)) 
        return dasd

    def abs_diffs_signal(data):
        return np.sum(np.abs(np.diff(data,axis=-1)),axis=-1)

    def kurtosis(data): 
            return  stats.kurtosis(data,axis=-1)

    def skews(data): 
            return  stats.skew(data,axis=-1)

    def log_detec(data):
        return np.exp(np.mean(np.log(np.abs(data)),axis=-1))

    def PFDs(data):
        list = []
        for i in range(len(data)):
            list.append(eeglib.features.PFD(data[i]))
        return np.asarray(list)

    def DFAs(data):
        list = []
        for i in range(len(data)):
            list.append(eeglib.features.DFA(data[i]))
        return np.asarray(list)

    def LZCs(data):
        list = []
        for i in range(len(data)):
            list.append(eeglib.features.LZC(data[i]))
        return np.asarray(list)

    def HFDs(data):
        list = []
        for i in range(len(data)):
            list.append(eeglib.features.HFD(data[i]))
        return np.asarray(list)

    def countSignChanges(data):
        list = []
        for i in range(len(data)):
            list.append(eeglib.features.countSignChanges(data[i]))
        return np.asarray(list)

    def hjorthActivities(helper:eeglib.helpers.EDFHelper):
        return helper.eeg.hjorthActivity()

    def hjorthComplexities(helper:eeglib.helpers.EDFHelper):
        return helper.eeg.hjorthComplexity()

    def hjorthMobilities(helper:eeglib.helpers.EDFHelper):
        return helper.eeg.hjorthMobility()

    def sampEns(helper:eeglib.helpers.EDFHelper):
        return helper.eeg.sampEn()

    def DTWs(helper:eeglib.helpers.EDFHelper):
        return helper.eeg.DTW()

    def bandsPower(helper:eeglib.helpers.EDFHelper,powerBands = power_band):
        dp = helper_stroke.eeg.bandPower(bands = power_band)
        df = pd.DataFrame(bp)
        return dp,df

    def alphaBand(helper:eeglib.helpers.EDFHelper,powerBands = power_band):
        return np.asarray(bandsPower(helper)[1].iloc[:,0].to_list())

    def betaBand(helper:eeglib.helpers.EDFHelper,powerBands = power_band):
        return np.asarray(bandsPower(helper)[1].iloc[:,1].to_list())

    def deltaBand(helper:eeglib.helpers.EDFHelper,powerBands = power_band):
        return np.asarray(bandsPower(helper)[1].iloc[:,1].to_list())

    def gammaBand(helper:eeglib.helpers.EDFHelper,powerBands = power_band):
        return np.asarray(bandsPower(helper)[1].iloc[:,3].to_list())

    def thetaBand(helper:eeglib.helpers.EDFHelper,powerBands = power_band):
        return np.asarray(bandsPower(helper)[1].iloc[:,4].to_list())


    def features_extraction(data,helper:eeglib.helpers.EDFHelper):
        features_dict = {
            'mean'
        }
        return [
            mean(data),std(data),var(data),minim(data),maxim(data),argminim(data),
            argmaxim(data),mean_square(data),rms(data),
            dasd(data),abs_diffs_signal(data),kurtosis(data),skews(data),
            log_detec(data),PFDs(data),DFAs(data),LZCs(data),
            HFDs(data),countSignChanges(data),hjorthActivities(helper),
            hjorthComplexities(helper),hjorthMobilities(helper),
            sampEns(helper),alphaBand(helper),betaBand(helper),deltaBand(helper),
            gammaBand(helper),thetaBand(helper)
        ]

    def features_extract_to_dataframe(features:list,channels_names):

        list_features = []
        for j in range(len(channels_names)):
            dict_feat = {
                'channel':channels_names[j],
                'mean':features[0][j],
                'std':features[1][j],
                'var':features[2][j],
                'minim':features[3][j],
                'maxim':features[4][j],
                'argminim':features[5][j],
                'argmaxim':features[6][j],
                'mean_square':features[7][j],
                'rms':features[8][j],
                'dasd':features[9][j],
                'abs_diffs_signal':features[10][j],
                'kurtosis':features[11][j],
                'skews':features[12][j],
                'log_detec':features[13][j],
                'PFDs':features[14][j],
                'DFAs':features[15][j],
                'LZCs':features[16][j],
                'HFDs':features[17][j],
                'countSignChanges':features[18][j],
                'hjorthActivities':features[19][j],
                'hjorthComplexities':features[20][j],
                'hjorthMobilities':features[21][j],
                'sampEns':features[22][j],
                'alphaBand':features[23][j],
                'betaBand':features[24][j],
                'deltaBand':features[25][j],
                'gammaBand':features[26][j],
                'thetaBand':features[27][j],
            }
            #print(channels_names[j])
            list_features.append(dict_feat)

        return pd.DataFrame(list_features)