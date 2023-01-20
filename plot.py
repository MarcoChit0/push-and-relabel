from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import seaborn as sns

inputpath = 'data/'
outputpath = 'plot/'
filenames = ['0.2', '0.3', '0.4', '0.5', '0.6'] 
inputformat = '.csv'
outputformat = '.png'
for filename in filenames:
    df = pd.read_csv(inputpath + filename + inputformat)

    # head columns
    # num_vertex,num_edges,maxflow,delta_t,num_pushes,num_relabels
    mean_df = df.groupby(['num_vertex']).mean().reset_index()
    plt.clf()
    ax = plt.subplots()
    sns.lmplot(
        data=mean_df, x='num_vertex',y='delta_t',order=2, ci=None, scatter_kws={"s": 10}, line_kws={'lw':2, "color": "red"}
    ).set(title='P=' + filename + ': tempo real')
    plt.xlabel(xlabel='número de vértices')
    plt.ylabel(ylabel='tempo (s)')
    plt.savefig(outputpath + filename + outputformat)
    plt.clf()
    mean_df['comp'] = mean_df['delta_t']/ (pow(mean_df['num_vertex'], 2) * mean_df['num_edges'])
    sns.lmplot(
        data=mean_df, x='num_vertex', y='comp', order=8, ci=None, scatter_kws={"s": 10, 'color':'purple'}, line_kws={'lw':2, "color": "green"}
    )
    plt.title('P=' + filename + ': tempo real/ tempo esperado')
    plt.xlabel(xlabel='número de vértices')
    plt.ylabel(ylabel='tempo (s)')
    plt.savefig(outputpath + filename + 'comparision' + outputformat)