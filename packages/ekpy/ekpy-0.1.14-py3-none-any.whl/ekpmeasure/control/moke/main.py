from mcculw import ul
from mcculw.enums import ULRange, InfoType, AnalogInputMode
from mcculw.enums import ScanOptions, BoardInfo, TriggerEvent, TrigType, FunctionType
from mcculw.ul import ULError

import ctypes

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from warnings import warn
import os

from ..instruments.USB_1208HS_4AO import *

__all__ = ('RUN',)

class RUN():
    
    def __init__(self, daq):
        self.daq = daq.configure()
        self.board_num = daq.board_num
        self.ul_range = daq.ul_range
        return
    
    def load_waveform(self,wvfrm_vstack):
        """load a waveform for daq
        ----
        
        wvfrm_stack: numpy.vstack        
        """
        wf_1d, nzeros_front, nzeros_back = waveforms_to_1d_array(wvfrm_vstack)
        self.wf_1d = wf_1d
        self.nzeros_front = nzeros_front
        self.nzeros_back = nzeros_back
        self.input_wfm_df = pd.DataFrame({i:wvfrm_vstack[i,:] for i in range(wvfrm_vstack.shape[0])})
        
    def config(self, out_channel_start,out_channel_end,in_channel_start,in_channel_end,nave,quiet = False):
        """configure run
        ----
        
        out_channel_start: int, specify which start channel to output waveform
        out_channel_end: int
        in_channel_start: int
        in_channel_end: int
        """
        self.out_channel_end = out_channel_end
        self.out_channel_start = out_channel_start
        self.in_channel_end = in_channel_end
        self.in_channel_start = in_channel_start
        self.nave = nave
        self.quiet = quiet
        
    def go(self):
        """start the run"""
        to_average = []
        #stop old processes in case
        ul.stop_background(self.board_num, FunctionType.AOFUNCTION)
        ul.stop_background(self.board_num, FunctionType.AIFUNCTION)

        nchannels_out = self.out_channel_end - self.out_channel_start + 1

        for i in range(self.nave):    
            returned = apply_and_listen(self.wf_1d, self.nzeros_front, self.nzeros_back, 
                                        in_channel_start=self.in_channel_start, in_channel_end=self.in_channel_end, 
                                        out_channel_start=self.out_channel_start, out_channel_end=self.out_channel_end,
                                        board_num=self.board_num, quiet=self.quiet)
            memhandle_in, memhandle_out, data_array_in, data_array_out, count_in, time = returned

            # Free the buffer and set the data_array to None
            ul.win_buf_free(memhandle_out)
            data_array_out = None

            #now that it is done convert from data_array back to numpy data:
            out = []
            for i in range(0, count_in):
                out.append(ul.to_eng_units(self.board_num, self.ul_range, data_array_in[i]))
            out = np.array(out)

            #clear memory
            ul.win_buf_free(memhandle_in)
            data_array_in = None

            #append data
            to_average.append(out)

        data = np.array(to_average)
        means = np.mean(data, axis = 0)
        out = waveform_1d_to_array(means, nchannels_in=nchannels_out)
        self.waveform_collected = out
        self.time = time
        return
    
    def plot(self,**kwargs):
        """plot waveform_collected"""
        if not hasattr(self, 'time'):
            raise AttributeError('no data has been collected, suggest self.go()')
            return
        fig, ax = plt.subplots(**kwargs)
        for i in range(self.waveform_collected.shape[0]):
            ax.plot(self.time*1e6, self.waveform_collected[i,:])

        ax.set_xlabel('time (us)')
        return fig, ax

    def get_df(self):
        """return pandas dataframe of waveform_collected"""
        if not hasattr(self, 'waveform_collected'):
            raise AttributeError('no data has been collected, suggest self.go()')

        nchannels_in = self.in_channel_end - self.in_channel_start + 1

        #for time so divide by how many channels in 
        nzeros_front_for_time = int(self.nzeros_front/nchannels_in)
        nzeros_back_for_time = int(self.nzeros_back/nchannels_in)

        time = self.time[nzeros_front_for_time:-nzeros_back_for_time]

        data = pd.DataFrame({
                'time':time,
            })
        warn("You are getting the input wfm data (which is perfect), not measured current input to the coil")
        for i in self.input_wfm_df:
            data['AOUT_{}'.format(i)] = 10*(self.input_wfm_df[i]-2047)/2047

        for i, x in enumerate(self.waveform_collected):
            x_for_data = x[nzeros_front_for_time:-nzeros_back_for_time]
            data['AIN_{}'.format(i)] = x_for_data    

        self.data = data
        return

    def save(self, path, name):
        """save waveform_collected too file"""
        if not hasattr(self, 'data'):
            self.get_df(self)
            
        #check if file name exists:
        file_set = set(os.listdir(path))
        if name in file_set:
            yn = input('file already exists. Overwrite? (y/n)')
            if yn == 'y':
                self.data.to_csv(path+name, index = False)
            else: 
                print('Ok. Skipping.')
        else:
            self.data.to_csv(path+name, index = False)
        return