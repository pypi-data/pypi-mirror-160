# Functions create constant dictionary storing transition information of Dy.

import scipy.constants as constant
from dylab import TransitionClass


def creat_Dy421():
    wavelength = 421.291e-9

    lifetime = 4.94e-9
    natural_linewidth = 1 / lifetime
    linewidth = natural_linewidth / 2 / constant.pi
    landau_factor = 1.22

    Dy421 = TransitionClass.Transition(wavelength, linewidth, landau_factor)

    return Dy421


def creat_Dy626():
    wavelength = 626.086e-9
    lifetime = 1200e-9
    natural_linewidth = 1 / lifetime
    linewidth = natural_linewidth / 2 / constant.pi
    landau_factor = 1.29

    Dy626 = TransitionClass.Transition(wavelength, linewidth, landau_factor)

    return Dy626