from lyse import *
from dylab import DyTransition, Camera, AbsorptionImaging


absorption_imaging_transition = DyTransition.creat_Dy421()
mot_3D_camera = Camera.c11440_36u(absorption_imaging_transition['wavelength'])

with AbsorptionImaging.absorption_imaging(path, 'MOT_3D_Camera', 'in_situ_absorption',
                                          absorption_imaging_transition, mot_3D_camera, 0, 0) as absorption_image:

    absorption_image.select_effective_data((800, 500), (1000, 700))
    absorption_image.plot_result(-0.05, 0.05)

    print(absorption_image.atom_number)
