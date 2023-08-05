import os
from copy import copy
from typing import Union

import numpy as np
import pandas as pd
from sklearn import model_selection
from torcheeg.datasets.module.base_dataset import BaseDataset


def train_test_split_cross_trial(
        dataset: BaseDataset,
        test_size: float = 0.2,
        shuffle: bool = False,
        random_state: Union[float, None] = None,
        split_path='./dataset/train_test_split_cross_trial'):
    r'''
    A tool function for cross-validations, to divide the training set and the test set. It is suitable for experiments with large dataset volume and no need to use k-fold cross-validations. Parts of trials are sampled according to a certain proportion as the test dataset, and samples from other trials are used as training samples. In most literatures, 20% of the data are sampled for testing.

    :obj:`train_test_split_cross_trial` devides training set and the test set at the dimension of each trial. For example, when :obj:`test_size=0.2`, the first 80% of samples of each trial are used for training, and the last 20% of samples are used for testing. It is more consistent with real applications and can test the generalization of the model to a certain extent.

    .. image:: _static/train_test_split_cross_trial.png
        :height: 120px
        :alt: The schematic diagram of train_test_split_cross_trial
        :align: center

    |

    .. code-block:: python

        dataset = DEAPDataset(io_path=f'./deap',
                              root_path='./data_preprocessed_python',
                              online_transform=transforms.Compose([
                                  transforms.To2d(),
                                  transforms.ToTensor()
                              ]),
                              label_transform=transforms.Compose([
                                  transforms.Select(['valence', 'arousal']),
                                  transforms.Binary(5.0),
                                  transforms.BinariesToCategory()
                              ]))

        train_dataset, test_dataset = train_test_split_cross_trial(dataset=dataset, split_path='./split')

        train_loader = DataLoader(train_dataset)
        test_loader = DataLoader(test_dataset)
        ...

    Args:
        dataset (BaseDataset): Dataset to be divided.
        test_size (int):  If float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in the test split. If int, represents the absolute number of test samples. (default: :obj:`0.2`)
        shuffle (bool): Whether to shuffle the data before splitting into batches. Note that the samples within each split will not be shuffled. (default: :obj:`False`)
        random_state (int, optional): When shuffle is :obj:`True`, :obj:`random_state` affects the ordering of the indices, which controls the randomness of each fold. Otherwise, this parameter has no effect. (default: :obj:`None`)
        split_path (str): The path to data partition information. If the path exists, read the existing partition from the path. If the path does not exist, the current division method will be saved for next use. (default: :obj:`./split/k_fold_dataset`)
    '''
    if not os.path.exists(split_path):
        os.makedirs(split_path)
        info = dataset.info
        subjects = list(set(info['subject_id']))

        train_info = None
        test_info = None

        for subject in subjects:
            subject_info = info[info['subject_id'] == subject]
            trial_ids = list(set(subject_info['trial_id']))

            train_trial_ids, test_trial_ids = model_selection.train_test_split(
                trial_ids,
                test_size=test_size,
                shuffle=shuffle,
                random_state=random_state)

            if len(train_trial_ids) == 0 or len(test_trial_ids) == 0:
                raise ValueError(
                    f'The number of training or testing trials for subject {subject} is zero.'
                )

            subject_train_info = []
            for train_trial_id in train_trial_ids:
                subject_train_info.append(
                    subject_info[subject_info['trial_id'] == train_trial_id])
            subject_train_info = pd.concat(subject_train_info,
                                           ignore_index=True)

            subject_test_info = []
            for test_trial_id in test_trial_ids:
                subject_test_info.append(
                    subject_info[subject_info['trial_id'] == test_trial_id])
            subject_test_info = pd.concat(subject_test_info, ignore_index=True)

            if train_info is None and test_info is None:
                train_info = subject_train_info
                test_info = subject_test_info
            else:
                train_info = train_info.append(subject_train_info)
                test_info = test_info.append(subject_test_info)

        train_info.to_csv(os.path.join(split_path, 'train.csv'), index=False)
        test_info.to_csv(os.path.join(split_path, 'test.csv'), index=False)

    train_info = pd.read_csv(os.path.join(split_path, 'train.csv'))
    test_info = pd.read_csv(os.path.join(split_path, 'test.csv'))

    train_dataset = copy(dataset)
    train_dataset.info = train_info

    test_dataset = copy(dataset)
    test_dataset.info = test_info

    return train_dataset, test_dataset