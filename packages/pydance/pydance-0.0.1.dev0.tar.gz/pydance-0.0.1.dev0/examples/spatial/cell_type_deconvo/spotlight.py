import sys
import os.path as o
#use if running from dance/examples/spatial/cell_type_deconvo
root_path=o.abspath(o.join(o.dirname(sys.modules[__name__].__file__), "../../.."))
sys.path.append(root_path)


from dance.datasets.spatial import CellTypeDeconvoDataset
from dance.modules.spatial.cell_type_deconvo.spotlight import SPOTlight
import numpy as np
# get data 
dataset = CellTypeDeconvoDataset("toy2", data_dir="data/spatial")

X=np.array(dataset.data['ref_sc_count'])
Y=np.array(dataset.data['mix_count'])

#set cell-types 
cell_types = cell_types=np.array([np.repeat(i+1, X.shape[1]//3) for i in range(3)]).flatten()

#run deconvolution with SPOTlight (NMFReg + additional NNLS layer) - set rank for NMF dim red.
decon_model = SPOTlight(rank=10, bias=False)

#fit using reference scRNA X, with cell_type labels
decon_model.fit(X, Y, cell_types)
print(decon_model.P[:,:3])
#decon_model.P gives fitted cell-type proportions for Y 

#predict proportions at given spot 
prop_preds=decon_model.predict(Y[:,0])

#score model
print('Score:', decon_model.score(X, Y, cell_types))