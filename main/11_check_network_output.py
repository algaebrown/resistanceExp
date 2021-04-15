########## Domain #############
from scipy.sparse import load_npz
import numpy as np
import pandas as pd
from itertools import combinations

binary_matrix = load_npz('/nas2/users/hermuba/resist_subnet/domain/domain_binary.npz')
non_zero_genes = np.where(np.sum(binary_matrix, axis = 1)>0)[0]
df = pd.read_csv('/nas2/users/hermuba/resist_subnet/domain/network.csv', header = None)[[0,1]] 

sucess_task = set([tuple(x) for x in df.to_numpy()])
all_index_combine = set(combinations(list(non_zero_genes), 2))
failed_task = list(all_index_combine - sucess_task)
print('DOMAIN failed task: {}'.format(len(failed_task)))

########## ESKAPE ###############
binary_matrix = load_npz('/nas2/users/hermuba/resist_subnet/eskape/binned.pivot.npz')
non_zero_genes = np.where(np.sum(binary_matrix, axis = 1)>0)[0]
df = pd.read_csv('/nas2/users/hermuba/resist_subnet/eskape/network.csv', header = None)[[0,1]] 

sucess_task = set([tuple(x) for x in df.to_numpy()])
all_index_combine = set(combinations(list(non_zero_genes), 2))
failed_task = list(all_index_combine - sucess_task)
print('ESKAPE failed task: {}'.format(len(failed_task)))

########## ESKAPE ###############
binary_matrix = load_npz('/nas2/users/hermuba/resist_subnet/refseq/binned.pivot.npz')
non_zero_genes = np.where(np.sum(binary_matrix, axis = 1)>0)[0]
df = pd.read_csv('/nas2/users/hermuba/resist_subnet/refseq/network.csv', header = None)[[0,1]] 

sucess_task = set([tuple(x) for x in df.to_numpy()])
all_index_combine = set(combinations(list(non_zero_genes), 2))
failed_task = list(all_index_combine - sucess_task)
print('REFSEQ failed task: {}'.format(len(failed_task)))