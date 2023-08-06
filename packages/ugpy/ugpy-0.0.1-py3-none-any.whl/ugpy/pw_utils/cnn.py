import pandas as pd
from pathlib import Path
import numpy as np
import tifffile as tif
import sys
import copy

from tqdm import tqdm

project_path = 'D:/Code/repos/psd95_segmentation'
sys.path.insert(1, project_path)
import src.features.synapse_features as ft

# imports for CnnModel
import tensorflow.keras.callbacks as callback
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, BatchNormalization
from sklearn.model_selection import train_test_split
from src.features.synapse_features import prepare_output
from synspy.analyze.util import dump_segment_info_to_csv

from tensorflow.keras.models import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import concatenate
import tensorflow.keras.backend as Kb
from tensorflow.keras.callbacks import ModelCheckpoint
import datetime
import matplotlib.pyplot as plt

import sys
import platform

if platform.system() == 'Windows':
    project_path = 'D:/Code/repos/pwreg'
else:
    project_path = '/mnt/d/Code/repos/pwreg'

sys.path.insert(1, f'{project_path}/pwreg')


class CnnPredictor:
    """
    A Class to use the network for prediction. These are two networks togehter: YX and YZ .
    """

    def __init__(self):
        self.model = self._2_2D_CNNs()
        self.weights = ''
        self.train_data = []
        self.train_history = []
        self.training_dict = {}

    def __str__(self):
        return "Two 2D CNNs looking at XY and ZY 15x15 pixel image centered around the synapse"

    def _2_2D_CNNs(self):
        """
        following
        https://stackoverflow.com/questions/57729485/model-with-two-branches-converging-to-one-zero-gradients-and-constant-output
        """

        def _simple_CNN(tag):
            """
            tag (string): cnn branch describtion
            """
            chan_dim = -1

            cnn_input = Input(shape=(15, 15, 1))
            cnn = Conv2D(4, kernel_size=3, activation='relu', input_shape=(15, 15, 1), name=f'{tag}_conv_1')(cnn_input)
            cnn = BatchNormalization(axis=chan_dim)(cnn)
            cnn = Conv2D(4, kernel_size=3, activation='relu', name=f'{tag}_conv_2')(cnn)
            cnn = BatchNormalization(axis=chan_dim)(cnn)
            cnn = MaxPooling2D(pool_size=2)(cnn)
            cnn = Conv2D(8, kernel_size=3, activation='relu', name=f'{tag}_conv_3')(cnn)
            cnn = BatchNormalization(axis=chan_dim)(cnn)
            cnn = Conv2D(8, kernel_size=3, activation='relu', name=f'{tag}_conv_4')(cnn)
            cnn = BatchNormalization(axis=chan_dim)(cnn)
            cnn = Flatten()(cnn)
            cnn = Model(inputs=cnn_input, outputs=cnn)
            return cnn

        # the first branch operates on the first input
        x = _simple_CNN("yx")
        # the second branch opreates on the second input
        y = _simple_CNN("zy")

        # combine the output of the two branches
        combined = concatenate([x.output, y.output])
        # prediction on the combined outputs
        z = Dense(64, activation='relu', name='dense_1')(combined)
        z = Dense(32, activation='relu', name='dense_2')(z)
        z = Dense(1, activation='sigmoid', name='final_out')(z)
        # our model will accept the inputs of the two branches and
        # then output a single value
        model = Model(inputs=[x.input, y.input], outputs=z)

        return model

    def load_weights(self, weights):
        self.weights = weights
        self.model.load_weights(self.weights)

    def compile(self):
        # functions to train by improving f1 score
        THRESHOLD = 0.5

        def precision(y_true, y_pred, threshold_shift=0.5 - THRESHOLD):
            # just in case
            y_pred = Kb.clip(y_pred, 0, 1)

            # shifting the prediction threshold from .5 if needed
            y_pred_bin = Kb.round(y_pred + threshold_shift)

            tp = Kb.sum(Kb.round(y_true * y_pred_bin)) + Kb.epsilon()
            fp = Kb.sum(Kb.round(Kb.clip(y_pred_bin - y_true, 0, 1)))

            precision = tp / (tp + fp)
            return precision

        def recall(y_true, y_pred, threshold_shift=0.5 - THRESHOLD):
            # just in case
            y_pred = Kb.clip(y_pred, 0, 1)

            # shifting the prediction threshold from .5 if needed
            y_pred_bin = Kb.round(y_pred + threshold_shift)

            tp = Kb.sum(Kb.round(y_true * y_pred_bin)) + Kb.epsilon()
            fn = Kb.sum(Kb.round(Kb.clip(y_true - y_pred_bin, 0, 1)))

            recall = tp / (tp + fn)
            return recall

        def fbeta(y_true, y_pred, threshold_shift=0.5 - THRESHOLD):
            beta = 2

            # just in case
            y_pred = Kb.clip(y_pred, 0, 1)

            # shifting the prediction threshold from .5 if needed
            y_pred_bin = Kb.round(y_pred + threshold_shift)

            tp = Kb.sum(Kb.round(y_true * y_pred_bin)) + Kb.epsilon()
            fp = Kb.sum(Kb.round(Kb.clip(y_pred_bin - y_true, 0, 1)))
            fn = Kb.sum(Kb.round(Kb.clip(y_true - y_pred, 0, 1)))

            precision = tp / (tp + fp)
            recall = tp / (tp + fn)

            beta_squared = beta ** 2
            return (beta_squared + 1) * (precision * recall) / (beta_squared * precision + recall)

        self.model.compile(loss='binary_crossentropy', optimizer='adamax', metrics=[fbeta, precision, recall])

    @staticmethod
    def crop_slices(centroids, img):
        """
        centroids in ZYX order in pixels
        """
        xy_slices = np.zeros((len(centroids), 15, 15))
        yz_slices = np.zeros((len(centroids), 15, 15))

        for i, centroid in enumerate(centroids):
            start = centroid - 7
            end = centroid + 7 + 1
            xy_slices[i, :] = img.img[centroid[0], start[1]:end[1], start[2]:end[2]]
            yz_slices[i, :] = img.img[start[0]:end[0], start[1]:end[1], centroid[2]]

        # normalize by mean
        xy_slices = xy_slices - np.mean(xy_slices, axis=(1, 2))[:, None, None]
        yz_slices = yz_slices - np.mean(yz_slices, axis=(1, 2))[:, None, None]

        xy_slices = np.expand_dims(xy_slices, axis=3)
        yz_slices = np.expand_dims(yz_slices, axis=3)

        test_pairs = [xy_slices, yz_slices]
        return test_pairs

    def predict(self, centroids, img):
        test_pairs = self.crop_slices(centroids, img)
        prob = self.model.predict(test_pairs, batch_size=15000)
        return prob

    def get_probability_map(self, rois, img):
        """
        rois : in how many chunks to break the image when processing, dict
        """

        def get_pixels_as_centroids(roi):
            """
            roi: region for which to get the pixels
            """
            z, y, x = np.meshgrid(np.arange(roi['zmin'], roi['zmax']),
                                  np.arange(roi['ymin'], roi['ymax']),
                                  np.arange(roi['xmin'], roi['xmax']))
            return np.c_[z.flatten(), y.flatten(), x.flatten()]

        SCALE = 10000
        prob_map = np.zeros(img.shape)
        for roi in tqdm(rois):
            pixels = get_pixels_as_centroids(roi)
            predictions = self.predict(pixels, img)
            for i, pixel in enumerate(pixels):
                prob_map[pixel[0], pixel[1], pixel[2]] = int(predictions[i] * SCALE)

        return prob_map


class Box:
    """
    A Bounding Box.
    """

    def __init__(self, center, score, box_size):
        """
        center : coordinates in zyx order
        param box_size: can be int or 3x1 numpy array representing 3 voxel sides.needs to be odd.
        """
        self.center = np.array(center)
        self.size = np.array(box_size)
        self.volume = self.size[0] * self.size[1] * self.size[2]

        self.zyx = self.get_zyx()
        self.vertices = self.get_vertices()

        self.score = score

    def get_zyx(self):
        """
        Returns the zyx coordinates of the top right and bottom left corners of the box
        """
        half_size = np.floor(self.size / 2)
        zyx_min = self.center - half_size
        zyx_max = self.center + half_size

        return {'xmin': zyx_min[2], 'xmax': zyx_max[2],
                'ymin': zyx_min[1], 'ymax': zyx_max[1],
                'zmin': zyx_min[0], 'zmax': zyx_max[0]}

    def get_vertices(self):
        """
        Returns a set of XY vertices for each z slice.
        """
        vertices = []

        for z in np.arange(self.zyx['zmin'], self.zyx['zmax'] + 1):
            xy_corners = [[z, self.zyx['ymin'], self.zyx['xmin']],
                          [z, self.zyx['ymin'], self.zyx['xmax']],
                          [z, self.zyx['ymax'], self.zyx['xmax']],
                          [z, self.zyx['ymax'], self.zyx['xmin']]]
            vertices.append(xy_corners)

        return vertices

    @staticmethod
    def iou(box1, box2):
        # determine the (x, y, z)-coordinates of the intersection rectangle
        # x
        xmin = max(box1.zyx['xmin'], box2.zyx['xmin'])
        xmax = min(box1.zyx['xmax'], box2.zyx['xmax'])
        # y
        ymin = max(box1.zyx['ymin'], box2.zyx['ymin'])
        ymax = min(box1.zyx['ymax'], box2.zyx['ymax'])
        # z
        zmin = max(box1.zyx['zmin'], box2.zyx['zmin'])
        zmax = min(box1.zyx['zmax'], box2.zyx['zmax'])

        # compute the area of intersection rectangle
        inter_volume = max(0, xmax - xmin + 1) * max(0, ymax - ymin + 1) * max(0, zmax - zmin + 1)
        # iou
        iou = inter_volume / float(box1.volume + box2.volume - inter_volume)

        return iou


class Boxes:
    """
    Deals with the Bounding Boxes.
    """

    def __init__(self, box_list, is_sorted=False):
        """
        prob_img : probability map, as Image
        """
        self.boxes = box_list
        self.is_sorted = is_sorted

    @classmethod
    def make_boxes(cls, prob_img, prb_thr, box_size):
        """
        Builds a list of boxes.
        """
        boxes = []

        zmax, ymax, xmax = prob_img.shape

        # yes, this loop is not beautiful and it's slow,
        # but it's easy to track for a prototype :)
        for i in np.arange(zmax):
            for j in np.arange(ymax):
                for k in np.arange(xmax):
                    if prob_img.img[i, j, k] > prb_thr:
                        boxes.append(Box([i, j, k], prob_img.img[i, j, k], box_size))

        return cls(boxes)

    def sort_boxes(self):
        """
        Sort boxes by score.
        """
        self.is_sorted = True
        self.boxes = sorted(self.boxes, key=lambda x: x.score, reverse=True)

    def nms(self, nms_threshold):
        """
        Non-maximum Suppression : remove duplicate boxes.
        returns list of boxes.
        """

        if not self.is_sorted:
            self.sort_boxes()

        boxes = copy.deepcopy(self.boxes)
        good_boxes = []

        while len(boxes) > 0:

            good_box = boxes.pop(0)
            good_boxes.append(good_box)

            keep_boxes = []
            for box in boxes:
                iou = Box.iou(good_box, box)
                if iou < nms_threshold:
                    keep_boxes.append(box)

            boxes = keep_boxes

        return Boxes(good_boxes, is_sorted=True)

    def get_vertices(self):
        """
        Concatenates all the vertices.
        """
        vertices = []

        for box in self.boxes:
            vertices.extend(box.vertices)

        return vertices
