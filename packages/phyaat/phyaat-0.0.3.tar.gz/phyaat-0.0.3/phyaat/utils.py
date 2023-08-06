'''Utilities for PhyAAt.

'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np



A=['\\','-','/','|']

def ProgBar(i,N,title='',style=1,L=50,selfTerminate=True,delta=None):

    pf = int(100*(i+1)/float(N))
    st = ' '*(3-len(str(pf))) + str(pf) +'%|'

    if L==50:
        pb = '#'*int(pf//2)+' '*(L-int(pf//2))+'|'
    else:
        L = 100
        pb = '#'*pf+' '*(L-pf)+'|'
    if style==1:
        print(st+A[i%len(A)]+'|'+pb+title,end='\r', flush=True)
    elif style==2:
        print(st+pb+str(N)+'\\'+str(i+1)+'|'+title,end='\r', flush=True)
    if pf==100 and selfTerminate:
        print('')


def ProgBar_float(i,N,title='',style=1,L=50,selfTerminate=True,delta=None):

    pf = np.around(100*(i+1)/float(N),2)
    st = ' '*(5-len(str(pf))) + str(pf) +'%|'

    if L==50:
        pb = '#'*int(pf//2)+' '*(L-int(pf//2))+'|'
    else:
        L = 100
        pb = '#'*int(pf)+' '*(L-int(pf))+'|'
    if style==1:
        print(st+A[i%len(A)]+'|'+pb+title,end='\r', flush=True)
    elif style==2:
        print(st+pb+str(N)+'\\'+str(i+1)+'|'+title,end='\r', flush=True)
    if pf==100 and selfTerminate:
        print('\nDone..')

# EXPERIMENTAL #TODO
def write_numpy_edf(data_array, fname, info={}, tmin=0, tmax=None, overwrite=False,dimension='uV',dmul=1e6):
    import pyedflib # pip install pyedflib
    from pyedflib import highlevel # new high-level interface
    from pyedflib import FILETYPE_BDF, FILETYPE_BDFPLUS, FILETYPE_EDF, FILETYPE_EDFPLUS
    from datetime import datetime, timezone, timedelta
    #import mne
    import os
    """
    EXPERIMENTAL
    ------------------
    Saves data to a file using the EDF+/BDF filetype
    pyEDFlib is used to save the raw contents of the RawArray to disk
    Parameters
    ----------
    data_array : data with shape (nch, n)
    fname : string
        File name of the new dataset. This has to be a new filename
        unless data have been preloaded. Filenames should end with .edf
    tmin : float | None
        Time in seconds of first sample to save. If None first sample
        is used.
    tmax : float | None
        Time in seconds of last sample to save. If None last sample
        is used.
    overwrite : bool
        If True, the destination file (if it exists) will be overwritten.
        If False (default), an error will be raised if the file exists.
    """
    #if not issubclass(type(mne_raw), mne.io.BaseRaw):
    #    raise TypeError('Must be mne.io.Raw type')
    if not overwrite and os.path.exists(fname):
        raise OSError('File already exists. No overwrite.')

    # static settings
    #has_annotations = True if len(mne_raw.annotations)>0 else False
    if os.path.splitext(fname)[-1] == '.edf':
        #file_type = FILETYPE_EDFPLUS if has_annotations else FILETYPE_EDF
        file_type = FILETYPE_EDF
        dmin, dmax = -32768, 32767
    else:
        #file_type = FILETYPE_BDFPLUS if has_annotations else FILETYPE_BDF
        file_type = FILETYPE_BDF
        dmin, dmax = -8388608, 8388607

    print('saving to {}, filetype {}'.format(fname, file_type))
    #sfreq = mne_raw.info['sfreq']
    #date = _stamp_to_dt(mne_raw.info['meas_date'])

    sfreq = info['fs']
    date_of_data = info['date'] if 'data' in info.keys() else datetime.today()

    if tmin:
        date += timedelta(seconds=tmin)
    # no conversion necessary, as pyedflib can handle datetime.
    #date = date.strftime('%d %b %Y %H:%M:%S')
    first_sample = int(sfreq*tmin)
    last_sample  = int(sfreq*tmax) if tmax is not None else None


    # convert data
    #channels = mne_raw.get_data(picks,
    #                            start = first_sample,
    #                            stop  = last_sample)

    channels = data_array
    # convert to microvolts to scale up precision
    channels *= dmul

    # set conversion parameters
    n_channels = len(channels)

    # create channel from this
    try:
        f = pyedflib.EdfWriter(fname, n_channels=n_channels, file_type=file_type)

        channel_info = []

        ch_idx = range(n_channels)
        #keys   = list(mne_raw._orig_units.keys())
        for i in ch_idx:
            ch_dict = {'label': info['ch_names'][i],
                       'dimension': dimension,
                       'sample_rate': sfreq,
                       'physical_min': channels.min(),
                       'physical_max': channels.max(),
                       'digital_min':  dmin,
                       'digital_max':  dmax,
                       'transducer': '',
                       'prefilter': ''}

            channel_info.append(ch_dict)

        f.setPatientCode(info['subject_info'].get('id', '0'))
        f.setPatientName(info['subject_info'].get('name', 'noname'))
        f.setTechnician('phyaat')
        f.setSignalHeaders(channel_info)
        f.setStartdatetime(date_of_data)
        f.writeSamples(channels)
    except Exception as e:
        raise e
    finally:
        f.close()
    return True
