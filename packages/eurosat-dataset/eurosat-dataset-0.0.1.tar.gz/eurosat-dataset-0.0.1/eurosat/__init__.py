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
from deel.datasets.providers.http_providers import HttpSingleFileProvider
from deel.datasets.settings import Settings


class EurosatDataset(Dataset):

    """
    Class for the blink dataset.
    """

    # URL of the remote file:
    EUROSAT_REMOTE_FILE = "http://madm.dfki.de/files/sentinel/EuroSAT.zip"

    _default_mode: str = "path"

    def __init__(
        self, version: str = "latest", settings: typing.Optional[Settings] = None
    ):
        """
        Args:
            version: Version of the dataset.
            settings: The settings to use for this dataset, or `None` to use the
            default settings.
        """
        super().__init__("eurosat", version, settings)

    def _get_provider(self) -> HttpSingleFileProvider:
        return HttpSingleFileProvider(
            self._settings.local_storage, EurosatDataset.EUROSAT_REMOTE_FILE, "eurosat"
        )
