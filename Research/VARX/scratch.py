import pandas as pd

df = pd.read_csv('data_csvs/train_1m.csv')
nans = lambda df: df[df.isnull().any(axis=1)]
print(nans(df))