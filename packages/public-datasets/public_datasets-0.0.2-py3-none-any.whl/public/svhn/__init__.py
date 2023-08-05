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

import matplotlib.pyplot as plt
import scipy.io as sio
from deel.datasets.providers.http_providers import HttpMultiFilesProvider


class SvhnProvider(HttpMultiFilesProvider):
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
        super().__init__(root_folder, remote_url_list, "svhn")

    def _process_svhn_dataset(self, file: pathlib.Path):
        for f in file.glob("*.mat"):
            mat = sio.loadmat(f)
            images = mat["X"]
            labels = mat["y"]
            os.mkdir(os.path.join(f.with_suffix("")))
            for i in range(images.shape[3]):
                plt.figure()
                lab = labels[i][0] if labels[i][0] != 10 else 0
                dest = f.with_suffix("").joinpath(str(lab), "%05d.png" % i)
                if not os.path.isfile(dest):
                    os.makedirs(dest.parent, exist_ok=True)
                    plt.imsave(dest, images[..., i])
                plt.close()
            os.remove(f)

    def _after_downloads(self, local_path: pathlib.Path):
        """
        Post-processing of dowloaded dataset.
        Case of MNIST dataset save images in corresponding label directory
        """
        self._process_svhn_dataset(local_path)
