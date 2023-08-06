import numpy as np
import scipy.stats as sts

EPS = 1e-10


def linear_reg(x: np.ndarray, y: np.ndarray):
    Num0 = x.shape[0]
    Num1 = y.shape[0]
    org_sp_Y = y.shape
    if Num0 != Num1:
        raise (ValueError("x.shape[0] no equal to y.shape[0] , dim0 is wrong"))
    print(Num1)
    y_rs = y.reshape(Num1, -1)
    print(y_rs.shape)
    xa = x - x.mean(axis=0)
    ya = y_rs - y_rs.mean(axis=0)
    y_std = ya.std(axis=0)
    x_std = xa.std(axis=0)
    covar = ya.T @ xa / Num0
    corr = covar / y_std / x_std
    slope = corr * y_std / x_std
    intcpt = y_rs.mean(axis=0) - slope * x.mean(axis=0)
    t = corr / np.sqrt(1 - corr**2) * np.sqrt(Num0 - 2)
    p_value = sts.t.sf(t, df=Num0 - 2)
    pv_cp = np.copy(p_value)
    p_value[pv_cp >= 0.5] = (1 - p_value[pv_cp >= 0.5]) * 2
    p_value[pv_cp < 0.5] = (p_value[pv_cp < 0.5]) * 2
    slope, intcpt, corr, p_value = list(map(lambda inar: inar.reshape(org_sp_Y[1:]), [slope, intcpt, corr, p_value]))
    return slope, intcpt, corr, p_value


class Lin_reg():

    def __init__(self, x: np.ndarray, y: np.ndarray):
        self.slope, self.intcpt, self.corr, self.p_value = linear_reg(x, y)


def multi_linreg(x: np.ndarray, y: np.ndarray):
    Num0 = x.shape[0]
    Num1 = y.shape[0]
    Numf = x.shape[1]
    org_sp_Y = y.shape
    if Num0 != Num1:
        raise (ValueError("x.shape[0] no equal to y.shape[0] , dim0 is wrong"))
    y_rs = y.reshape(Num1, -1)
    x_mean = x.mean(axis=0)
    y_mean = y_rs.mean(axis=0)
    xa = x - x_mean
    ya = y_rs - y_mean
    covar_xx = xa.T @ xa / Num0
    covar_yx = xa.T @ ya / Num0
    slope = np.linalg.solve(covar_xx, covar_yx)  #　(Numf , Num space)
    # print(slope.shape)
    intcpt = y_mean - slope.T @ x_mean
    y_pre = xa @ slope
    SSyy = Num0 * y_rs.var(axis=0)
    U = Num0 * y_pre.var(axis=0)
    Q = SSyy - U
    R = np.sqrt(U / SSyy)  # (Num space)
    F = U / Numf / (Q / (Num0 - Numf - 1))
    C_mx = np.diagonal(np.linalg.inv(covar_xx))
    Q_mx = slope**2 / C_mx[..., np.newaxis]  # (Numf,Num space)
    # print(Q_mx)
    F_i = Q_mx / (Q / (Num0 - Numf - 1))  # (Numf,Num space)
    # print(F_i)
    pv_all = 1 - sts.f.cdf(F, Num0 - Numf - 1, Num0)  # (Num space)
    pv_i = 1 - sts.f.cdf(F_i, Num0 - Numf - 1, 1)  # (Numf,Num space)
    pv_all, R, intcpt = list(map(lambda inar: inar.reshape(org_sp_Y[1:]), [pv_all, R, intcpt]))
    slope, pv_i = list(map(lambda inar: inar.reshape([Numf, *org_sp_Y[1:]]), [slope, pv_i]))
    return slope, intcpt, R, pv_all, pv_i


class Mult_lin_reg():

    def __init__(self, x: np.ndarray, y: np.ndarray):
        self.slope, self.intcpt, self.R, self.pv_all, self.pv_i = multi_linreg(x, y)


if __name__ == "__main__":
    pass
    np.random.seed(10)
    x = np.random.randn(10)
    x1 = np.random.randn(10)
    err = np.random.randn(10) * 0.1
    y = -1.5 * x + 0.6 + err * 0.02 + 1.0 * x1
    y = np.repeat(y[np.newaxis, ...], axis=0, repeats=10000).T
    y = y.reshape(10, 100, 100)
    x_all = np.vstack([x, x1]).T
    print(linear_reg(x1, y))
