import pandas as pd
import numpy as np

__all__ = ('load_radiant_loop_from_text_file','convert_pCum2_to_uCcm2')

def load_radiant_loop_from_text_file(file, measured_value = 'Charge', return_meta_data = False, delimiter = ','):
    """Load a radiant loop from a text file. Typically one would use 'Charge' for measured_value unless one accurately measured capacitor area and input correctly into the Radiant UI.

    args:
        file (str): Filename and path. 
        measured_value (str): 'Charge' or 'Polarization'
        return_meta_data (bool): Return meta data (dict)

    returns:
        (pandas.DataFrame, (dict)): Data, Optional: (meta data)



    """
    
    if measured_value.lower() not in set({'charge', 'polarization'}):
        raise ValueError('measured_value {} not supported. must be either "charge" or "polarization"'.format(measured_value))
        
        
    with open(file, 'rb') as f:
        lines = f.readlines()

    newlines = []

    for i, line in enumerate(lines):
        #radiant's file structure is the worst
        newlines.append(str(line.decode('windows-1252').replace('»', '').replace('«', '').replace(' ', '').replace('\r', '').replace('\n', '').replace('µ', 'u')))

    lines = newlines

    meta_data = dict()
    data = []
    for line in lines:
        spl = line.split(':,')
        if len(spl)>1: #often there is a comma before the actual data. why? who knows! this is the case where there exists such a comma
            meta_data.update({spl[0]:spl[1]})
            continue
        #now try the case with no comma:
        spl = line.split(':')
        if len(spl)>1: 
            meta_data.update({spl[0]:spl[1]})
            continue
        else:
            data.append(line)

    out = dict()
    i = 0 #counter for when we have established column names

    pointer_dict = dict() #holds which column index points to which column name
    for row in data:
        spl = row.split(delimiter)
        if len(spl)<=1: #there are some rows in here which are not data and they are therefor not comma sep
            continue

        if i == 0: #establish column names
            out.update({spl[a]:[] for a in range(len(spl))})
            pointer_dict.update({a:spl[a] for a in range(len(spl))})
            i+=1
            continue

        try:
            for ijk, a in enumerate(spl):
                out[pointer_dict[ijk]].append(float(a))
        except ValueError: #could not convert to float (i.e. nonnumeric data)
            continue
        
    out = pd.DataFrame(out)
    if len(out) == 0:
        raise ValueError('No data. Is your delimiter correct?')
    out.drop(columns = ['Point'], inplace = True)

    
    if measured_value.lower() == 'charge':
        out['MeasuredPolarization'] = out['MeasuredPolarization']*float(meta_data['SampleArea(cm2)'])*1e6 #to convert from uC to pC
        out.rename(columns = {'MeasuredPolarization':'MeasuredCharge(pC)'}, inplace = True)
    elif measured_value.lower() == 'polarization':
        out.rename(columns = {'MeasuredPolarization':'MeasuredPolarization(uC/cm2)'}, inplace = True)
        
    if return_meta_data:
        return out, meta_data
        
    return out
    
def convert_pCum2_to_uCcm2(value):
    """Convert from picocoulombs/um^2 to microcoulombs/cm^2. This is simply multpilying by 100, but it's a calculation I do a lot and always have to look up to make sure I'm correct.

    args:
        value (float): Value to convert.

    returns:
        (float): value*100

    """
    return value*100