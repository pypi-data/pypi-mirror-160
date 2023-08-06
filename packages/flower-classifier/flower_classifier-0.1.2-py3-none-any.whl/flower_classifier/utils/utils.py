import pickle

import torch


def dump_pickle(address, file):
    with open(address, 'wb') as f:
        pickle.dump(file, f)


def load_pickle(address):
    with open(address, 'rb') as f:
        data = pickle.load(f)
    return data


def get_device():
    return torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def get_num_params(model):
    return sum([p.numel() for p in model.parameters()])
