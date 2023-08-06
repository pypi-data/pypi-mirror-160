import os

import pytest
import numpy as np

from empyre.fields import Field


@pytest.fixture
def fielddata_path():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_fielddata')


@pytest.fixture
def vector_data():
    magnitude = np.zeros((4, 4, 4, 3))
    magnitude[1:-1, 1:-1, 1:-1] = 1
    return Field(magnitude, 10.0, vector=True)


@pytest.fixture
def vector_data_asymm():
    shape = (5, 7, 11, 3)
    data = np.linspace(0, 1, np.prod(shape))
    return Field(data.reshape(shape), 10.0, vector=True)


@pytest.fixture
def vector_data_asymm_2d():
    shape = (5, 7, 2)
    data = np.linspace(0, 1, np.prod(shape))
    return Field(data.reshape(shape), 10.0, vector=True)


@pytest.fixture
def vector_data_asymmcube():
    shape = (3, 3, 3, 3)
    data = np.linspace(0, 1, np.prod(shape))
    return Field(data.reshape(shape), 10.0, vector=True)


@pytest.fixture
def scalar_data():
    magnitude = np.zeros((4, 4, 4))
    magnitude[1:-1, 1:-1, 1:-1] = 1
    return Field(magnitude, 10.0, vector=False)


@pytest.fixture
def scalar_data_asymm():
    shape = (5, 7, 2)
    data = np.linspace(0, 1, np.prod(shape))
    return Field(data.reshape(shape), 10.0, vector=False)
