import xarray as xr
import numpy as np
from scipy import signal
import scipy.stats as sts


def convert_lon(lon):
    """将经度换算到[-180, 180]范围内."""
    return (lon + 180) % 360 - 180


def DeTrend(array):
    array = np.array(array)
    flag = np.isnan(array).sum(axis=0) != 0
    flags = np.repeat(flag[np.newaxis, ...], axis=0, repeats=array.shape[0])
    array[flags] = 0
    res = signal.detrend(array, axis=0)
    res[flags] = np.NAN
    return res


def GetSlopePv(data1, data2):
    res = sts.linregress(data2, data1)
    slope, intep, p_value, corr = res.slope, res.intercept, res.pvalue, res.rvalue
    return slope, intep, p_value, corr


def lingReg(data1, data2):
    """
    data1: y
    data2: x
    """
    dim0 = data1.dims[0]
    # print(dim0)
    return xr.apply_ufunc(GetSlopePv,
                          data1,
                          input_core_dims=[[dim0]],
                          kwargs={"data2": data2},
                          output_core_dims=[[], [], [], []],
                          vectorize=True)


def GetAnom(DaArray, method=0):
    if method == 0:
        anom = DaArray.groupby("time.month") - DaArray.groupby("time.month").mean()
    if method == 1:
        anom = DaArray.groupby("time.month").map(DeTrend)

    return anom
