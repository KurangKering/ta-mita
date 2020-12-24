import numpy as np 
import pandas as pd


def normalisasi(df):
	df_input = df.loc[:, ~df.columns.isin(['id'])]
	df_min = np.min(df_input, axis=0)
	df_max = np.max(df_input, axis=0)
	df_input_norm = (df_input - df_min) / (df_max - df_min)
	df_norm = pd.concat([df['id'], df_input_norm], axis=1)
	return df_norm