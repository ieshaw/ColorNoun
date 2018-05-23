import pandas as pd

df = pd.read_csv('eth.csv')
df['diff'] = df.open_time - df.open_time.shift(-1)
df['prev'] = df.open_time.shift(-1)
df.prev += 60000
missing_data = df.loc[df['diff'] > 60000].copy()
missing_tuples = list(zip(missing_data.prev.astype(int), missing_data.open_time.astype(int)))
print(missing_tuples)