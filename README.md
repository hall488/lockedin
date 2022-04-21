# edgetpuvision

Python API to run inference on image data coming from the camera.

## Model
```
wget -P ${TEST_DATA}/ https://github.com/google-coral/test_data/raw/master/ssd_mobilenet_v2_face_quant_postprocess_edgetpu.tflite
```

## Build
```
cd ..
cd ..
cd mnt
cd home
cd mendel
cd lockedin
export TEST_DATA="test_data"
sudo mkfs.ext4 /dev/mmcblk1
sudo mount /dev/mmcblk1 /mnt
sudo rsync -aXS --exclude='/*/.gvfs' /home  /mnt
sudo diff -r /home /mnt/home -x ".gvfs/*"
sudo chown -R mendel:mendel /mnt/home/mendel
sudo echo " /dev/mmcblk1 /home ext4 defaults 0 1" >> /etc/fstab
sudo fallocate -l 10G /home/swapfile
sudo chmod 600 /home/swapfile
sudo mkswap /home/swapfile
sudo swapon /home/swapfile
sudo sysctl vm.swappiness=10
python3 setup.py sdist
python3 setup.py bdist
export FLASK_ENV=development
python3 -m edgetpuvision.detect \
--source /dev/video1:YUY2:1024x768:15/1  \
--model ${TEST_DATA}/ssd_mobilenet_v2_face_quant_postprocess_edgetpu.tflite

```

## Debian pacakge

To build debian pacakge run:
```
dpkg-buildpackage -b -rfakeroot -us -uc -tc
```
To run detect_server.py

```

```
```
python3 -m edgetpuvision.detect_server \
--model ${TEST_DATA}/ssd_mobilenet_v2_face_quant_postprocess_edgetpu.tflite
```
```
python3 -m edgetpuvision.detect \
--source /dev/video1:YUY2:1024x768:15/1  \
--model ${TEST_DATA}/ssd_mobilenet_v2_face_quant_postprocess_edgetpu.tflite
```
