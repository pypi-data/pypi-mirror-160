# PyTorch libraries
import torch
from torch import nn
import numpy as np
from tqdm import tqdm

def conv2d_module(in_channels, out_channels, kernel_size, stride=1, padding=0, batch_norm=True):
    """
    define a CONV2D => BN => RELU pattern
    batch_norm : weather or not to apply batch norm
    """
    if batch_norm:
        conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride, padding=padding),
            nn.BatchNorm2d(out_channels),
            nn.ReLU())
    else:
        conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride, padding=padding),
            nn.ReLU())
    # return the block
    return conv


class TwoBranchConv2d(nn.Module):
    """
    Model with two branches of 2d convolution along them
    https://stackoverflow.com/questions/66786787/pytorch-multiple-branches-of-a-model
    """

    def __init__(self, do_batch_norm=False):
        super(TwoBranchConv2d, self).__init__()

        self.cnns = nn.ModuleList([self.cnn_branch(do_batch_norm=do_batch_norm),
                                   self.cnn_branch(do_batch_norm=do_batch_norm)])
        self.fc = nn.Sequential(
            nn.Linear(16, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
            # skipping sigmoid layer because during the training wea are using nn.BCEWithLogitsLoss ,
            # which combines nn.Sigmoid and nn.BCELoss
        )

    @staticmethod
    def cnn_branch(do_batch_norm=False):
        conv = nn.Sequential(
            conv2d_module(1, 4, 3, stride=1, padding=0, batch_norm=do_batch_norm),
            conv2d_module(4, 4, 3, stride=1, padding=0, batch_norm=do_batch_norm),
            nn.MaxPool2d(2),
            conv2d_module(4, 8, 3, stride=1, padding=0, batch_norm=do_batch_norm),
            conv2d_module(8, 8, 3, stride=1, padding=0, batch_norm=do_batch_norm)
        )
        return conv

    def forward(self, x, y):
        x = self.cnns[0](x)
        y = self.cnns[1](y)

        combined = torch.cat((x.view(x.size(0), -1),
                              y.view(y.size(0), -1)), dim=1)

        # before squeeze it is (Batch x 1) , but need to match labels (Batch)
        z = torch.squeeze(self.fc(combined))
        return z

