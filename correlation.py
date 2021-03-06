import seaborn as sns
import numpy as np
import pickle
import pandas as pd
import matplotlib.pyplot as plt

#Import file from the pickle
with open('readings.pickle', 'rb') as f: 
    dictCount = pickle.load(f)
    alcDictList = pickle.load(f)
    conDictList = pickle.load(f)
    readingsDataframeList = pickle.load(f)

#for simplicity        
readingsDataframe = readingsDataframeList[0]    

#correlation matrix
corr_df = readingsDataframe.corr(method='pearson')
#_________plotting correlation matrix_______________________________

sns.heatmap(corr_df, cmap='RdYlGn_r' , linewidths=2.5)
# Show the plot we reorient the labels for each column and row to make them easier to read.
plt.yticks(rotation=0) 
plt.xticks(rotation=90) 
plt.show()  
#___________________________________________
#plotting half correlation matrix
mask = np.zeros_like(corr_df)
mask[np.triu_indices_from(mask)] = True
with sns.axes_style("white"):
    ax = sns.heatmap(corr_df,cmap='RdYlGn_r', mask=mask, vmax=.3, square=True)

tempdf = readingsDataframe.drop('category',1)

#__________________higher correlation pairs__________________
def get_redundant_pairs(df):
    '''Get diagonal and lower triangular pairs of correlation matrix'''
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop

def get_top_correlations(df, n=5):
    au_corr = df.corr().unstack()
    labels_to_drop = get_redundant_pairs(df)
    #reset index makes all pairs printable or some pairs are printed partially
    au_corr_pos = au_corr.drop(labels_to_drop).sort_values(ascending=False).reset_index()
    au_corr_neg = au_corr.drop(labels_to_drop).sort_values().reset_index()
    return au_corr_pos[0:n], au_corr_neg[0:n]

print("Top Correlation pairs:")
pairCount = 10

posCorrPairs, negCorrPairs = get_top_correlations(tempdf, pairCount)
print('Positive Correlation pairs:',posCorrPairs,'Negative Correlation pairs:',negCorrPairs)
