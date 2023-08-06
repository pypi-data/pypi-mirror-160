import pytest

from utils import assert_allclose

from empyre.fields import Field
import numpy as np


@pytest.mark.parametrize(
    'axis', ['x', 'y', 'z']
)
def test_rot90_360(vector_data_asymm, axis):
    assert_allclose(vector_data_asymm.rot90(axis=axis).rot90(axis=axis).rot90(axis=axis).rot90(axis=axis),
                    vector_data_asymm,
                    err_msg=f'Unexpected behavior in rot90()! {axis}')


@pytest.mark.parametrize(
    'rot_axis,flip_axes', [
        ('x', (0, 1)),
        ('y', (0, 2)),
        ('z', (1, 2))
    ]
)
def test_rot90_180(vector_data_asymm, rot_axis, flip_axes):
    res = vector_data_asymm.rot90(axis=rot_axis).rot90(axis=rot_axis)
    ref = vector_data_asymm.flip(axis=flip_axes)
    assert_allclose(res, ref, err_msg=f'Unexpected behavior in rot90()! {rot_axis}')


@pytest.mark.parametrize(
    'rot_axis', [
        'x',
        'y',
        'z',
    ]
)
def test_rotate_compare_rot90_1(vector_data_asymmcube, rot_axis):
    res = vector_data_asymmcube.rotate(angle=90, axis=rot_axis)
    ref = vector_data_asymmcube.rot90(axis=rot_axis)
    print("input", vector_data_asymmcube.data)
    print("ref", res.data)
    print("res", ref.data)
    assert_allclose(res, ref, err_msg=f'Unexpected behavior in rotate()! {rot_axis}')


def test_rot90_manual():
    data = np.zeros((3, 3, 3, 3))
    diag = np.array((1, 1, 1))
    diag_unity = diag / np.sqrt(np.sum(diag**2))
    data[0, 0, 0] = diag_unity
    data = Field(data, 10, vector=True)
    print("data", data.data)

    rot90_x = np.zeros((3, 3, 3, 3))
    # Axis order z, y, x; vector components x, y, z
    rot90_x[0, 2, 0] = diag_unity * (1, -1, 1)
    rot90_x = Field(rot90_x, 10, vector=True)
    print("rot90_x", rot90_x.data)
    print("data rot90 x", data.rot90(axis='x').data)

    rot90_y = np.zeros((3, 3, 3, 3))
    # Axis order z, y, x; vector components x, y, z
    rot90_y[2, 0, 0] = diag_unity * (1, 1, -1)
    rot90_y = Field(rot90_y, 10, vector=True)
    print("rot90_y", rot90_y.data)
    print("data rot90 y", data.rot90(axis='y').data)

    rot90_z = np.zeros((3, 3, 3, 3))
    # Axis order z, y, x; vector components x, y, z
    rot90_z[0, 0, 2] = diag_unity * (-1, 1, 1)
    rot90_z = Field(rot90_z, 10, vector=True)
    print("rot90_z", rot90_z.data)
    print("data rot90 z", data.rot90(axis='z').data)

    assert_allclose(rot90_x, data.rot90(axis='x'), err_msg='Unexpected behavior in rot90("x")!')
    assert_allclose(rot90_y, data.rot90(axis='y'), err_msg='Unexpected behavior in rot90("y")!')
    assert_allclose(rot90_z, data.rot90(axis='z'), err_msg='Unexpected behavior in rot90("z")!')


def test_rot45_manual():
    data = np.zeros((3, 3, 3, 3))
    data[0, 0, 0] = (1, 1, 1)
    data = Field(data, 10, vector=True)
    print("data", data.data)

    rot45_x = np.zeros((3, 3, 3, 3))
    # Axis order z, y, x; vector components x, y, z
    rot45_x[0, 1, 0] = (1, 0, np.sqrt(2))
    rot45_x = Field(rot45_x, 10, vector=True)
    print("rot45_x", rot45_x.data)
    # Disable spline interpolation, use nearest instead
    res_rot45_x = data.rotate(45, axis='x', order=0)
    print("data rot45 x", res_rot45_x.data)

    rot45_y = np.zeros((3, 3, 3, 3))
    # Axis order z, y, x; vector components x, y, z
    rot45_y[1, 0, 0] = (np.sqrt(2), 1, 0)
    rot45_y = Field(rot45_y, 10, vector=True)
    print("rot45_y", rot45_y.data)
    # Disable spline interpolation, use nearest instead
    res_rot45_y = data.rotate(45, axis='y', order=0)
    print("data rot45 y", res_rot45_y.data)

    rot45_z = np.zeros((3, 3, 3, 3))
    # Axis order z, y, x; vector components x, y, z
    rot45_z[0, 0, 1] = (0, np.sqrt(2), 1)
    rot45_z = Field(rot45_z, 10, vector=True)
    print("rot45_z", rot45_z.data)
    # Disable spline interpolation, use nearest instead
    res_rot45_z = data.rotate(45, axis='z', order=0)
    print("data rot45 z", res_rot45_z.data)

    assert_allclose(rot45_x, res_rot45_x, err_msg='Unexpected behavior in rotate(45, "x")!')
    assert_allclose(rot45_y, res_rot45_y, err_msg='Unexpected behavior in rotate(45, "y")!')
    assert_allclose(rot45_z, res_rot45_z, err_msg='Unexpected behavior in rotate(45, "z")!')


def test_rot90_2d_360(vector_data_asymm_2d):
    assert_allclose(vector_data_asymm_2d.rot90().rot90().rot90().rot90(), vector_data_asymm_2d,
                    err_msg='Unexpected behavior in 2D rot90()!')


def test_rot90_2d_180(vector_data_asymm_2d):
    res = vector_data_asymm_2d.rot90().rot90()
    ref = vector_data_asymm_2d.flip()
    assert_allclose(res, ref, err_msg='Unexpected behavior in 2D rot90()!')


@pytest.mark.parametrize(
    'k', [0, 1, 2, 3, 4]
)
def test_rot90_comp_2d_with_3d(vector_data_asymm_2d, k):
    data_x, data_y = [comp.data[np.newaxis, :, :] for comp in vector_data_asymm_2d.comp]
    data_z = np.zeros_like(data_x)
    data_3d = np.stack([data_x, data_y, data_z], axis=-1)
    vector_data_asymm_3d = Field(data_3d, scale=10, vector=True)
    print(f'2D shape, scale: {vector_data_asymm_2d.shape, vector_data_asymm_2d.scale}')
    print(f'3D shape, scale: {vector_data_asymm_3d.shape, vector_data_asymm_3d.scale}')
    vector_data_rot_2d = vector_data_asymm_2d.rot90(k=k)
    vector_data_rot_3d = vector_data_asymm_3d.rot90(k=k, axis='z')
    print(f'2D shape after rot: {vector_data_rot_2d.shape}')
    print(f'3D shape after rot: {vector_data_rot_3d.shape}')
    assert_allclose(vector_data_rot_2d, vector_data_rot_3d[0, :, :, :2], err_msg='Unexpected behavior in 2D rot90()!')


@pytest.mark.parametrize(
    'angle', [90, 45, 23, 11.5]
)
def test_rotate_comp_2d_with_3d(vector_data_asymm_2d, angle):
    data_x, data_y = [comp.data[np.newaxis, :, :] for comp in vector_data_asymm_2d.comp]
    data_z = np.zeros_like(data_x)
    data_3d = np.stack([data_x, data_y, data_z], axis=-1)
    vector_data_asymm_3d = Field(data_3d, scale=10, vector=True)
    print(f'2D shape, scale: {vector_data_asymm_2d.shape, vector_data_asymm_2d.scale}')
    print(f'3D shape, scale: {vector_data_asymm_3d.shape, vector_data_asymm_3d.scale}')
    r2d = vector_data_asymm_2d.rotate(angle)
    r3d = vector_data_asymm_3d.rotate(angle, axis='z')
    print(f'2D shape after rot: {r2d.shape}')
    print(f'3D shape after rot: {r3d.shape}')
    assert_allclose(r2d, r3d[0, :, :, :2], err_msg='Unexpected behavior in 2D rotate()!')


@pytest.mark.parametrize(
    'angle', [180, 360, 90, 45, 23, 11.5],
)
@pytest.mark.parametrize(
    'axis', ['x', 'y', 'z'],
)
def test_rotate_scalar(vector_data_asymm, angle, axis):

    data = np.zeros((1, 2, 2, 3))
    data[0, 0, 0] = 1
    field = Field(data, scale=10., vector=True)
    print(field)
    print(field.amp)

    assert_allclose(
        field.rotate(angle, axis=axis).amp,
        field.amp.rotate(angle, axis=axis)
    )


@pytest.mark.parametrize(
    'angle,order', [(180, 3), (360, 3), (90, 3), (45, 0), (23, 0), (11.5, 0)],
)
@pytest.mark.parametrize(
    'axis', ['x', 'y', 'z'],
)
@pytest.mark.parametrize(
    'reshape', [True, False],
)
def test_rotate_scalar_asymm(vector_data_asymm, angle, axis, order, reshape):
    assert_allclose(
        vector_data_asymm.rotate(angle, axis=axis, reshape=reshape, order=order).amp,
        vector_data_asymm.amp.rotate(angle, axis=axis, reshape=reshape, order=order)
    )


@pytest.mark.parametrize(
    'axis', ['x', 'y', 'z'],
)
@pytest.mark.parametrize(
    'k', [0, 1, 2, 3, 4],
)
def test_rot90_scalar(vector_data_asymm, axis, k):
    assert_allclose(
        vector_data_asymm.amp.rot90(k=k, axis=axis),
        vector_data_asymm.rot90(k=k, axis=axis).amp
    )
