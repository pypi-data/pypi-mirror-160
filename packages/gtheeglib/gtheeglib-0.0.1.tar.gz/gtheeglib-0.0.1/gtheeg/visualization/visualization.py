import mne #for eeg (bdf) file
from matplotlib import pyplot as plt

def plot_channels(data : mne.io.edf.edf.RawEDF,interval_min):
    ax = [plt.subplot(3,2,i) for i in range(1,7)]
    j = interval_min
    for i in range(6):
        if data._data[j,1:2]:
            ax[i].plot(data._data[j,:])
            ax[i].set_title(data.ch_names[j])
            j = j+1

def plot3Inter(raw1:mne.io.edf.edf.RawEDF,raw2:mne.io.edf.edf.RawEDF,raw3:mne.io.edf.edf.RawEDF,id_channel:int,min_val:int,max_val:int):
    ax1 = plt.subplot(2,2,1)
    ax2 = plt.subplot(2,2,2)
    ax3 = plt.subplot(2,2,3)

    ax1.set_title('Healthy - ' + raw1.ch_names[id_channel])
    ax1.plot(raw1._data[id_channel,min_val:max_val])

    ax2.set_title('Stroke - ' +raw2.ch_names[id_channel])
    ax2.plot(raw2._data[id_channel,min_val:max_val])

    ax3.set_title('TIA - ' +raw3.ch_names[id_channel])
    ax3.plot(raw3._data[id_channel,min_val:max_val])

def to_minutes(time:str):
    h = int(time.split(':')[0])
    m = int(time.split(':')[1])

    final_time = h*60 + m

    return final_time

def plotMultiEEGInter(raw1:mne.io.edf.edf.RawEDF,raw2:mne.io.edf.edf.RawEDF,raw3:mne.io.edf.edf.RawEDF,id_channel:int,min_val:int,max_val:int,total_plot:int):
    nbcols = total_plot // 2 + 1
    ax = [plt.subplot(nbcols,2,i) for i in range(1,nbcols+1)]

    l = 1
    for i in range(nbcols * 2):
        ax[l].set_title(raw1.ch_names[id_channel])
        ax[l].plot(raw1._data[id_channel,min_val:max_val])

        l += l+1
        ax[l].set_title(raw2.ch_names[id_channel])
        ax[l].plot(raw2._data[id_channel,min_val:max_val])

        l += l+1
        ax[l].set_title(raw3.ch_names[id_channel])
        ax[l].plot(raw3._data[id_channel,min_val:max_val])