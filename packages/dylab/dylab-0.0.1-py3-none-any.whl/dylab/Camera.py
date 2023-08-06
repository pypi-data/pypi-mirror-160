class c11440_36u(dict):
    class ConstError(TypeError):
        pass

    class DataError(TypeError):
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

    def __init__(self, wavelength):
        super().__init__()
        self['pixel_size_V'] = 5.8e-6
        self['pixel_size_H'] = 5.8e-6
        self['pixel_num_H'] = 1920
        self['pixel_num_v'] = 1200

        # Measured quantum efficiency @ 421nm
        # original measurement data is in our shared folder for data
        # Data\Measurements\2022\05\23\camera\qe\
        if 420e-9 < wavelength < 422e-9:
            self['quantum_efficiency'] = 0.639714338817604
            self['quantum_efficiency_std'] = 0.021405684133816

        # Measured quantum efficiency @ 626nm
        # original measurement data is in our shared folder for data
        # Data\Measurements\2022\05\24\camera\qe_626\
        if 625e-9 < wavelength < 627e-9:
            self['quantum_efficiency'] = 0.516529105247143
            self['quantum_efficiency_std'] = 0.023114728382457

        if self['quantum_efficiency'] is None:
            raise self.DataError("Lack for quantum efficiency data at specified wavelength")

        self['full_well_capacity'] = 33000
        self['reading_to_electron'] = self['full_well_capacity'] / 4095
        self['electron_to_reading'] = 4095 / self['full_well_capacity']
        self['reading_to_photon'] = self['quantum_efficiency'] * self['reading_to_electron']
        self['photon_to_reading'] = self['electron_to_reading'] / self['quantum_efficiency']
        self['noise_RMS'] = 6.6
        self['noise_RMS_measure'] = 6.458

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    # A function convert the setting value of analog gain to amplification factor in times
    def analog_gain_factor(self, setting_value):
        return 10**(setting_value * 0.1 / 20)

    def reading2electron(self, reading_value):
        return reading_value * self['reading_to_electron']

    def electron2reading(self, electron_num):
        return electron_num * self['electron_to_reading']

    def reading2photon(self, reading_value):
        return reading_value * self['reading_to_photon']
