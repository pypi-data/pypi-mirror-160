from torch.utils.data import Dataset
import torchvision.transforms as transforms
from preprocess import Slices
import numpy as np


class DatasetTwoSlices(Dataset):
    """
    Slices Dataset : cropped slices through the center of the synapses
    """

    def __init__(self,
                 imgs1, imgs2, labels=None,
                 transform1=False,
                 transform2=False):
        """
        Args:
        """
        self.n_synapses = len(imgs1)
        self.imgs1 = imgs1
        self.imgs2 = imgs2
        self.labels = labels

        self.transform1 = transform1
        self.transform2 = transform2

    def __getitem__(self, index):
        # This method should return only 1 sample and label
        # (according to "index"), not the whole dataset
        if self.labels is not None:
            label = self.labels[index]
        img1 = self.imgs1[index]
        img2 = self.imgs2[index]

        if self.transform1:
            img1 = self.transform1(img1)
        if self.transform2:
            img2 = self.transform2(img2)
        if self.labels is not None:
            return img1, img2, label
        else:
            return img1, img2

    def __len__(self):
        return self.n_synapses

    def __repr__(self):
        info_str = f"""TwoSlices Dataset contains {self.n_synapses} pairs of images"""
        return info_str


class DatasetTwoSlicesProbMap(Dataset):
    """
    Slices Dataset : cropped slices through the center of the synapses
    """

    def __init__(self, img, rois):
        """
        Args:
        """
        self.img = img
        self.mean = np.mean(self.img)
        self.std = np.std(self.img)

        self.roi = rois
        self.centroids = self.get_centroids(rois)
        self.slicer_yx = Slices([1, 15, 15])
        self.slicer_zy = Slices([15, 15, 1])

    @staticmethod
    def get_centroids(rois):
        """
        creates a centroid for every pixel in the rois
        """

        def get_pixels_as_centroids(roi):
            """
            turns pixel into [z,y,x]
            roi: region for which to get the pixels
            """
            z, y, x = np.meshgrid(np.arange(roi['zmin'], roi['zmax']),
                                  np.arange(roi['ymin'], roi['ymax']),
                                  np.arange(roi['xmin'], roi['xmax']))
            return np.c_[z.flatten(), y.flatten(), x.flatten()]

        centroids = np.empty((1, 3))
        for roi in rois:
            centroids = np.append(centroids, get_pixels_as_centroids(roi), axis=0)

        return centroids.astype(int)

    def standardize(self, data):
        """
        Standardize data using z score per group. Volume or slices.
        """
        data = (data - self.mean) / self.std
        return data

    def __getitem__(self, index):
        # This method should return only 1 sample and label
        # (according to "index"), not the whole dataset
        img1 = self.slicer_yx.crop(self.centroids[index][None, :], self.img)
        img2 = self.slicer_zy.crop(self.centroids[index][None, :], self.img)

        img1 = self.standardize(img1)
        img2 = self.standardize(img2)

        img1 = transforms.ToTensor()(img1)
        img2 = transforms.ToTensor()(img2)

        return img1, img2

    def __len__(self):
        return len(self.centroids)

    def __repr__(self):
        info_str = f"""TwoSlices Dataset contains {len(self.centroids)} pairs of images"""
        return info_str
