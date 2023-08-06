from lyse import *
from pylab import *
import numpy as np
import scipy.constants as constant
from dylab import DyTransition, Camera
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import colorsys


# Produce the jet colormap
def man_cmap(cmap, value=1.):
    colors = cmap(np.arange(cmap.N))
    hls = np.array([colorsys.rgb_to_hls(*c) for c in colors[:, :3]])
    hls[:, 1] *= value
    rgb = np.clip(np.array([colorsys.hls_to_rgb(*c) for c in hls]), 0, 1)
    return mcolors.LinearSegmentedColormap.from_list("", rgb)


class absorption_imaging:
    image_name = {
        'atoms': 'atoms',
        'background': 'background',
        'dark': 'dark'
    }

    class CameraError(TypeError):
        pass

    class TransitionError(TypeError):
        pass

    class IntensityError(TypeError):
        pass

    def __init__(self, data_path, camera_orientation, camera_label, transition=None, camera=None, detuning=None,
                 intensity=None):
        self.path = data_path

        # Ideally, we should be able to access all the data by function data(path).
        # However it is still under development. Now we can not read a picture by using function data(path).
        # We have to change to use function Run(path), which creat a class with the saved hdf5 file.
        self.data_handle = Run(data_path)

        # Path of the saving images
        self.camera_orientation = camera_orientation
        self.camera_label = camera_label

        # Two dimensional array storing the images
        self.image_atoms = None
        self.image_background = None
        self.image_dark = None
        self.image_absorption = None

        #
        self.image_absorption_cut = None
        self.x_start = None
        self.y_start = None
        self.x_end = None
        self.y_end = None

        # import the data of transition
        # The transition should be an object of TransitionClass.py in module TransitionConstant
        # self.transition = transition

        self.detuning = detuning

        # Camera information
        # The Camera should be an object of Camera class in module Camera
        # self.camera = camera
        self.intensity = intensity

        self.beam_energy = None
        self.atom_number = None

        # For debuging
        self.transition = DyTransition.creat_Dy421()
        self.camera = Camera.c11440_36u(self.transition['wavelength'])

    def __enter__(self):
        self.get_image_absorption()
        self.get_atom_number()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def set_image_name(self, image, name):
        self.image_name[image] = name

    def open(self):
        self.image_atoms = self.data_handle.get_image(self.camera_orientation, self.camera_label,
                                                      self.image_name['atoms'])
        self.image_background = self.data_handle.get_image(self.camera_orientation, self.camera_label,
                                                           self.image_name['background'])
        self.image_dark = self.data_handle.get_image(self.camera_orientation, self.camera_label,
                                                     self.image_name['dark'])

        self.image_atoms = self.image_atoms.astype(float)
        self.image_background = self.image_background.astype(float)
        self.image_dark = self.image_dark.astype(float)

    def close(self):
        self.save()

    def save(self):
        if self.image_absorption is not None:
            self.data_handle.save_result_array('absorption_imaging', self.image_absorption,
                                               'results/absorption_imaging/')
        if self.atom_number is not None:
            self.data_handle.save_result('atom_number', self.atom_number, 'results/absorption_imaging/')

    # select the effective data in an rectangle area defined by coordinates of two conner
    # The select region will be presented as a red box in the plotting
    def select_effective_data(self, left_up_conner, right_down_conner):

        self.x_start = left_up_conner[0]
        self.x_end = right_down_conner[0]
        self.y_start = left_up_conner[1]
        self.y_end = right_down_conner[1]

        self.image_absorption_cut = self.image_absorption[self.y_start:self.y_end, self.x_start:self.x_end]

        return self.image_absorption_cut

    # The function do the analyzation for absorption imaging
    # It will return a two-dimensional array, which stores the absorption imaging
    def get_image_absorption(self):
        # import three pictures from hfd5 data file
        self.open()

        self.image_absorption = np.ones(shape(self.image_atoms))

        numerator = self.image_background - self.image_dark
        denominator = self.image_atoms - self.image_dark

        numerator[numerator <= 0] = 1
        denominator[denominator <= 0] = 1
        self.image_absorption = numerator / denominator
        self.image_absorption = np.log(self.image_absorption)

        # OD_means = np.log(imagine_absorption)
        # OD_sat = 0
        # OD_mod = np.log((1 - constant.e**-OD_sat) / (constant.e**-OD_means - constant.e**-OD_sat))
        # OD_act = OD_mod + (1 - constant.e**OD_mod) * self.intensity / self.transition['saturation_intensity']
        # self._imagine_absorption = constant.e**OD_act

        return self.image_absorption

    def get_beam_power(self, laser_pulse_duration):
        if self.beam_energy is None:
            self.beam_energy = self.image_background - self.image_dark
            self.beam_energy[self.beam_energy < 0] = 0
            self.beam_energy = self.camera.reading2photon(self.image_background - self.image_dark)
            self.beam_energy = self.beam_energy * constant.h * self.transition['frequency']
            self.beam_energy = np.sum(self.beam_energy)

        return self.beam_energy / laser_pulse_duration

    def get_atom_number(self, force_to_run=False):

        if self.camera is None:
            raise self.CameraError("No camera information")

        if self.transition is None:
            raise self.TransitionError("No transition information")

        if self.intensity is None:
            raise self.IntensityError("No beam intensity information")

        if self.atom_number is not None and not force_to_run:
            return self.atom_number

        if self.image_absorption is None or not force_to_run:
            self.image_absorption = self.get_image_absorption()

        if self.image_absorption_cut is None:
            self.image_absorption_cut = self.image_absorption
            self.x_start = 0
            self.x_end = self.image_absorption.shape[1]
            self.y_start = 0
            self.y_end = self.image_absorption.shape[0]

        OD_act = self.image_absorption_cut

        cross_section = self.transition.get_cross_section(self.detuning, self.intensity)

        self.atom_number = np.sum(1 / cross_section * OD_act) * self.camera['pixel_size_V'] * self.camera[
            'pixel_size_H']

        return self.atom_number

    # Plot the result
    def plot_result(self, vmin=None, vmax=None):

        cmap = plt.cm.get_cmap("jet")

        grid = plt.GridSpec(3, 3, wspace=0.3, hspace=0.3)

        ax1 = plt.subplot(grid[0, 0])
        pos = ax1.imshow(self.image_atoms, cmap=cmap)
        ax1.set_title('With atoms')
        plt.colorbar(pos, ax=ax1)

        ax2 = plt.subplot(grid[1, 0])
        pos = ax2.imshow(self.image_background, cmap=cmap)
        ax2.set_title('Without atoms')
        plt.colorbar(pos, ax=ax2)

        ax3 = plt.subplot(grid[2, 0])
        pos = ax3.imshow(self.image_dark, cmap=cmap)
        ax3.set_title('Dark')
        plt.colorbar(pos, ax=ax3)

        ax4 = plt.subplot(grid[0:2, 1:3])
        pos = ax4.imshow(self.image_absorption, cmap=cmap, vmin=vmin, vmax=vmax)
        ax4.set_title('Absorption Imaging')
        plt.colorbar(pos, ax=ax4)
        ax4.plot([self.x_start, self.x_start], [self.y_start, self.y_end], color='black')
        ax4.plot([self.x_end, self.x_end], [self.y_start, self.y_end], color='black')
        ax4.plot([self.x_start, self.x_end], [self.y_start, self.y_start], color='black')
        ax4.plot([self.x_start, self.x_end], [self.y_end, self.y_end], color='black')

        ax5 = plt.subplot(grid[2:3, 1:3])
        atom_number_str = '{:g}'.format(self.atom_number)
        ax5.text(0, 0.55, 'Atom Number : '+atom_number_str, horizontalalignment='left', verticalalignment='center',
                 transform=ax5.transAxes, fontsize=40)
        plt.axis('off')

        plt.show()
