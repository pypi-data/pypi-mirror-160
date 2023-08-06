import os
import sys
import logging
import argparse
import numpy as np
import pandas as pd
import scipy.spatial
import scanpy as sc

import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.nn.functional as F
import random
from dance.utils import PairedDataset
import skorch.helper
import math

from dance.datasets.multimodality import ModalityPredictionDataset
from dance.modules.multi_modality.predict_modality.babel import BabelWrapper
from dance.utils import set_seed
import dance.utils.loss as loss_functions

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    OPTIMIZER_DICT = {
        "adam": torch.optim.Adam,
        "rmsprop": torch.optim.RMSprop,
    }
    rndseed = random.randint(0, 2147483647)
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--subtask', default='openproblems_bmmc_cite_phase2_rna')
    parser.add_argument('-device', '--device', default='cuda:3')
    parser.add_argument('-cpu', '--cpus', default = 1, type = int)
    parser.add_argument('-seed', '--rnd_seed', default = rndseed, type=int)
    parser.add_argument('-m', '--model_folder', default = './models')
    parser.add_argument("--outdir", "-o", default = './logs', help="Directory to output to")
    parser.add_argument("--lossweight", type=float, default=1., help="Relative loss weight",)
    parser.add_argument("--lr", "-l", type=float, default=0.01, help="Learning rate")
    parser.add_argument("--batchsize", "-b", type=int, default=64, help="Batch size")
    parser.add_argument("--hidden", type=int, default=64, help="Hidden dimensions")
    parser.add_argument("--earlystop", type=int, default=20, help="Early stopping after N epochs")
    parser.add_argument("--naive", "-n", action="store_true", help="Use a naive model instead of lego model",)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--max_epochs", type=int, default=500)
    args = parser.parse_args()
    args.resume = True

    torch.set_num_threads(args.cpus)
    rndseed = args.rnd_seed
    set_seed(rndseed)
    dataset = ModalityPredictionDataset(args.subtask).load_data().preprocess('feature_selection')
    device = args.device
    os.makedirs(args.model_folder, exist_ok=True)
    os.makedirs(args.outdir, exist_ok=True)

    args.outdir = os.path.abspath(args.outdir)

    if not os.path.isdir(os.path.dirname(args.outdir)):
        os.makedirs(os.path.dirname(args.outdir))

    # Specify output log file
    logger = logging.getLogger()
    fh = logging.FileHandler(f"{args.outdir}/training_{args.subtask}_{args.rnd_seed}.log", "w")
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)

    for arg in vars(args):
        logging.info(f"Parameter {arg}: {getattr(args, arg)}")

    idx = np.random.permutation(dataset.modalities[0].shape[0])
    train_idx = idx[:int(idx.shape[0]*0.85)]
    val_idx = idx[int(idx.shape[0]*0.85):]
    train_mod1 = torch.from_numpy(dataset.numpy_features(0)[train_idx]).float()
    train_mod2 = torch.from_numpy(dataset.numpy_features(1)[train_idx]).float()
    valid_mod1 = torch.from_numpy(dataset.numpy_features(0)[val_idx]).float()
    valid_mod2 = torch.from_numpy(dataset.numpy_features(1)[val_idx]).float()
    test_mod1 = torch.from_numpy(dataset.numpy_features(2)).float()
    test_mod2 = torch.from_numpy(dataset.numpy_features(3)).float()

    sc_dual_train_dataset = PairedDataset(train_mod1, train_mod2)
    sc_dual_valid_dataset = PairedDataset(valid_mod1, valid_mod2)

    model = BabelWrapper(args, dataset)
    model.fit(sc_dual_train_dataset, sc_dual_valid_dataset, args.max_epochs)
    print(model.predict(test_mod1))
    print(model.score(test_mod1, test_mod2))


    # # Instantiate and train model
    # model_class = (
    #     autoencoders.NaiveSplicedAutoEncoder
    #     if args.naive
    #     else autoencoders.AssymSplicedAutoEncoder
    # )
    #
    # spliced_net = autoencoders.BabelWrapper(
    #     module=model_class,
    #     module__hidden_dim=args.hidden,  # Based on hyperparam tuning
    #     module__input_dim1=dataset.modalities[0].shape[1],
    #     module__input_dim2=[dataset.modalities[1].shape[1]],
    #     module__final_activations1=[
    #                 autoencoders.Exp(),
    #                 autoencoders.ClippedSoftplus(),
    #             ],#nn.ReLU(),
    #     module__final_activations2=[
    #                 autoencoders.Exp(),
    #                 autoencoders.ClippedSoftplus(),
    #             ],#nn.ReLU(),
    #     module__flat_mode=True,
    #     module__seed=args.rnd_seed,
    #     lr=args.lr,  # Based on hyperparam tuning
    #     criterion=loss_functions.QuadLoss,
    #     criterion__loss1=loss_functions.NegativeBinomialLoss, #RMSELoss,
    #     criterion__loss2=loss_functions.NegativeBinomialLoss, #RMSELoss,  # handle output of encoded layer
    #     criterion__loss2_weight=1.5,#args.lossweight,  # numerically balance the two losses with different magnitudes
    #     criterion__record_history=True,
    #     optimizer=OPTIMIZER_DICT['adam'],
    #     iterator_train__shuffle=True,
    #     device=torch.device(args.device),
    #     batch_size=args.batchsize,  # Based on  hyperparam tuning
    #     max_epochs=500,
    #     callbacks=[
    #         skorch.callbacks.EarlyStopping(patience=args.earlystop),
    #         skorch.callbacks.LRScheduler(
    #             policy=torch.optim.lr_scheduler.ReduceLROnPlateau,
    #             **autoencoders.REDUCE_LR_ON_PLATEAU_PARAMS,
    #         ),
    #         skorch.callbacks.GradientNormClipping(gradient_clip_value=5),
    #         skorch.callbacks.Checkpoint(
    #             dirname=args.outdir, fn_prefix="net_", monitor="valid_loss_best",
    #         ),
    #     ],
    #     train_split=skorch.helper.predefined_split(sc_dual_valid_dataset),
    #     iterator_train__num_workers=8,
    #     iterator_valid__num_workers=8,
    # )
    #
    # if args.resume:
    #     # Load in the warm start parameters
    #     try:
    #         spliced_net.initialize()
    #         cp = skorch.callbacks.Checkpoint(dirname=args.outdir, fn_prefix="net_", monitor="valid_loss_best", )
    #         spliced_net.load_params(checkpoint=cp)
    #
    #         # Upon successfully finding correct hiden size, break out of loop
    #         print(f"Loaded model with hidden size {args.hidden}")
    #         spliced_net = spliced_net
    #     except RuntimeError as e:
    #         print(f"Failed to load with hidden size {args.hidden}")
    #     spliced_net.module_.eval()
    # else:
    #     spliced_net.fit(sc_dual_train_dataset, y=None)
    #     spliced_net.module_.eval()
    #
    # sc_rna_atac_train_preds = spliced_net.translate_1_to_2(sc_dual_train_dataset)
    # sc_rna_atac_valid_preds = spliced_net.translate_1_to_2(sc_dual_valid_dataset)
    # sc_rna_atac_test_preds = spliced_net.translate_1_to_2(sc_dual_test_dataset)
    #
    # def evaluate(pred, label):
    #     mse = nn.MSELoss()
    #     return math.sqrt(mse(torch.from_numpy(pred.todense()), label))
    #
    # print('train:', evaluate(sc_rna_atac_train_preds, train_mod2))
    # print('valid:', evaluate(sc_rna_atac_valid_preds, valid_mod2))
    # print('test:', evaluate(sc_rna_atac_test_preds, test_mod2))


#######################
##  Remake
#######################

#
# model = model_class(hidden_dim=args.hidden,
#             input_dim1=dataset.modalities[0].shape[1],
#             input_dim2=[dataset.modalities[1].shape[1]],
#             final_activations1=nn.ReLU(),
#             final_activations2=nn.ReLU(),
#             flat_mode=True,
#             seed=args.rnd_seed,
#             ).to(device)
#
# def train(
#         criterion=loss_functions.QuadLoss(loss1 = loss_functions.RMSELoss, loss2 = loss_functions.RMSELoss,
#                                           loss2_weight=args.lossweight),
#         max_epochs=500,
#         callbacks=[
#                 skorch.callbacks.EarlyStopping(patience=args.earlystop),
#                 skorch.callbacks.GradientNormClipping(gradient_clip_value=5),
#             ],
#         train_split=sc_dual_valid_dataset):
#
#     device = args.device
#
#     optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
#     train_loader = DataLoader(dataset=sc_dual_train_dataset,
#                               batch_size=args.batchsize,
#                               shuffle=True,
#                               num_workers=1, )
#     valid_loader = DataLoader(dataset=sc_dual_valid_dataset,
#                               batch_size=len(sc_dual_valid_dataset),
#                               shuffle=False,
#                               num_workers=1, )
#
#     for i in range(max_epochs):
#         model.train()
#         total_loss = 0
#         for idx, data in enumerate(train_loader):
#             logits = model(data[0].to(device))
#             loss = criterion(logits, data[1].to(device))
#             total_loss += loss.item()
#
#             optimizer.zero_grad()
#             loss.backward()
#             optimizer.step()
#
#         print('training (sum of 4 losses):', total_loss/len(train_loader))
#         print('validation (prediction loss):', evaluate(valid_loader))
#         test()
#
#
# def evaluate(valid_loader):
#     mse = nn.MSELoss()
#     model.eval()
#
#     with torch.no_grad():
#         loss = 0
#         for _, data in enumerate(valid_loader):
#             logits = model(data[0].to(device))
#             loss += mse(logits[1][0], data[1][:, -logits[1][0].shape[1]:].to(device)).item()
#         return math.sqrt(loss/len(valid_loader))
#
# def test():
#     mse = nn.MSELoss()
#     model.eval()
#
#     with torch.no_grad():
#         emb = model.model12[0](test_mod1.to(device))
#         pred = model.model12[1](emb)[0]
#         print(math.sqrt(mse(pred, test_mod2.to(device))))
