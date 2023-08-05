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
from mnist import MNIST
from PIL import Image
from tqdm import tqdm


class MnistProvider(HttpMultiFilesProvider):
    # list of labels in CIFRA-10 dataset

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
        super().__init__(root_folder, remote_url_list, "mnist")

    def _convert_mnist_dataset(
        self,
        data_type: str,
        local_path: pathlib.Path,
        images: typing.List,
        labels: typing.List,
    ):
        """
        This method allows to extract MNIST dataset images and save
        them in their label directory.

        Args:
            data_type: train or test or other
            local_path: local parent directory
            images: list of images
            labels: list of labels
        """
        train_dir = local_path.joinpath(data_type)
        os.makedirs(train_dir, exist_ok=True)
        label_iter = iter(labels)
        numImages = len(images)

        images_iterator = iter(images)
        with tqdm(
            total=len(images),
            desc="convert {} images".format(data_type),
        ) as pbar:
            for image in range(0, numImages):
                im = next(images_iterator)
                lab = next(label_iter)
                # create a np array to save the image
                im = np.array(im, dtype="uint8")
                im = im.reshape(28, 28)
                im = Image.fromarray(im)

                dest = train_dir.joinpath(
                    str(lab), "{}_{}.bmp".format(data_type, image)
                )
                os.makedirs(dest.parent, exist_ok=True)
                im.save(dest, "bmp")
                pbar.update(1)

        pbar.close()

    def _process_mnist_dataset(self, local_path: pathlib.Path):
        """
        This method process and save MNIST dataset
        """
        f1 = local_path.joinpath("train-images-idx3-ubyte")
        f2 = local_path.joinpath("train-labels-idx1-ubyte")
        f3 = local_path.joinpath("t10k-images-idx3-ubyte")
        f4 = local_path.joinpath("t10k-labels-idx1-ubyte")
        if f1.exists() and f2.exists() and f3.exists() and f4.exists():
            mnistdata = MNIST(local_path)
            images, labels = mnistdata.load_training()
            self._convert_mnist_dataset("train", local_path, images, labels)
            images, labels = mnistdata.load_testing()
            self._convert_mnist_dataset("test", local_path, images, labels)
            os.remove(f1)
            os.remove(f2)
            os.remove(f3)
            os.remove(f4)

    def _after_downloads(self, local_path: pathlib.Path):
        """
        Post-processing of dowloaded dataset.
        Case of MNIST dataset save images in corresponding label directory
        """
        self._process_mnist_dataset(local_path)
