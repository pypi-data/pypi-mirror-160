# -*- coding: utf-8 -*-
"""Testcase for the magdata module."""

import pytest

from numbers import Number

import numpy as np
import numpy.testing

from empyre.fields import Field

from utils import assert_allclose


def test_copy(vector_data):
    vector_data = vector_data.copy()
    # Make sure it is a new object
    assert vector_data != vector_data, 'Unexpected behaviour in copy()!'
    assert np.allclose(vector_data, vector_data)


def test_bin(vector_data):
    binned_data = vector_data.bin(2)
    reference = 1 / 8. * np.ones((2, 2, 2, 3))
    assert_allclose(binned_data, reference,
                    err_msg='Unexpected behavior in scale_down()!')
    assert_allclose(binned_data.scale, (20, 20, 20),
                    err_msg='Unexpected behavior in scale_down()!')


def test_zoom(vector_data):
    zoomed_test = vector_data.zoom(2, order=0)
    reference = np.zeros((8, 8, 8, 3))
    reference[2:6, 2:6, 2:6] = 1
    assert_allclose(zoomed_test, reference,
                    err_msg='Unexpected behavior in zoom()!')
    assert_allclose(zoomed_test.scale, (5, 5, 5),
                    err_msg='Unexpected behavior in zoom()!')


@pytest.mark.parametrize(
    'mode', [
        'constant',
        'edge',
        'wrap'
    ]
)
@pytest.mark.parametrize(
    'pad_width,np_pad', [
        (1, ((1, 1), (1, 1), (1, 1), (0, 0))),
        ((1, 2, 3), ((1, 1), (2, 2), (3, 3), (0, 0))),
        (((1, 2), (3, 4), (5, 6)), ((1, 2), (3, 4), (5, 6), (0, 0)))
    ]
)
def test_pad(vector_data, mode, pad_width, np_pad):
    magdata_test = vector_data.pad(pad_width, mode=mode)
    reference = np.pad(vector_data, np_pad, mode=mode)
    assert_allclose(magdata_test, reference,
                    err_msg='Unexpected behavior in pad()!')


@pytest.mark.parametrize(
    'axis', [-1, 3]
)
def test_component_reduction(vector_data, axis):
    # axis=-1 is supposed to reduce over the component dimension, if it exists. axis=3 should do the same here!
    res = np.sum(vector_data, axis=axis)
    ref = np.zeros((4, 4, 4))
    ref[1:-1, 1:-1, 1:-1] = 3
    assert res.shape == ref.shape, 'Shape mismatch!'
    assert_allclose(res, ref, err_msg="Unexpected behavior of axis keyword")
    assert isinstance(res, Field), 'Result is not a Field object!'
    assert not res.vector, 'Result is a vector field, but should be reduced to a scalar!'


@pytest.mark.parametrize(
    'axis', [(0, 1, 2), (2, 1, 0), None, (-4, -3, -2)]
)
def test_full_reduction(vector_data, axis):
    res = np.sum(vector_data, axis=axis)
    ref = np.zeros((3,))
    ref[:] = 8
    assert res.shape == ref.shape
    assert_allclose(res, ref, err_msg="Unexpected behavior of full or default reduction")
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize(
    'axis', [-1, 2]
)
def test_last_reduction_scalar(scalar_data, axis):
    # axis=-1 is supposed to reduce over the component dimension if it exists.
    # In this case it doesn't!
    res = np.sum(scalar_data, axis=axis)
    ref = np.zeros((4, 4))
    ref[1:-1, 1:-1] = 2
    assert res.shape == ref.shape
    assert_allclose(res, ref, err_msg="Unexpected behavior of axis keyword")
    assert isinstance(res, Field)
    assert not res.vector


@pytest.mark.parametrize(
    'axis', [(0, 1, 2), (2, 1, 0), None, (-1, -2, -3)]
)
def test_full_reduction_scalar(scalar_data, axis):
    res = np.sum(scalar_data, axis=axis)
    ref = 8
    assert res.shape == ()
    assert_allclose(res, ref, err_msg="Unexpected behavior of full or default reduction")
    assert isinstance(res, Number)


def test_binary_operator_vector_number(vector_data):
    res = vector_data + 1
    ref = np.ones((4, 4, 4, 3))
    ref[1:-1, 1:-1, 1:-1] = 2
    assert res.shape == ref.shape
    assert_allclose(res, ref, err_msg="Unexpected behavior of addition")
    assert isinstance(res, Field)
    assert res.vector


def test_binary_operator_vector_scalar(vector_data, scalar_data):
    res = vector_data + scalar_data
    ref = np.zeros((4, 4, 4, 3))
    ref[1:-1, 1:-1, 1:-1] = 2
    assert res.shape == ref.shape
    assert_allclose(res, ref, err_msg="Unexpected behavior of addition")
    assert isinstance(res, Field)
    assert res.vector


def test_binary_operator_vector_vector(vector_data):
    res = vector_data + vector_data
    ref = np.zeros((4, 4, 4, 3))
    ref[1:-1, 1:-1, 1:-1] = 2
    assert res.shape == ref.shape
    assert_allclose(res, ref, err_msg="Unexpected behavior of addition")
    assert isinstance(res, Field)
    assert res.vector


@pytest.mark.xfail
def test_binary_operator_vector_broadcast(vector_data):
    # Broadcasting between vector fields is currently not implemented
    second = np.zeros((4, 4, 3))
    second[1:-1, 1:-1] = 1
    second = Field(second, 10.0, vector=True)
    res = vector_data + second
    ref = np.zeros((4, 4, 4, 3))
    ref[1:-1, 1:-1, 1:-1] = 1
    ref[:, 1:-1, 1:-1] += 1
    assert res.shape == ref.shape
    assert_allclose(res, ref, err_msg="Unexpected behavior of addition")
    assert isinstance(res, Field)
    assert res.vector


def test_mask(vector_data):
    mask = vector_data.mask
    reference = np.zeros((4, 4, 4))
    reference[1:-1, 1:-1, 1:-1] = True
    assert_allclose(mask, reference,
                    err_msg='Unexpected behavior in mask attribute!')


def test_get_vector(vector_data):
    mask = vector_data.mask
    vector = vector_data.get_vector(mask)
    reference = np.ones(np.sum(mask) * 3)
    assert_allclose(vector, reference,
                    err_msg='Unexpected behavior in get_vector()!')


def test_set_vector(vector_data):
    mask = vector_data.mask
    vector = 2 * np.ones(np.sum(mask) * 3)
    vector_data.set_vector(vector, mask)
    reference = np.zeros((4, 4, 4, 3))
    reference[1:-1, 1:-1, 1:-1] = 2
    assert_allclose(vector_data, reference,
                    err_msg='Unexpected behavior in set_vector()!')


def test_flip(vector_data_asymm):
    field_flipz = vector_data_asymm.flip(0)
    field_flipy = vector_data_asymm.flip(1)
    field_flipx = vector_data_asymm.flip(2)
    field_flipxy = vector_data_asymm.flip((1, 2))
    field_flipdefault = vector_data_asymm.flip()
    field_flipcomp = vector_data_asymm.flip(-1)
    assert_allclose(np.flip(vector_data_asymm.data, axis=0) * [1, 1, -1], field_flipz.data,
                    err_msg='Unexpected behavior in flip()! (z)')
    assert_allclose(np.flip(vector_data_asymm.data, axis=1) * [1, -1, 1], field_flipy.data,
                    err_msg='Unexpected behavior in flip()! (y)')
    assert_allclose(np.flip(vector_data_asymm.data, axis=2) * [-1, 1, 1], field_flipx.data,
                    err_msg='Unexpected behavior in flip()! (x)')
    assert_allclose(np.flip(vector_data_asymm.data, axis=(1, 2)) * [-1, -1, 1], field_flipxy.data,
                    err_msg='Unexpected behavior in flip()! (xy)')
    assert_allclose(np.flip(vector_data_asymm.data, axis=(0, 1, 2)) * [-1, -1, -1], field_flipdefault.data,
                    err_msg='Unexpected behavior in flip()! (default)')
    assert_allclose(np.flip(vector_data_asymm.data, axis=-1) * [1, 1, 1], field_flipcomp.data,
                    err_msg='Unexpected behavior in flip()! (components)')


def test_unknown_num_of_components():
    shape = (5, 7, 7)
    data = np.linspace(0, 1, np.prod(shape))
    with pytest.raises(AssertionError):
        Field(data.reshape(shape), 10.0, vector=True)


def test_repr(vector_data_asymm):
    string_repr = repr(vector_data_asymm)
    data_str = str(vector_data_asymm.data)
    string_ref = f'Field(data={data_str}, scale=(10.0, 10.0, 10.0), vector=True)'
    print(f'reference: {string_ref}')
    print(f'repr output: {string_repr}')
    assert string_repr == string_ref, 'Unexpected behavior in __repr__()!'


def test_str(vector_data_asymm):
    string_str = str(vector_data_asymm)
    string_ref = 'Field(dim=(5, 7, 11), scale=(10.0, 10.0, 10.0), vector=True, ncomp=3)'
    print(f'reference: {string_str}')
    print(f'str output: {string_str}')
    assert string_str == string_ref, 'Unexpected behavior in __str__()!'


@pytest.mark.parametrize(
    "index,t,scale", [
        ((0, 1, 2), tuple, None),
        ((0, ), Field, (2., 3.)),
        (0, Field, (2., 3.)),
        ((0, 1, 2, 0), float, None),
        ((0, 1, 2, 0), float, None),
        ((..., 0), Field, (1., 2., 3.)),
        ((0, slice(1, 3), 2), Field, (2.,)),
    ]
)
def test_getitem(vector_data, index, t, scale):
    vector_data.scale = (1., 2., 3.)
    data_index = index
    res = vector_data[index]
    assert_allclose(res, vector_data.data[data_index])
    assert isinstance(res, t)
    if t is Field:
        assert res.scale == scale


def test_from_scalar_field(scalar_data):
    sca_x, sca_y, sca_z = [i * scalar_data for i in range(1, 4)]
    field_comb = Field.from_scalar_fields([sca_x, sca_y, sca_z])
    assert field_comb.vector
    assert field_comb.scale == scalar_data.scale
    assert_allclose(sca_x, field_comb.comp[0])
    assert_allclose(sca_y, field_comb.comp[1])
    assert_allclose(sca_z, field_comb.comp[2])


def test_squeeze():
    magnitude = np.zeros((4, 1, 4, 3))
    field = Field(magnitude, (1., 2., 3.), vector=True)
    sq = field.squeeze()
    assert sq.shape == (4, 4, 3)
    assert sq.dim == (4, 4)
    assert sq.scale == (1., 3.)


def test_gradient():
    pass


def test_gradient_1d():
    pass


def test_curl():
    pass


def test_curl_2d():
    pass


def test_clip_scalar_noop():
    shape = (3, 3, 3)
    data = np.linspace(-2, 1, np.prod(shape)).reshape(shape)
    field = Field(data, (1., 2., 3.), vector=False)
    assert_allclose(field, field.clip())


def test_clip_scalar_minmax():
    shape = (3, 3, 3)
    data = np.linspace(-2, 1, np.prod(shape)).reshape(shape)
    field = Field(data, (1., 2., 3.), vector=False)
    assert_allclose(np.clip(data, -1, 0.1), field.clip(vmin=-1, vmax=0.1))


def test_clip_scalar_sigma():
    shape = (3, 3, 3)
    data = np.linspace(-2, 1, np.prod(shape)).reshape(shape)
    data[0, 0, 0] = 1e6
    field = Field(data, (1., 2., 3.), vector=False)
    # We clip off the one outlier
    assert_allclose(np.clip(data, -2, 1), field.clip(sigma=5))
    assert field.clip(sigma=5)[0, 0, 0] == 1


def test_clip_scalar_mask():
    shape = (3, 3, 3)
    data = np.linspace(-2, 1, np.prod(shape)).reshape(shape)
    mask = np.zeros(shape, dtype=bool)
    mask[0, 0, 0] = True
    mask[0, 0, 1] = True
    field = Field(data, (1., 2., 3.), vector=False)
    assert_allclose(np.clip(data, data[0, 0, 0], data[0, 0, 1]), field.clip(mask=mask))


def test_clip_vector_noop():
    shape = (3, 3, 3, 3)
    data = np.linspace(-2, 1, np.prod(shape)).reshape(shape)
    field = Field(data, (1., 2., 3.), vector=True)
    assert_allclose(field, field.clip())


def test_clip_vector_max():
    shape = (3, 3, 3, 3)
    data = np.linspace(-2, 1, np.prod(shape)).reshape(shape)
    field = Field(data, (1., 2., 3.), vector=True)
    res = field.clip(vmax=0.1)
    assert_allclose(np.max(res.amp), 0.1)


def test_clip_vector_sigma():
    shape = (3, 3, 3, 3)
    data = np.linspace(-2, 1, np.prod(shape)).reshape(shape)
    data[0, 0, 0] = (1e6, 1e6, 1e6)
    field = Field(data, (1., 2., 3.), vector=True)
    # We clip off the one outlier
    res = field.clip(sigma=5)
    assert np.max(res.amp) < 1e3


# TODO: HyperSpy would need to be installed for the following tests (slow...):
# def test_from_signal()
#     raise NotImplementedError()
#
# def test_to_signal()
#     raise NotImplementedError()
