import sys
import os.path as o
#use if running from dance/examples/spatial/cell_type_deconvo
root_path=o.abspath(o.join(o.dirname(sys.modules[__name__].__file__), "../../.."))
sys.path.append(root_path)


from dance.datasets.spatial import CellTypeDeconvoDataset
from dance.transforms.preprocess import pseudo_spatial_process, preprocess_adj, split
from dance.transforms.graph_construct import stAdjConstruct
import torch
import torch.nn.functional as F
import numpy as np
import scanpy as sc
import random
from dance.modules.spatial.cell_type_deconvo.dstg import DSTGLearner
# Set random seed
seed = 123
np.random.seed(seed)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


import warnings
warnings.filterwarnings("ignore")


# get data 
dataset = CellTypeDeconvoDataset("toy1", data_dir="data/spatial")
## dataset.data has repeat name , be careful

count_data = [sc.AnnData(dataset.data['ref_sc_count']), sc.AnnData(dataset.data['mix_count'])]
label_data = [dataset.data['ref_sc_annot'], dataset.data['mix_annot']]
#pre-process: get variable genes --> normalize --> log1p --> standardize --> out
#set scRNA to false if already using pseudo spot data with real spot data
st_data, labels, hvgs = pseudo_spatial_process(count_data, label_data, scRNA=False)

# create train/val/test split
adj_data, features, labels_binary_train, labels_binary_val, labels_binary_test, train_mask, pred_mask, val_mask, test_mask, new_label, true_label = split(st_data, label_data, pre_process=1, split_val=.8)

labels_binary_train=torch.FloatTensor(labels_binary_train)

features = torch.sparse.FloatTensor(torch.LongTensor([features[0][:,0].tolist(), features[0][:,1].tolist()]),
                                  torch.FloatTensor(features[1]))


#construct adjacency matrix
adj = stAdjConstruct(st_data, label_data, adj_data, k_filter=200)
#preprocess adjacency matrix
adj = preprocess_adj(adj)

adj = torch.sparse.FloatTensor(torch.LongTensor([adj.row.tolist(), adj.col.tolist()]),
                              torch.FloatTensor(adj.data.astype(np.int32)))




# Create model
model_func = DSTGLearner
model = model_func(nfeat=features.size()[1], nhid1=32, nout=labels_binary_train.size()[1], device=device, bias=False, dropout=0,act=F.relu)

#fit model
model.fit(features, adj, labels_binary_train, labels_mask=torch.FloatTensor(train_mask), lr=0.01, max_epochs=200, weight_decay=0)

#predict on both pseudo & real ST data
preds = model.predict(features, adj)

#score
print('Score:', model.score(X=features, adj=adj, labels=labels_binary_train, labels_mask=torch.FloatTensor(train_mask)).item() )
