# edgetpuvision

Python API to run inference on image data coming from the camera.

## Model
```
wget -P ${TEST_DATA}/ https://github.com/google-coral/test_data/raw/master/ssd_mobilenet_v2_face_quant_postprocess_edgetpu.tflite
```

## Build
```
python3 setup.py sdist
python3 setup.py bdist
```

## Debian pacakge

To build debian pacakge run:
```
dpkg-buildpackage -b -rfakeroot -us -uc -tc
```
To run detect_server.py

```
export TEST_DATA="$MNT/home/mendel/lockedin/test_data"
```
```
python3 -m edgetpuvision.detect_server \
--model ${TEST_DATA}/ssd_mobilenet_v2_face_quant_postprocess_edgetpu.tflite
```
```
python3 -m edgetpuvision.detect \
--model ${TEST_DATA}/ssd_mobilenet_v2_face_quant_postprocess_edgetpu.tflite
```
