# A self defined constant dictionary class
# It is used for storing the physical constant related to transition
import numpy as np
import scipy.constants as constant


class Transition(dict):
    class ConstError(TypeError):
        pass

    def __setitem__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't change const %s" % name)
        super().__setitem__(name, value)
        self.__dict__[name] = value

    def __getattr__(self, name):
        return self[name]

    def __dir__(self):
        return sorted(self)

    def __init__(self, wavelength, linewidth, landauFactor):
        super().__init__()

        wavevector = 2 * constant.pi / wavelength
        frequency = constant.speed_of_light / wavelength
        circular_frequency = 2 * constant.pi * frequency
        natural_linewidth = 2 * constant.pi * linewidth
        lifetime = 1 / natural_linewidth
        saturation_intensity = 2 * constant.pi ** 2 / 3 * \
                               constant.hbar * constant.c * natural_linewidth / wavelength ** 3

        resonance_cross_section = constant.hbar * circular_frequency * \
                                  natural_linewidth / 2 / saturation_intensity

        self['wavelength'] = wavelength
        self['wavevector'] = wavevector
        self['frequency'] = frequency
        self['circular_frequency'] = circular_frequency
        self['linewidth'] = linewidth
        self['natural_linewidth'] = natural_linewidth
        self['landauFactor'] = landauFactor
        self['lifetime'] = lifetime
        self['saturation_intensity'] = saturation_intensity
        self['resonance_cross_section'] = resonance_cross_section

    def get_rabi_frequency(self, intensity):
        rabi_frequency = np.sqrt(intensity / self['saturation_intensity'] / 2) * self['natural_linewidth']

        return rabi_frequency

    def get_cross_section(self, detuning, intensity):

        cross_section = self['resonance_cross_section'] / (
                1 + 4 * (detuning / self['natural_linewidth']) ** 2 + intensity / self['saturation_intensity'])
        return cross_section
