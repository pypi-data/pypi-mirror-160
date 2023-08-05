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
import typing

from deel.datasets.dataset import Dataset
from deel.datasets.providers.http_providers import HttpMultiFilesProvider
from deel.datasets.settings import Settings

from .cifra10 import Cifar10Provider
from .mnist import MnistProvider
from .svhn import SvhnProvider


class SvhnDataset(Dataset):

    """
    Class for the public svhn dataset.
    """

    # URL of the remote file:
    SVHN_REMOTE_FILES = [
        # "http://ufldl.stanford.edu/housenumbers/train.tar.gz",
        # "http://ufldl.stanford.edu/housenumbers/test.tar.gz",
        # "http://ufldl.stanford.edu/housenumbers/extra.tar.gz",
        "http://ufldl.stanford.edu/housenumbers/train_32x32.mat",
        "http://ufldl.stanford.edu/housenumbers/test_32x32.mat",
        "http://ufldl.stanford.edu/housenumbers/extra_32x32.mat",
    ]

    def __init__(
        self, version: str = "latest", settings: typing.Optional[Settings] = None
    ):
        """
        Args:
            version: Version of the dataset.
            settings: The settings to use for this dataset, or `None` to use the
            default settings.
        """
        super().__init__("svhn", version, settings)

    def _get_provider(self) -> HttpMultiFilesProvider:
        svhnProvider = SvhnProvider(
            self._settings.local_storage, SvhnDataset.SVHN_REMOTE_FILES
        )
        return svhnProvider


class MnistDataset(Dataset):

    """
    Class for the public mnist dataset.
    """

    # URL of the remote file:
    MNIST_REMOTE_FILES = [
        "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz",
        "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz",
        "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz",
        "http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz",
    ]

    def __init__(
        self, version: str = "latest", settings: typing.Optional[Settings] = None
    ):
        """
        Args:
            version: Version of the dataset.
            settings: The settings to use for this dataset, or `None` to use the
            default settings.
        """
        super().__init__("mnist", version, settings)

    def _get_provider(self) -> HttpMultiFilesProvider:
        mnistProvider = MnistProvider(
            self._settings.local_storage, MnistDataset.MNIST_REMOTE_FILES
        )
        return mnistProvider


class Cifra10Dataset(Dataset):

    """
    Class for the public cifra10 dataset.
    """

    # URL of the remote file:
    CIFRA10_REMOTE_FILES = [
        "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz",
    ]

    def __init__(
        self, version: str = "latest", settings: typing.Optional[Settings] = None
    ):
        """
        Args:
            version: Version of the dataset.
            settings: The settings to use for this dataset, or `None` to use the
            default settings.
        """
        super().__init__("cifra10", version, settings)

    def _get_provider(self) -> HttpMultiFilesProvider:
        cifar10Provider = Cifar10Provider(
            self._settings.local_storage, Cifra10Dataset.CIFRA10_REMOTE_FILES
        )
        return cifar10Provider
