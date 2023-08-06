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

class Utilities:
    def save_object(obj, filename):
        with open(filename, 'wb') as outp:  # Overwrites any existing file.
            pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)
            
    def pickle_loader(filename):
        """ Deserialize a file of pickled objects. """
        with open(filename, "rb") as f:
            while True:
                try:
                    yield pickle.load(f)
                except EOFError:
                    break