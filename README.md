
Current process of creating PiDog:

1. Draw parts in FreeCAD and exporting the .dae files. The parts were all assembled inside FreeCAD to verify relative dimensions.
2. Utilized blender to correct some deviations in the meshes (e.g. CoM deviation from the (0,0,0))
3. Creating URDF of robot
4. Using [urdf2webots](https://github.com/cyberbotics/urdf2webots) converted.
```bash
python -m urdf2webots.importer --input=urdf/pidog.urdf --output=proto/ --normal --init-pos="[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]" 
```

## Installation

- <https://docs.sunfounder.com/projects/pidog/en/latest/python/python_start/install_all_modules.html>

### install tool

```bash
sudo apt install git python3-pip python3-setuptools python3-smbus
```

### robot-hat library

```bash
cd ~/
git clone -b v2.0 https://github.com/sunfounder/robot-hat.git
cd robot-hat
sudo python3 setup.py install

```

### vilib library

```bash
cd ~/
git clone -b picamera2 https://github.com/sunfounder/vilib.git
cd vilib
sudo python3 install.py
```

### pidog library

```bash
cd ~/
git clone https://github.com/sunfounder/pidog.git
cd pidog
sudo python3 setup.py install
```

### i2samp

```
cd ~/pidog
sudo bash i2samp.sh
```

----------------------------------------------