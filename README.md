# edgetpuvision

Python API to run inference on image data coming from the camera.

## Build

python3 setup.py sdist
python3 setup.py bdist
python3 setup.py sdist_wheel

## Debian pacakge

To build debian pacakge run:
```
dpkg-buildpackage -b -rfakeroot -us -uc -tc
```
To run detect_server.py

export TEST_DATA="$HOME/lockedin/test_data"
python3 -m edgetpuvision.detect_server \
--model ${TEST_DATA}/ssd_mobilenet_v2_face_quant_postprocess_edgetpu.tflite
