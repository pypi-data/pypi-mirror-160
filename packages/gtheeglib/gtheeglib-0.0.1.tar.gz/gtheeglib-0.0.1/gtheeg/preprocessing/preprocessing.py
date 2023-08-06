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



        
class Preprocessing:
    #def __init__(self):
    
    #channels_names = ['F7','Fp1','Fp2','F8','F3','Fz','F4','C3','Cz','P8','P7','Pz','P4','T3','P3','O1','O2','C4','T4','A2']
    
    def features_extraction(data : np.ndarray, channel_name : str):
        mean = np.mean(data)
        std = np.std(data)
        var = np.var(data)
        rms = np.sqrt(np.mean(data**2))
        ptp = np.ptp(data)
        minim = np.min(data,axis=-1)
        maxim = np.max(data,axis=-1)
        argminim = np.argmin(data,axis=-1)
        argmaxim = np.argmax(data,axis=-1)
        dasd = np.sqrt(np.mean(np.square(np.diff(data,axis=-1)),axis=-1)) #difference absolute standard deviation
        PFD = eeglib.features.PFD(data)
        DFA = eeglib.features.DFA(data)
        HFD = eeglib.features.HFD(data)
        LZC = eeglib.features.LZC(data)
        kurtosis = stats.kurtosis(data)
        skew = stats.skew(data)
        countSignChanges = eeglib.features.countSignChanges(data)
        hjorthActivity = eeglib.features.hjorthActivity(data)
        hjorthComplexity = eeglib.features.hjorthComplexity(data)
        hjorthMobility = eeglib.features.hjorthMobility(data)
        sampEn = eeglib.features.sampEn(data)


        features = {
            channel_name+'_mean': mean,
            channel_name+'_std': std,
            channel_name+'_var': var,
            channel_name+'_rms': rms,
            channel_name+'_ptp': ptp,
            channel_name+'_minim': minim,
            channel_name+'_maxim': maxim,
            channel_name+'_argminim': argminim,
            channel_name+'_argmaxim': argmaxim, 
            channel_name+'_dasd': dasd,
            channel_name+'_PFD': PFD,
            channel_name+'_DFA': DFA,
            channel_name+'_HFD': HFD,
            channel_name+'_LZC': LZC,
            channel_name+'_kurtosis': kurtosis,
            channel_name+'_skew': skew,
            channel_name+'_countSignChanges': countSignChanges,
            channel_name+'_hjorthActivity' : hjorthActivity,
            channel_name+'_hjorthComplexity' : hjorthComplexity,
            channel_name+'_hjorthMobility' : hjorthMobility,
            channel_name+'_sampEn' : sampEn
        }
        return features       
    
    def add_eog(raw, channels, new_name):
        """Computes a single bipolar EOG channel from a list of possible names."""

        # Check that exactly two of the provided channels are in the data
        channels = [ch for ch in channels if ch in raw.ch_names]
        assert len(channels) == 2, (
            'Could not find exactly two channels for computing bipolar '
            f'{new_name}. Please provide different channel names or choose `None`')

        # Compute bipolar EOG channel
        anode = channels[0]
        cathode = channels[1]
        print(f'Adding bipolar channel {new_name} ({anode} - {cathode})')
        raw = set_bipolar_reference(
            raw, anode, cathode, new_name, drop_refs=False, verbose=False)
        raw = raw.set_channel_types({new_name: 'eog'})

        return raw

    def interpolate_bad_channels(raw, bad_channels=None, auto_bad_channels=None):
        """Interpolates any channels from the two lists."""

        # Combine lists of bad channels
        all_bad_channels = []
        if bad_channels is not None and bad_channels != 'auto':
            all_bad_channels += bad_channels
        if auto_bad_channels is not None:
            all_bad_channels += auto_bad_channels

        # Interpolate bad channels
        if all_bad_channels != []:
            raw.info['bads'] += auto_bad_channels
            raw = raw.interpolate_bads()

        return raw, all_bad_channels


    def correct_ica(raw, n_components=15, random_seed=1234, method='fastica'):
        """Corrects ocular artifacts using ICA and automatic component removal."""

        # Run ICA on a copy of the data
        raw_filt_ica = raw.copy()
        raw_filt_ica.load_data().filter(l_freq=1, h_freq=None, verbose=False)
        ica = ICA(
            n_components, random_state=random_seed, method=method)
        ica.fit(raw_filt_ica)

        # Remove bad components from the raw data
        eog_indices, _ = ica.find_bads_eog(
            raw, ch_name='VEOG', verbose=False)
        ica.exclude = eog_indices
        raw = ica.apply(raw)

        return raw, ica


    def read_data(file_path):
        raw = mne.io.read_raw_bdf(file_path,preload=True)
        raw.set_eeg_reference()
        raw.filter(l_freq=None,h_freq=45)
        epochs = mne.make_fixed_length_epochs(raw,duration=30,
                                              #overlap=0
                                             )
        epochs = epochs.get_data()

        return epochs

    def read_data_bdf(file_path):
        raw = mne.io.read_raw_bdf(file_path,preload=True)
        raw.set_eeg_reference()
        raw.filter(l_freq=None,h_freq=45)

        edf_data = raw.get_data()

        return edf_data

    def eeg_preprocessing(file_path,epochs_duration=20,l_freq=.5,h_freq=45,plot=False):
        no_eeg = ['ACC0','ACC1','ACC2','Packet Counter','TRIGGER']
        mont1020 = create_montage_10_20(channels_names)

        raw = mne.io.read_raw_bdf(file_path,preload=True)
        raw = add_eog(raw_stroke,['Fp1','Fp2'],'VEOG')
        raw = raw.set_montage(mont1020,on_missing = 'ignore')
        raw, all_bad_channels = interpolate_bad_channels(raw)
        raw, ica = correct_ica(raw.copy().drop_channels(no_eeg))
        raw.filter(l_freq=.5,h_freq=45)

        if plot:
            print('Ploting PSD')
            raw.plot_psd()
            print('Components of ICA')
            ica.plot_components(outlines = 'skirt')
            print('Ploting Raw')
            raw.plot()
            print('Effect of ICA in the Raw Data')
            ica.plot_sources(raw);

        epochs = mne.make_fixed_length_epochs(raw,duration=epochs_duration,
                                              #overlap=0
                                             )

        return raw,ica,epochs

    


    def features_extraction_eeg(data : np.ndarray,
                                channels_names:list = ['F7','Fp1','Fp2','F8','F3','Fz','F4','C3'
                                                       ,'Cz','P8','P7','Pz','P4','T3','P3','O1',
                                                       'O2','C4','T4','A2'], 
                                number_of_channels:int = 20):
        i = 0
        features_channel_list = []
        dall = {}
        
        if len(data)>=number_of_channels:
            for i in range(number_of_channels):
                print("Extraction of features's channels "+channels_names[i] +" in progress...")
                features = features_extraction(data=data[i],channel_name=channels_names[i])
                features_channel_list.append(features)

                print('features of channels '+channels_names[i]+' well extracted')
            print('----- All Done Well -----')
            for i in features_channel_list:
                dall.update(i)
        else:
            print("Error: The number of channels specified it's too many")

        return dall
    

    def features_extraction_eeg_helper(helper:eeglib.helpers.EDFHelper,
                                channels_names:list = ['F7','Fp1','Fp2','F8','F3','Fz','F4','C3'
                                                       ,'Cz','P8','P7','Pz','P4','T3','P3','O1',
                                                       'O2','C4','T4','A2'], 
                                number_of_channels:int = 20):
        i = 0
        features_channel_list = []
        dall = {}
        data = helper.data

        if len(data)>=number_of_channels:
            for i in range(number_of_channels):
                print("Extraction of features's channels "+channels_names[i] +" in progress...")
                features = features_extraction(data=data[i],channel_name=channels_names[i])
                features_channel_list.append(features)

                print('features of channels '+channels_names[i]+' well extracted')
            print('----- All Done Well -----')
            for i in features_channel_list:
                dall.update(i)
        else:
            print("Error: The number of channels specified it's too many")

        return dall

    def features_extraction_eeg_file(file_path):
        channels_names = ['F7','Fp1','Fp2','F8','F3','Fz','F4','C3','Cz','P8','P7','Pz','P4','T3','P3','O1','O2','C4','T4','A2']
        dataframe = pd.DataFrame()
        for i in range(len(file_path)):
            print("###### Features Extraction for the file " + str(i+1) + ' #######')
            helper = eeglib.helpers.EDFHelper(file_path[i],selectedSignals = channels_names,ICA=True)
            all_features = features_extraction_eeg(helper.data)
            dataframe = dataframe.append(all_features, ignore_index = True)

        return dataframe

    def features_extraction_eeg_file_parallel(file_path):
        channels_names  = ['F7','Fp1','Fp2','F8','F3','Fz','F4','C3','Cz','P8',
                           'P7','Pz','P4','T3','P3','O1','O2','C4','T4','A2']
        dataframe = pd.DataFrame()
        time.sleep(1)
        for i in range(len(file_path)):
            print("###### Features Extraction for the file " + str(i+1) + ' #######')
            helper = eeglib.helpers.EDFHelper(file_path[i],selectedSignals = channels_names,ICA=True)
            all_features = features_extraction_eeg(helper.data)
            dataframe = dataframe.append(all_features, ignore_index = True)

        return dataframe