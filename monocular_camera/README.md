# Monocular Camera Pkg

## To Calibrate Camera:

First launch camera node:
'''
roslaunch blurov_launch camera.launch
'''

Then run calibration script:
'''
rosrun camera_calibration cameracalibrator.py --size 6x8 --square 0.073 image:=/camera/image_raw camera:=/camera --no-service-check
'''

- calibrate
- save

Calibration files will be saved to: /tmp/calibration.data.tar.gz

Copy and past content from ost.yaml to monocular_camera/config/calibration.yaml

## Rectifying Image
roslaunch monocular_camera rectification.launch