# -*- coding: utf-8 -*-
from abc import abstractmethod

import numpy as np
import torch

from logging import getLogger
import os
import random

from accelbrainbase.iteratable_data import IteratableData


class DatasetIterator(IteratableData):
    '''
    Iterator that draws from image files and generates `mxnet.ndarray` of unlabeled samples.
    '''

    __label_key = "labels"

    def __init__(
        self, 
        reserved_model,
        train_dataset,
        test_dataset,
        epochs=300,
        batch_size=20,
    ):
        '''
        Init.

        Args:
            image_extractor:                is-a `ImageExtractor`.
            dir_list:                       `list` of directories that store your image files in training.
                                            This class will not scan the directories recursively and consider that
                                            all image file will be sorted by any rule in relation to your sequencial modeling.

            test_dir_list:                  `list` of directories that store your image files in test.
                                            If `None`, this value will be equivalent to `dir_list`.
                                            This class will not scan the directories recursively and consider that
                                            all image file will be sorted by any rule in relation to your sequencial modeling.

            epochs:                         `int` of epochs of Mini-batch.
            batch_size:                     `int` of batch size of Mini-batch.

        '''
        if isinstance(train_dataset, torch.utils.data.Dataset) is False:
            raise TypeError()
        if isinstance(test_dataset, torch.utils.data.Dataset) is False:
            raise TypeError()

        logger = getLogger("accelbrainbase")
        self.__logger = logger

        dataset_size = len(train_dataset)
        iter_n = int(epochs * max(dataset_size / batch_size, 1))

        forward_args_tuple = reserved_model.forward.__code__.co_varnames[
            :reserved_model.forward.__code__.co_argcount
        ]
        forward_args_list = [v for v in forward_args_tuple if v != "self"]
        if forward_args_list.count(self.__label_key) == 0:
            warnings.warn("`" + str(self.__label_key) + "` is not an argument in `reserved_model.forward`. This class was designed on the assumption that the `reserved_model` that calculate losses in `forward` method.")

        self.forward_args_list = forward_args_list
        self.train_dataset = train_dataset
        self.test_dataset = test_dataset
        self.iter_n = iter_n
        self.epochs = epochs
        self.batch_size = batch_size

    def convert_dataset_item_into_tuple(self, batch_dict):
        batch_list = [batch_dict[args] for args in self.forward_args_list]
        return tuple(batch_list)

    def generate_learned_samples(self):
        '''
        Draw and generate data.

        Returns:
            `Tuple` data. The shape is ...
            - `mxnet.ndarray` of observed data points in training.
            - `mxnet.ndarray` of supervised data in training.
            - `mxnet.ndarray` of observed data points in test.
            - `mxnet.ndarray` of supervised data in test.
        '''
        for _ in range(self.iter_n):
            training_batch_arr, test_batch_arr = None, None
            training_label_arr, test_label_arr = None, None
            training_batch_dict, test_batch_dict = {}, {}
            for batch_size in range(self.batch_size):
                train_i = np.random.randint(low=0, high=len(self.train_dataset))
                test_i = np.random.randint(low=0, high=len(self.test_dataset))

                training_data_dict = self.train_dataset[train_i]
                test_data_dict = self.test_dataset[test_i]
                
                if len(training_batch_dict) == 0:
                    for key, val in training_data_dict.items():
                        training_batch_dict.setdefault(
                            key, 
                            torch.unsqueeze(val, dim=0)
                        )
                else:
                    for key, val in training_data_dict.items():
                        training_batch_dict[key] = torch.cat(
                            (
                                training_batch_dict[key],
                                torch.unsqueeze(val, dim=0)
                            ),
                            dim=0
                        )

                if len(test_batch_dict) == 0:
                    for key, val in test_data_dict.items():
                        test_batch_dict.setdefault(
                            key, 
                            torch.unsqueeze(val, dim=0)
                        )
                else:
                    for key, val in test_data_dict.items():
                        test_batch_dict[key] = torch.cat(
                            (
                                test_batch_dict[key],
                                torch.unsqueeze(val, dim=0)
                            ),
                            dim=0
                        )

            training_batch_tuple = self.convert_dataset_item_into_tuple(
                training_batch_dict
            )
            test_batch_tuple = self.convert_dataset_item_into_tuple(
                test_batch_dict
            )
            yield training_batch_tuple, test_batch_tuple

    def generate_inferenced_samples(self):
        '''
        Draw and generate data.
        The targets will be drawn from all image file sorted in ascending order by file name.

        Returns:
            `Tuple` data. The shape is ...
            - `None`.
            - `None`.
            - `mxnet.ndarray` of observed data points in test.
            - file path.
        '''
        for test_i in range(len(self.test_dataset)):
            test_batch_arr = None
            test_label_arr = None
            test_batch_dict = {}
            for batch_size in range(self.batch_size):
                test_data_dict = self.test_dataset[test_i]

                if len(test_batch_dict) == 0:
                    for key, val in test_data_dict.items():
                        test_batch_dict.setdefault(
                            key, 
                            torch.unsqueeze(val, dim=0)
                        )
                else:
                    for key, val in test_data_dict.items():
                        test_batch_dict[key] = torch.cat(
                            (
                                test_batch_dict[key],
                                torch.unsqueeze(val, dim=0)
                            ),
                            dim=0
                        )

            test_batch_tuple = self.convert_dataset_item_into_tuple(
                test_batch_dict
            )
            yield test_batch_tuple
