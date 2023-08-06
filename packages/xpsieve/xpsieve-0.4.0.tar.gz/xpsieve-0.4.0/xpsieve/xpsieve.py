import pandas as pd
import warnings
import copy
import pandas as pd
import numpy as np
from collections import Iterable
from pandas.core.base import PandasObject
from IPython.display import display, HTML
import html
from dataclasses import dataclass
from string import Template

def read_wandb(project_name, exclude_gradients=True):
    """source: https://docs.wandb.ai/guides/track/public-api-guide"""
    import wandb
    api = wandb.Api(timeout=49)
    runs = api.runs(project_name)
    summary_list = [] 
    config_list = [] 
    name_list = []
    condition = lambda x: ('gradients/' not in x) if exclude_gradients else True
    for run in runs: 
        # run.summary are the output key/values like accuracy.  We call ._json_dict to omit large files 
        summary_list.append({k:v for k,v in run.summary._json_dict.items() if condition(k)}) 
        # run.config is the input metrics.  We remove special values that start with _
        config_list.append({k:v for k,v in run.config.items() if not ('hash' not in k and k.startswith('_'))}) 
        # run.name is the name of the run.
        name_list.append(run.name)       
    summary_df = pd.DataFrame.from_records(summary_list) 
    config_df = pd.DataFrame.from_records(config_list) 
    name_df = pd.DataFrame({'name': name_list}) 
    return pd.concat([name_df, config_df,summary_df], axis=1)

def sieve(df,d=dict(), **kwargs):
    df=df.copy()
    for k,v in {**d, **kwargs}.items():
        if type(v)!=list:
            v=[v]
        df=df[df[k].map(lambda x:x in v)]
    return df

def drop_constant(df):
    df=df.copy()
    return df.loc[:,df.astype(str).nunique()!=1]

class Stat():
    
    def __init__(self, mean=0.0, std=0.0, template='$mean±$std',precision=3):
        self.mean, self.std = mean, std
        self.template=template
        self.precision=precision

    def __repr__(self):
        return self.template.sub(mean=format(self.mean, f'.{self.precision}f'),
                                 std=format(self.std,  f'.{self.precision}f'))
    def __float__(self):
        return float(self.mean)

    def __sub__(self,other):
        return float(self.mean-other.mean)
    
    def __lt__(self,other):
        if np.isnan(self.mean):
            return True
        if np.isnan(other.mean):
            return False
        return self.mean<other.mean

    def __eq__(self,other):
        return self.mean==other.mean
    
    def mean(l, **kwargs):
        return Stat(mean=np.mean(l), std=np.std(l), **kwargs)
    

def show(df,n=20,random=False,escape=True,sep_width=120):
    '''Aesthethic visualization of data with multiple (possibly long) text fields)'''
    df=df.copy()
    length=len(df)
    if random: 
        df=df.sample(frac=1.0)
    df=df.head(n)
    
    if hasattr(df,'columns'):
        for c in df.columns:
            df[c]='•'+df[c].map(str).map(str.strip)
    df.index=['─'*sep_width]*len(df)

    s=df.to_csv(None,sep="\n")
    if escape:
        s=html.escape(s)
    s=f'length:{length}\n{s}'.replace('\n','<br>')
    return HTML(f'<font face="Arial" size="2px">{s}</font>')

def rshow(df,n=20):
    '''Aesthethic visualization of data with multiple (possibly long) text fields)'''
    return show(df,n,random=True)


PandasObject.bold = lambda x: x.copy().apply(bold)                                             
PandasObject.show = show
PandasObject.rshow = rshow
pd.read_wandb = read_wandb
PandasObject.drop_constant=drop_constant
PandasObject.sieve=sieve
