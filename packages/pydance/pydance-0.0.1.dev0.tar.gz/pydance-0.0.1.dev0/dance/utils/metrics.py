# Copyright 2022 DSE lab.  All rights reserved.
from scipy import sparse
import torch
from networkx.algorithms import bipartite
import numpy as np
import scib
import scanpy as sc
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
from sklearn.metrics.cluster import normalized_mutual_info_score
from sklearn.metrics import adjusted_rand_score
import random
import pylab as plt
import seaborn as sns
from scipy import sparse


def get_bipartite_matching_adjacency_matrix_mk3(raw_logits, threshold_quantile=0.995, copy=False):
    #getting rid of unpromising graph connections
    if copy:
        weights = raw_logits.copy()
    else:
        weights = raw_logits
    quantile_row = np.quantile(weights, threshold_quantile, axis=0, keepdims=True)
    quantile_col = np.quantile(weights, threshold_quantile, axis=1, keepdims=True)
    #quantile_minimum = np.minimum(quantile_row, quantile_col, out=quantile_row)
    mask_ = (weights<quantile_row)
    mask_ = np.logical_and(mask_, (weights<quantile_col), out=mask_)
    #weights[weights<quantile_minimum] = 0
    weights[mask_] = 0
    weights_sparse = sparse.csr_matrix(-weights)
    del(weights)
    graph = bipartite.matrix.from_biadjacency_matrix(weights_sparse)
    #explicitly combining top nodes in once component or networkx freaks tf out
    u = [n for n in graph.nodes if graph.nodes[n]['bipartite'] == 0]
    matches = bipartite.matching.minimum_weight_full_matching(graph, top_nodes=u)
    best_matches = np.array([matches[x]-len(u) for x in u])
    bipartite_matching_adjacency = np.zeros(raw_logits.shape)
    bipartite_matching_adjacency[np.arange(raw_logits.shape[0]), best_matches]=1
    return bipartite_matching_adjacency

def batch_separated_bipartite_matching(dataset, emb1, emb2):
    matrix = np.zeros((dataset.modalities[2].shape[0], dataset.modalities[2].shape[0]))
    for b in dataset.modalities[2].obs['batch'].unique():
        i0 = (dataset.modalities[2].obs['batch'] == b).values.nonzero()[0].tolist()
        j0 = (dataset.modalities[3].obs['batch'] == b).values.nonzero()[0].tolist()
        logits = torch.matmul(emb1[i0], emb2[j0].T)
        logits = torch.softmax(logits, -1) + torch.softmax(logits, 0)
        logits = logits.cpu().numpy()

        out1_2 = get_bipartite_matching_adjacency_matrix_mk3(logits, threshold_quantile=0.950)
        matrix[np.ix_(i0, j0)] = out1_2
    return matrix

def get_nmi(adata):
    # print('Preprocessing')
    sc.pp.neighbors(adata, use_rep='X_emb')
    # print('Clustering')
    scib.cl.opt_louvain(
        adata,
        label_key='cell_type',
        cluster_key='cluster',
        plot=False,
        inplace=True,
        force=True
    )
    # print('Compute score')
    score = scib.me.nmi(adata, group1='cluster', group2='cell_type')
    return score

def get_cell_type_ASW(adata):
    return scib.me.silhouette(adata, group_key='cell_type', embed='X_emb')

def get_cell_cycle_conservation(adata, adata_solution):
    recompute_cc = 'S_score' not in adata_solution.obs_keys() or \
            'G2M_score' not in adata_solution.obs_keys()
    organism = adata_solution.uns['organism']
    # print('Compute score')
    score = scib.me.cell_cycle(
        adata_pre=adata_solution,
        adata_post=adata,
        batch_key='batch',
        embed='X_emb',
        recompute_cc=recompute_cc,
        organism=organism
    )
    return score

def get_traj_conservation(adata, adata_solution):
    adt_atac_trajectory = 'pseudotime_order_ATAC' if 'pseudotime_order_ATAC' in adata_solution.obs else 'pseudotime_order_ADT'
    sc.pp.neighbors(adata, use_rep='X_emb')
    obs_keys = adata_solution.obs_keys()
    if 'pseudotime_order_GEX' in obs_keys:
        score_rna = scib.me.trajectory_conservation(
            adata_pre=adata_solution,
            adata_post=adata,
            label_key='cell_type',
            pseudotime_key='pseudotime_order_GEX'
        )
    else:
        score_rna = np.nan

    if adt_atac_trajectory in obs_keys:
        score_adt_atac = scib.me.trajectory_conservation(
            adata_pre=adata_solution,
            adata_post=adata,
            label_key='cell_type',
            pseudotime_key=adt_atac_trajectory
        )
    else:
        score_adt_atac = np.nan

    score_mean = (score_rna + score_adt_atac) / 2
    return score_mean

def get_batch_ASW(adata):
    score = scib.me.silhouette_batch(
        adata,
        batch_key='batch',
        group_key='cell_type',
        embed='X_emb',
        verbose=False
    )
    return score

def get_graph_connectivity(adata):
    sc.pp.neighbors(adata, use_rep='X_emb')
    # print('Compute score')
    score = scib.me.graph_connectivity(adata, label_key='cell_type')
    return score

def knn_accuracy(A, B, k, train_idx, test_idx, metric='l1'):
    nn = NearestNeighbors(k, metric=metric)
    nn.fit(A)
    transp_nearest_neighbor = nn.kneighbors(B, 1, return_distance=False)
    actual_nn = nn.kneighbors(A, k, return_distance=False)
    train_correct = 0
    test_correct = 0

    for i in range(len(transp_nearest_neighbor)):
        if transp_nearest_neighbor[i] not in actual_nn[i]:
            continue
        elif i in test_idx:
            test_correct += 1
        else:
            train_correct += 1

    return train_correct / len(train_idx), test_correct / len(test_idx)

def cluster_acc(y_true, y_pred):
    """
    Calculate clustering accuracy. Require scikit-learn installed
    # Arguments
        y: true labels, numpy.array with shape `(n_samples,)`
        y_pred: predicted labels, numpy.array with shape `(n_samples,)`
    # Return
        accuracy, in [0,1]
    """
    y_true = y_true.astype(np.int64)
    assert y_pred.size == y_true.size
    D = max(y_pred.max(), y_true.max()) + 1
    w = np.zeros((D, D), dtype=np.int64)
    for i in range(y_pred.size):
        w[y_pred[i], y_true[i]] += 1
    from scipy.optimize import linear_sum_assignment as linear_assignment
    ind = np.column_stack(linear_assignment(w.max() - w))
    return sum([w[i, j] for i, j in ind]) * 1.0 / y_pred.size

def labeled_clustering_evaluate(adata, dataset, cluster=10):

    kmeans = KMeans(n_clusters=cluster, n_init=5, random_state=200)

    adata_sol = dataset.test_sol
    # adata.obs['batch'] = adata_sol.obs['batch'][adata.obs_names]
    # adata.obs['cell_type'] = adata_sol.obs['cell_type'][adata.obs_names]
    true_labels = adata_sol.obs['cell_type'].to_numpy()

    pred_labels = kmeans.fit_predict(adata.X)
    NMI_score = round(normalized_mutual_info_score(true_labels, pred_labels, average_method='max'), 3)
    ARI_score = round(adjusted_rand_score(true_labels, pred_labels), 3)

    print('NMI: ' + str(NMI_score) + ' ARI: ' + str(ARI_score))
    return NMI_score, ARI_score


def joint_embedding_competition_score(adata, adata_sol):
    sc._settings.ScanpyConfig.n_jobs = 4
    adata.obs['batch'] = adata_sol.obs['batch'][adata.obs_names]
    adata.obs['cell_type'] = adata_sol.obs['cell_type'][adata.obs_names]
    print(adata.shape,adata_sol.shape)
    adata_bc = adata.obs_names
    adata_sol_bc = adata_sol.obs_names
    select = [item in adata_bc for item in adata_sol_bc]
    adata_sol = adata_sol[select, :]
    print(adata.shape, adata_sol.shape)

    adata.obsm['X_emb'] = adata.X
    nmi = get_nmi(adata)
    cell_type_asw = get_cell_type_ASW(adata)
    cc_con = get_cell_cycle_conservation(adata, adata_sol)
    traj_con = get_traj_conservation(adata, adata_sol)
    batch_asw = get_batch_ASW(adata)
    graph_score = get_graph_connectivity(adata)

    print('nmi %.4f, celltype_asw %.4f, cc_con %.4f, traj_con %.4f, batch_asw %.4f, graph_score %.4f\n' % (
    nmi, cell_type_asw, cc_con, traj_con, batch_asw, graph_score))

    print('average metric: %.4f' % np.mean(
        [round(i, 4) for i in [nmi, cell_type_asw, cc_con, traj_con, batch_asw, graph_score]]))

    return [round(i, 4) for i in [nmi, cell_type_asw, cc_con, traj_con, batch_asw, graph_score]]
