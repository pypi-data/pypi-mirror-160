import pandas as pd
import numpy as np

import warnings

from .core import Dataset, Data
from .core import _convert_ITP_to_path_to_index

__all__ = ('merge','merge_Datasets', 'merge_Datas')

def merge_Datas(datas):
	"""Merge data.

	args:
		datas (iter of Data): Iterable of Data objects to merge.

	returns:
		(Data): Merged data.

	"""

	if not hasattr(datas, '__iter__'):
		raise TypeError('datas is not iterable.')

	for i, data in enumerate(datas):
		if i == 0:
			out = data.to_dict().copy()
			continue
		tmp = data.to_dict()
		current_len = len(out)
		for index in tmp:
			out.update({current_len+index:tmp[index]})

	return Data(out)

def merge_Datasets(datasets):
	"""Merge datasets.

	args:
		datasets (iter of Dataset): Iterable of Dataset objects to merge.

	returns:
		(Dataset): Merged dataset.

	"""
	
	if not hasattr(datasets, '__iter__'):
		raise TypeError('datasets is not iterable.')
		
	columns = datasets[0].columns
	for dset in datasets[1:]:
		if len(columns) != len(dset.columns):
			raise ValueError('supplied datasets do not all have the same columns!')
		if (columns != dset.columns).all():
			raise ValueError('supplied datasets do not all have the same columns!')
	
	for i, dset in enumerate(datasets):
		if i == 0:
			new_path = dset.index_to_path
			new_df = pd.DataFrame(dset)
		else:
			new_path = pd.concat((new_path, dset.index_to_path), ignore_index = True)
			new_df = pd.concat((new_df, pd.DataFrame(dset)), ignore_index = True)
			
	path = _convert_ITP_to_path_to_index(new_path)
	
	return Dataset(path,new_df)

def merge(datasets):
	"""Merge datasets.

	args:
		datasets (iter of Dataset): Iterable of Dataset objects to merge.

	returns:
		(Dataset): Merged dataset.

	"""
	warnings.showwarning('merge() is deprecated. use merge_Datasets() instead', DeprecationWarning, '', 0,)
	
	if not hasattr(datasets, '__iter__'):
		raise TypeError('datasets is not iterable.')
		
	columns = datasets[0].columns
	for dset in datasets[1:]:
		if len(columns) != len(dset.columns):
			raise ValueError('supplied datasets do not all have the same columns!')
		if (columns != dset.columns).all():
			raise ValueError('supplied datasets do not all have the same columns!')
	
	for i, dset in enumerate(datasets):
		if i == 0:
			new_path = dset.index_to_path
			new_df = pd.DataFrame(dset)
		else:
			new_path = pd.concat((new_path, dset.index_to_path), ignore_index = True)
			new_df = pd.concat((new_df, pd.DataFrame(dset)), ignore_index = True)
			
	path = _convert_ITP_to_path_to_index(new_path)
	
	return Dataset(path,new_df)