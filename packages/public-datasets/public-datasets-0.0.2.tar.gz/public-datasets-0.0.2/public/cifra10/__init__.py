# -*- coding: utf-8 -*-
# Copyright IRT Antoine de Saint Exupéry et Université Paul Sabatier Toulouse III - All
# rights reserved. DEEL is a research program operated by IVADO, IRT Saint Exupéry,
# CRIAQ and ANITI - https://www.deel.ai/
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -*- encoding: utf-8 -*-
import os
import pathlib
import typing

import numpy as np
from deel.datasets.providers.http_providers import HttpMultiFilesProvider
from PIL import Image
from tqdm import tqdm


class Cifar10Provider(HttpMultiFilesProvider):
    # list of labels in CIFRA-10 dataset
    _cifar10_labels = [
        "airplane",
        "automobile",
        "bird",
        "cat",
        "deer",
        "dog",
        "frog",
        "horse",
        "ship",
        "truck",
    ]

    def __init__(
        self,
        root_folder: os.PathLike,
        remote_url_list: typing.List[str],
        version: str = "1.0.0",
    ):
        """
        Args:
            root_folder: Root folder to look-up datasets.
            remote_url: Remote URL of the file to serve.
            name: Name of the dataset corresponding to the remote file.
            version: Version of the dataset corresponding to the remote file.
            authenticator: Authenticator to use.
        """
        super().__init__(root_folder, remote_url_list, "cifra10")

    def _unpickle(self, file: pathlib.Path):
        """
        This method allows to extract images from CIFRA-10 raw dataset files
        """
        import pickle

        with open(file, "rb") as fo:
            dict = pickle.load(fo, encoding="bytes")
            return dict

    def _convert_cifar10_dataset(
        self,
        data_type: str,
        cifar10_dir: pathlib.Path,
        images: np.ndarray,
        labels: typing.List,
    ):
        """
        This method allows to extract CIFRA-10 dataset images and save
        them in their label directory:  cifar10/label/img

        Args:
            data_type: train or test or other
            cifar10_dir: local parent directory: cifar-10-batches-py
            images: list of images
            labels: list of labels
        """
        images_iterator = iter(images)
        numImages = len(images)
        label_iter = iter(labels)

        images_iterator = iter(images)
        with tqdm(
            total=numImages,
            desc="convert CIFAR-10 {} images".format(data_type),
        ) as pbar:
            for image in range(0, numImages):
                im = next(images_iterator)
                lab = next(label_iter)
                im = Image.fromarray(im)
                dest = cifar10_dir.joinpath(
                    data_type,
                    self._cifar10_labels[lab],
                    "{}_{}.bmp".format(data_type, image),
                )
                os.makedirs(dest.parent, exist_ok=True)
                im.save(dest, "bmp")
                pbar.update(1)
        pbar.close()

    def _process_cifra10_dataset(self, local_path: pathlib.Path):
        """
        This method process and save CIFAR-10 dataset
        """
        cifar10_dir = local_path.joinpath("cifar-10-batches-py")
        if cifar10_dir.exists():
            for f in cifar10_dir.glob("data_batch_*"):
                print("=================> {}".format(f))
                dataset = self._unpickle(f)
                labels = dataset[b"labels"]
                images = np.reshape(
                    dataset[b"data"], (len(dataset[b"data"]), 3, 32, 32)
                ).transpose(0, 2, 3, 1)
                self._convert_cifar10_dataset("data", cifar10_dir, images, labels)
                os.remove(f)
            for f in cifar10_dir.glob("test_batch*"):
                print("=================> {}".format(f))
                dataset = self._unpickle(f)
                labels = dataset[b"labels"]
                images = np.reshape(
                    dataset[b"data"], (len(dataset[b"data"]), 3, 32, 32)
                ).transpose(0, 2, 3, 1)
                self._convert_cifar10_dataset("test", cifar10_dir, images, labels)
                os.remove(f)

    def _after_downloads(self, local_path: pathlib.Path):
        """
        Post-processing of dowloaded dataset.
        """
        self._process_cifra10_dataset(local_path)
