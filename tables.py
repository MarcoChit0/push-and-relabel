import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
import os

def append_into_table(t, d, i):
    num_pushes = d['num_pushes'].sum()
    num_relabels = d['num_relabels'].sum()
    max_time = d['delta_t'].max()
    mean_time = d['delta_t'].mean()
    total_time = d['delta_t'].sum()
    comp_time = d['delta_t'].iloc[-1] / (pow(d['num_vertex'].iloc[-1],2)*d['num_edges'].iloc[-1])

    t.loc[i] = [
        str(int(f'{num_pushes:.0f}')),
        str(int(f'{num_relabels:.0f}')), 
        str(float(f'{mean_time:.2f}')),
        str(float(f'{max_time:.2f}')),
        str(float(f'{total_time:.2f}')),
        str(float(f'{comp_time*pow(10, 10):.2f}'))]

inputpath = 'data/'
outputpath = 'tables/'
filenames = ['0.2', '0.3', '0.4', '0.5', '0.6'] 
inputformat = '.csv'
outputformat = '.tex'

columns = ['pushes', 'relabels', 'mean_time', 'max_time', 'total_time', 'comp_time*pow(10,10)']
column_format = 'c|cccccc'

t1 = pd.DataFrame(columns = columns, index=filenames)
t2 = pd.DataFrame(columns = columns, index=filenames)
t3 = pd.DataFrame(columns = columns, index=filenames)

for filename in filenames:
    df = pd.read_csv(inputpath + filename + inputformat)
    df100 = df.loc[lambda row: row["num_vertex"] <= 100].groupby(['num_vertex']).mean().reset_index()
    df200 = df.loc[lambda row: 100 < row["num_vertex"]].loc[lambda row: row["num_vertex"] <= 200].groupby(['num_vertex']).mean().reset_index()
    df300 = df.loc[lambda row: 200 < row["num_vertex"]].loc[lambda row: row["num_vertex"] <= 300].groupby(['num_vertex']).mean().reset_index()
    append_into_table(t1, df100, filename)
    append_into_table(t2, df200, filename)
    append_into_table(t3, df300, filename)

t1.to_latex(outputpath + 't1' + outputformat, caption='N=[10..100]', column_format=column_format)
t2.to_latex(outputpath + 't2' + outputformat, caption='N=[101..200]', column_format=column_format)
t3.to_latex(outputpath + 't3' + outputformat, caption='N=[201..300]', column_format=column_format)