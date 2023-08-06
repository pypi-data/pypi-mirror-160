import sys
import os.path as o
#use if running from dance/examples/spatial/cell_type_deconvo
root_path=o.abspath(o.join(o.dirname(sys.modules[__name__].__file__), "../../.."))
sys.path.append(root_path)

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import optim

from dance.datasets.spatial import CellTypeDeconvoDataset
from dance.modules.spatial.cell_type_deconvo.spatialdecon import SpatialDecon
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# get data 
dataset = CellTypeDeconvoDataset("toy2", data_dir="data/spatial")

X=np.array(dataset.data['ref_sc_count'])
Y=np.array(dataset.data['mix_count'])

#set cell-types 
cell_types =np.array([np.repeat(i+1, X.shape[1]//3) for i in range(3)]).flatten()

def cell_topic_profile(X, groups,axis=0, method='median'):
    ids=np.unique(groups)
    if method == "median":
        X_profile = np.array([np.median(X[:, groups==ids[i]], axis=1) for i in range(len(ids))]).T
    else:
        X_profile = np.array([np.mean(X[:, groups==ids[i]], axis=1) for i in range(len(ids))]).T
    return X_profile
X_profile = cell_topic_profile(X, cell_types, 0, "mean" )


y=Y[:,:5]
print(y.shape)
x=X_profile
print(x.shape)

torch.manual_seed(17)
#run deconvolution with logNormReg (multiplicative log-normal errors)
deconLNR = SpatialDecon(in_dim=x.shape[1], out_dim=y.shape[1], device=device) #,sd=.13, mu=.4)
deconLNR.fit(x, y, max_iter=4000, lr=.0001)
proportion_preds = deconLNR.predict().clone().detach()
print('MSLE score:',deconLNR.score(x, y))
print('Predicted Proportions:', proportion_preds)