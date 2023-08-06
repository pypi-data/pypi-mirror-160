import numpy as np
from dylab import FittingFunction
import laserbeamsize as lbs
import lmfit
from lmfit.minimizer import MinimizerResult


class OneD_Gaussian_fitting(FittingFunction.Fitting):

    def __init__(self, data, x, fitting_function=None):
        self.data = data
        self.x = x
        self.x0 = None
        self.x_sigma = None
        self.amplitude = None
        self.offset = None
        self.x0_arg = None
        self.x_sigma_arg = None

        # Use d4sigma method estimating the start point
        self.find_start_point()

        # Initialize the fitting parameters
        self.parameters = lmfit.Parameters()
        self.independent_vars = ['x']
        if fitting_function is None:
            self.fitting_function = FittingFunction.oneD_Gaussian
            self.parameters.add_many(('x0', self.x0, True),
                                     ('x_sigma', self.x_sigma, True, 0),
                                     ('A', np.max(self.data) / 2, True),
                                     ('offset', 0, True))
        else:
            self.fitting_function = fitting_function
            self.parameters.add_many(('x0', self.x0, True),
                                     ('x_sigma', self.x_sigma, True, 0))

        # Flat the data into 1D array for fitting
        self.independent_vars_value = {
            'x': self.x,
        }

        # Initialize the fitting model
        super(OneD_Gaussian_fitting, self).__init__(self.data, self.parameters,
                                                    self.fitting_function, self.independent_vars,
                                                    self.independent_vars_value)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def find_start_point(self):
        self.x0_arg = np.argmax(self.data)
        self.x0 = self.x[int(self.x0_arg)]

        data_max = np.max(self.data)
        data_sigma = data_max * np.e ** (-0.5)
        self.x_sigma_arg = self.x0_arg - np.argmax(self.data > data_sigma)
        self.x_sigma = self.x[int(self.x_sigma_arg)]


class TwoD_Gaussian_fitting(FittingFunction.Fitting):

    def __init__(self, data, x, y):
        self.data_origin = data
        self.x_origin = x
        self.y_origin = y
        self.x0 = None
        self.y0 = None
        self.x_sigma = None
        self.y_sigma = None
        self.amplitude = None
        self.offset = None
        self.x0_arg = None
        self.y0_arg = None
        self.x_sigma_arg = None
        self.y_sigma_arg = None

        # Use d4sigma method estimating the start point
        self.find_start_point()

        # Initialize the fitting parameters
        self.parameters = lmfit.Parameters()
        self.independent_vars = ['x', 'y']
        self.fitting_function = FittingFunction.twoD_Gaussian
        self.parameters.add_many(('x0', self.x0, True),
                                 ('y0', self.y0, True),
                                 ('x_sigma', self.x_sigma, True, 0),
                                 ('y_sigma', self.y_sigma, True, 0),
                                 ('A', np.max(self.data_origin) / 2, True),
                                 ('offset', 0, True))

        # Flat the data into 1D array for fitting
        self.data = self.data_origin.flatten()
        self.x, self.y = np.meshgrid(x, y)
        self.x = self.x.flatten()
        self.y = self.y.flatten()
        self.independent_vars_value = {
            'x': self.x,
            'y': self.y,
        }

        # Initialize the fitting model
        super(TwoD_Gaussian_fitting, self).__init__(self.data, self.parameters,
                                                    self.fitting_function, self.independent_vars,
                                                    self.independent_vars_value)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def find_start_point(self):
        self.x0_arg, self.y0_arg, self.x_sigma_arg, self.y_sigma_arg, phi = lbs.beam_size(self.data_origin, max_iter=3)
        self.x_sigma_arg = self.x_sigma_arg / 4
        self.y_sigma_arg = self.y_sigma_arg / 4
        self.x0 = self.x_origin[int(self.x0_arg)]
        self.y0 = self.y_origin[int(self.y0_arg)]
        self.x_sigma = self.x_origin[int(self.x_sigma_arg)]
        self.y_sigma = self.x_origin[int(self.y_sigma_arg)]


class Two_OneD_Gaussian_fitting:

    def __init__(self, data, x, y):
        self.data = data
        self.x = x
        self.y = y
        self.x0 = None
        self.y0 = None
        self.x_sigma = None
        self.y_sigma = None
        self.amplitude = None
        self.offset = None
        self.x0_arg = None
        self.y0_arg = None
        self.x_sigma_arg = None
        self.y_sigma_arg = None
        self.x_max_arg = None
        self.y_max_arg = None

        # Use d4sigma method estimating the start point
        self.find_start_point()

        # Initialize the fitting parameters
        self.fitting_function = FittingFunction.twoD_Gaussian
        self.fitting_x_data = self.data[self.x_max_arg:self.x_max_arg + 1]
        self.fitting_x_data = self.fitting_x_data.flatten()
        self.fitting_y_data = self.data[:, self.y_max_arg:self.y_max_arg + 1]
        self.fitting_y_data = self.fitting_y_data.flatten()
        self.fitting_x = None
        self.fitting_y = None

        # Initialize the fitting result
        self.result = MinimizerResult()
        self.data_fit = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def find_start_point(self):
        # find the position of maximal value in data
        self.x_max_arg, self.y_max_arg = np.unravel_index(np.argmax(self.data), self.data.shape)

    def run_fitting(self):
        self.fitting_x = OneD_Gaussian_fitting(self.fitting_x_data, self.x)
        self.fitting_x.run_fitting()
        self.fitting_y_data = self.fitting_y_data - self.fitting_x.result.best_values['offset']
        self.fitting_y_data = self.fitting_y_data / self.fitting_x.result.best_values['A']
        self.fitting_y = OneD_Gaussian_fitting(self.fitting_y_data, self.y, FittingFunction.oneD_Gaussian_normalized)
        self.fitting_y.run_fitting()

        self.result.best_values = {
            'x0': self.fitting_x.result.best_values['x0'],
            'y0': self.fitting_y.result.best_values['x0'],
            'x_sigma': self.fitting_x.result.best_values['x_sigma'],
            'y_sigma': self.fitting_y.result.best_values['x_sigma'],
            'A': self.fitting_x.result.best_values['A'],
            'offset': self.fitting_x.result.best_values['offset']
        }

    def get_fitting_data(self, data_shape):
        data = self.data.flatten()
        x, y = np.meshgrid(self.x, self.y)
        x = x.flatten()
        y = y.flatten()
        fit_function_kws = {
            'x': x,
            'y': y,
        }
        self.data_fit = self.fitting_function(**fit_function_kws, **self.result.best_values)
        self.data_fit = self.data_fit.reshape(data_shape)

        return self.data_fit
