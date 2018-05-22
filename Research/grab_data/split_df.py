import pandas as pd

def splitDataFrameIntoSmaller(df, chunkSize = 10000):
    listOfDf = list()
    numberChunks = len(df) // chunkSize + 1
    for i in range(numberChunks):
        listOfDf.append(df[i*chunkSize:(i+1)*chunkSize])
    return listOfDf

eth_df = pd.read_csv('eth.csv')

df_list = splitDataFrameIntoSmaller(eth_df, chunkSize=25000)