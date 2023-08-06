import numpy as np
import lmfit


def oneD_Gaussian(x, x0, x_sigma, A, offset):
    return A * np.exp(-(x - x0) ** 2 / (2 * x_sigma ** 2)) + offset


def oneD_Gaussian_normalized(x, x0, x_sigma):
    return np.exp(-(x - x0) ** 2 / (2 * x_sigma ** 2))


def twoD_Gaussian(x, y, x0, y0, x_sigma, y_sigma, A, offset):
    return A * np.exp(-(x - x0) ** 2 / (2 * x_sigma ** 2)) * np.exp(-(y - y0) ** 2 / (2 * y_sigma ** 2)) + offset


class Fitting:

    def __init__(self, data, parameters, fitting_function, independent_vars, independent_vars_value):
        self.data = data
        self.parameters = parameters
        self.fitting_function = fitting_function
        self.fit_function_kws = independent_vars_value
        self.independent_vars = independent_vars
        self.fitting_model = None
        self.result = None
        self.data_fit = None

    def __enter__(self):
        self.run_fitting()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def set_parameters(self, parameters):
        self.parameters = parameters

    def run_fitting(self):
        self.fitting_model = lmfit.Model(self.fitting_function, independent_vars=self.independent_vars)
        self.result = self.fitting_model.fit(self.data, params=self.parameters, **self.fit_function_kws)

    def get_fitting_data(self, data_shape):
        self.data_fit = self.fitting_function(**self.fit_function_kws, **self.result.best_values)
        self.data_fit = self.data_fit.reshape(data_shape)
        return self.data_fit
