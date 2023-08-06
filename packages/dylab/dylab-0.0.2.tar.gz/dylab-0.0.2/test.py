import lyse
from pylab import *
from lyse import *

run = Run(path)

imaging = 'absorption_imaging'
cam = 'absorption_imaging'
h5_paths = lyse.h5_paths()

print(run.globals_groups())

print(run.get_result_arrays(imaging, cam))
