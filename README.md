
Current process of creating PiDog:

1. Draw parts in FreeCAD and exporting the .dae files. The parts were all assembled inside FreeCAD to verify relative dimensions.
2. Utilized blender to correct some deviations in the meshes (e.g. CoM deviation from the (0,0,0))
3. Creating URDF of robot
4. Using [urdf2webots](https://github.com/cyberbotics/urdf2webots) converted.
```bash
python -m urdf2webots.importer --input=urdf/pidog.urdf --output=proto/ --normal --init-pos="[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]" 
```
