import numpy
import numpy.testing


def assert_allclose(actual, desired, rtol=1e-07, atol=1e-08, equal_nan=True, err_msg='', verbose=True):
    return numpy.testing.assert_allclose(
        actual=actual,
        desired=desired,
        rtol=rtol,
        atol=atol,
        equal_nan=equal_nan,
        err_msg=err_msg,
        verbose=verbose,
    )
