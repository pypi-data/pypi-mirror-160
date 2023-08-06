"""
Main functionality for starting training.
This code is based on https://github.com/NVlabs/MUNIT.
"""
import torch
import argparse
import random
from sklearn import preprocessing
import yaml

try:
    from itertools import izip as zip
except ImportError:
    pass
import os
import shutil
from dance.datasets.multimodality import ModalityMatchingDataset
from dance.modules.multi_modality.match_modality.cmae import CMAE
from dance.utils import set_seed

def prepare_sub_folder(output_directory):
    image_directory = os.path.join(output_directory, 'images')
    if not os.path.exists(image_directory):
        print("Creating directory: {}".format(image_directory))
        os.makedirs(image_directory)
    checkpoint_directory = os.path.join(output_directory, 'checkpoints')
    if not os.path.exists(checkpoint_directory):
        print("Creating directory: {}".format(checkpoint_directory))
        os.makedirs(checkpoint_directory)
    return checkpoint_directory, image_directory

def get_config(config):
    # Note need to have pip install pyyaml==5.4.1
    with open(config, 'r') as stream:
        return yaml.load(stream, Loader=yaml.Loader)

if __name__ == '__main__':
    rndseed = random.randint(0, 2147483647)
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default = './match_modality/cross_modal_supervised.yaml', help='Path to the config file.')
    parser.add_argument('--output_path', type=str, default='./match_modality/output', help="outputs path")
    parser.add_argument('-d', '--data_folder', default = './data/modality_matching')
    parser.add_argument("--resume", action="store_true")
    parser.add_argument('-t', '--subtask', default='openproblems_bmmc_cite_phase2_rna')
    parser.add_argument('-device', '--device', default='cuda:3')
    parser.add_argument('-cpu', '--cpus', default = 1, type = int)
    parser.add_argument('-seed', '--rnd_seed', default = rndseed, type=int)
    parser.add_argument('-pk', '--pickle_suffix', default='_lsi_input_pca_count.pkl')

    opts = parser.parse_args()

    torch.set_num_threads(opts.cpus)
    rndseed = opts.rnd_seed
    set_seed(rndseed)
    pkl_path = opts.subtask + opts.pickle_suffix
    dataset = ModalityMatchingDataset(opts.subtask, data_dir=opts.data_folder).load_data().load_sol().preprocess(kind='feature_selection')
    device = opts.device

    # Load experiment setting
    config = get_config(opts.config)

    # Setup logger and output folders
    model_name = os.path.splitext(os.path.basename(opts.config))[0]
    output_directory = os.path.join(opts.output_path + "/outputs", model_name)
    checkpoint_directory, image_directory = prepare_sub_folder(output_directory)
    shutil.copy(opts.config, os.path.join(output_directory, 'config.yaml'))  # copy config file to output folder

    le = preprocessing.LabelEncoder()
    train_batch = dataset.modalities[0].obs['batch']
    batch = le.fit_transform(train_batch)
    train_batch = torch.from_numpy(batch).long().to(device)
    train_mod1 = torch.from_numpy(dataset.numpy_features(0)).float().to(device)
    train_mod2 = torch.from_numpy(dataset.numpy_features(1)).float().to(device)
    test_mod1 = torch.from_numpy(dataset.numpy_features(2)).float().to(device)
    test_mod2 = torch.from_numpy(dataset.numpy_features(3)).float().to(device)
    z_test = torch.from_numpy(dataset.test_sol.X.toarray())

    config['input_dim_a'] = dataset.modalities[0].shape[1]
    config['input_dim_b'] = dataset.modalities[1].shape[1]
    config['resume'] = opts.resume
    config['num_of_classes'] = max(batch) + 1

    model = CMAE(config)
    model.to(device)

    model.fit(train_mod1, train_mod2, checkpoint_directory=checkpoint_directory)
    print(model.predict(test_mod1, test_mod2))
    print(model.score(test_mod1, test_mod2, z_test))
