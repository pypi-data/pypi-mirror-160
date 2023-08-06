import numpy as np
import re
import warnings

__all__ = ('get_number_and_suffix', 'time_str_to_freq_str', 'frequency_suffix_to_scientific_str', 'current_suffix_to_scientific_str', 
    'scientific_str_to_time_suffix', 'voltage_suffix_to_scientic_str', 'time_suffix_to_scientic_str', 
    'voltage_amp_mapper', 'freq_mapper','sci_to_freq_mapper', 'current_amp_mapper', 'time_to_sci_mapper','sci_to_time_mapper',
    '_get_number_and_suffix', 'scientific_notation', 'add_time_strings')

freq_mapper = {'Mhz':'e6','khz':'e3', 'hz':'e0', 'mhz':'e-3', 'MHz':'e6', 'kHz':'e3','Hz':'e0', 'mHz':'e-3', '':''}
sci_to_freq_mapper = {'e6':'Mhz','e3':'kHz', 'e0':'Hz','e-3':'mHz', '':''}
current_amp_mapper = {'ma':'e-3', 'ua':'e-6', 'na':'e-9', 'mA':'e-3', 'uA':'e-6', 'nA':'e-9', '':''}
sci_to_time_mapper = {'e0':'s', 'e3':'ks', 'e-3':'ms', 'e-6':'us', 'e-9':'ns', '':''}
voltage_amp_mapper = {'mv':'e-3', 'v':'e0', 'mV':'e-3','V':'e0','kV':'e3','kv':'e3', '':''}
time_to_sci_mapper = {'ms':'e-3', 'us':'e-6', 'ns':'e-9', 'ps':'e-12', 's':'e0', 'ks':'e3', '':''}

def add_time_strings(str1, str2):
    """Returns a string in units of str1"""
    n1, s1 = get_number_and_suffix(str1)
    n2, s2 = get_number_and_suffix(str2)
    unit_multiplier = 1/float('1'+time_suffix_to_scientic_str(s1))
    
    float_total = (n1*float('1'+time_suffix_to_scientic_str(s1)) + 
                  n2*float('1'+time_suffix_to_scientic_str(s2)))
    
    return str(np.round(float_total*unit_multiplier, 5)) + s1

def time_str_to_freq_str(time_str):
    """Converts a time string to its reciprocal frequency string. *i.e* '1ms' -> '1kHz'
    
    args:
        time_str (str): Time string to convert

    returns:
        (str): Frequency string.
    """
    
    period_number, period_suffix = get_number_and_suffix(time_str)
    assert period_suffix in set(time_to_sci_mapper.keys()), "time_str {} not in time_to_sci_mapper. Allowed keys are {}".format(time_str, list(time_to_sci_mapper.keys()))
    period_suffix = time_to_sci_mapper[period_suffix]
    freq_number = 1/(float(str(period_number) + period_suffix))
    freq_str = "{:3e}".format(freq_number)
    freq_num, freq_suffix = get_number_and_suffix_regex(freq_str)
    power = int(freq_suffix[1:])
    if power % 3 != 0:
        if (power - 1) % 3 != 0:
            power = power - 2
            freq_num = freq_num*100
        else:
            power = power - 1
            freq_num = freq_num*10
        freq_suffix = 'e' + str(power)
    assert freq_suffix in set(sci_to_freq_mapper.keys()), "freq_suffix {} not in sci_to_freq_mapper. Allowed keys are {}".format(freq_suffix, list(sci_to_freq_mapper.keys()))
    return str(round(freq_num)) + sci_to_freq_mapper[freq_suffix]


def scientific_str_to_time_suffix(sci_str):
    """Convert scientific notation string to suffix for time. *i.e.* 'e-9' -> 'ns'

    args:
        sci_str (str): Scientific string to convert

    returns:
        (str): Time suffix
    """
    assert sci_str in set(sci_to_time_mapper.keys()), "sci_str {} not in sci_to_time_mapper. Allowed keys are {}".format(sci_str, list(sci_to_time_mapper.keys()))
    return sci_to_time_mapper[sci_str]

def time_suffix_to_scientic_str(time_suffix):
    """Convert time suffix to scientific. *i.e.* 'ms' -> 'e-3'.

    args:
        time_suffix (str): Suffix to convert

    returns:
        (str): Scientific notation str
    """
    assert time_suffix in set(time_to_sci_mapper.keys()), "time_suffix {} not in time_to_sci_mapper. Allowed keys are {}".format(time_suffix, list(time_to_sci_mapper.keys()))
    return time_to_sci_mapper[time_suffix]

def voltage_suffix_to_scientic_str(volt_suffix):
    """Convert voltage suffix to scientific. *i.e.* 'mV' -> 'e-3'.

    args:
        volt_suffix (str): Suffix to convert

    returns:
        (str): Scientific notation str
    """
    assert volt_suffix in set(voltage_amp_mapper.keys()), "volt_suffix '{}' not in voltage_amp_mapper. Allowed keys are {}".format(volt_suffix, list(voltage_amp_mapper.keys()))
    return voltage_amp_mapper[volt_suffix]

def frequency_suffix_to_scientific_str(freq_suffix):
    """Convert frequency suffix to scientific. *i.e.* 'MHz' -> 'e6'

    args:
        freq_suffix (str): Suffix to convert

    returns:
        (str): Scientific notation str
    """
    freq_suffix = freq_suffix.replace('H', 'h').replace('Z', 'z')
    assert freq_suffix in set(freq_mapper.keys()), "Suffix '{}'' not in freq_mapper. Allowed keys are {}".format(freq_suffix, list(freq_mapper.keys()))
    return freq_mapper[freq_suffix]

def current_suffix_to_scientific_str(current_suffix):
    """Convert current suffix to scientific. *i.e.* 'mA' -> 'e-3'

    args:
        current_suffix (str): Suffix to convert

    returns:
        (str): Scientific notation str
    """
    assert current_suffix in set(current_amp_mapper.keys()), "Suffix '{}'' not in current_amp_mapper. Allowed keys are {}".format(current_suffix, list(current_amp_mapper.keys()))
    return current_amp_mapper[current_suffix]

def get_number_and_suffix(string):
    """Return number and suffix of a string.

    args:
        string (str): String.

    returns:
        (tuple): number, suffix

    examples:
        ```
        >>> get_number_and_suffix('1khz')
        > (1.0, 'khz')
        ```


    """
    return get_number_and_suffix_regex(string)

def _get_number_and_suffix2(string):
    """Return number and suffix of a string. e.g. 1khz will return (1.0, 'khz').

    args:
        string (str): String.

    returns:
        (tuple): number, suffix


    """
    iteration = 0
    number = np.nan
    while np.isnan(number):
        if iteration >= len(string):
            raise ValueError('unable to find a valid number in str: {}'.format(string))
        try:
            number = float(string[:-(1+iteration)])
        except ValueError:
            iteration+=1
            
    return number, string[-(iteration + 1):]

def get_number_and_suffix_regex(string):
    """Return number and suffix of a string. e.g. 1khz will return (1.0, 'khz').
    Formats python scientific notation to simplified form e.g. (case insensitive)
    3E+06 -> (3.0, e6), 3e+06 -> (3.0, e6), 1e12 -> (1.0, e12).

    args:
        string (str): String.

    returns:
        (tuple): number, suffix


    """
    string = string.lower()
    res = re.search(r'^[-0-9.]+',string)
    if res is None:
        raise ValueError('unable to find a valid number in str: {}'.format(string))
    number = float(string[:res.end()])
    suffix = string[res.end():]
    res = re.search(r'[+-]', suffix)
    if res != None:
        index = res.start()
        if suffix[index + 1] == '0':
            suffix = suffix[:index + 1] + suffix[index + 2:]
        if suffix[index] == '+':
            suffix = suffix[:index] + suffix[index + 1:]
    return number, suffix


def _get_number_and_suffix(string):
    """Return number and suffix of a string. e.g. 1khz will return (1.0, 'khz').

    args:
        string (str): String.

    returns:
        (tuple): number, suffix


    """
    warnings.showwarning("_get_number_and_suffix is deprecated. Please use get_number_and_suffix instead.", DeprecationWarning, '', '')
    iteration = 0
    number = np.nan
    while np.isnan(number):
        if iteration >= len(string):
            raise ValueError('unable to find a valid number in str: {}'.format(string))
        try:
            number = float(string[:-(1+iteration)])
        except ValueError:
            iteration+=1
            
    return number, string[-(iteration + 1):]

def scientific_notation(number):
    """Return a string of a number in scientific notation.

    args:
        number (int or float): Number

    returns:
        (str): String of number in scientific notation. 


    """
    return _scientific_notation(number)

def _scientific_notation(number):
    number = float(number)

    if len(str(number).split('e'))>1:
        out = str(number)
    else:
        number_string = str(number)
        before_decimal, after_decimal = number_string.split('.')
        if before_decimal[0] == '0' and len(before_decimal) == 1:
            #the hard case

            n_zeros_after_decimal = 0
            for x in after_decimal:
                if x == '0':
                    n_zeros_after_decimal += 1
                else:
                    break
            exponent = -(1 + n_zeros_after_decimal)
            out = '{}.{}e{}'.format(
                after_decimal[n_zeros_after_decimal], 
                after_decimal[n_zeros_after_decimal+1:],
                exponent
            )
        else:
            #the easy case
            exponent = len(before_decimal) - 1
            out = '{}.{}e{}'.format(
                before_decimal[0], 
                before_decimal[1:] + after_decimal, 
                exponent
            )
    return out