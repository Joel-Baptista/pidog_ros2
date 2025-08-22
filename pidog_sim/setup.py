from setuptools import find_packages, setup

package_name = 'pidog_sim'
data_files = []
data_files.append(('share/ament_index/resource_index/packages', ['resource/' + package_name]))
data_files.append(('share/' + package_name + '/launch', ['launch/pidog_launch.py']))
data_files.append(('share/' + package_name + '/worlds', ['worlds/pidog_world.wbt']))
data_files.append(('share/' + package_name + '/resource', ['resource/pidog_world.urdf']))
data_files.append(('share/' + package_name + '/protos', ['protos/PiDog.proto']))
data_files.append(('share/' + package_name + '/pidog_sim', ['pidog_sim/pidog_sim_driver.py']))
data_files.append(('share/' + package_name, ['package.xml']))


setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Joel-Baptista',
    maintainer_email='joelbaptista@ua.pt',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pidog_sim_driver = pidog_sim.pidog_sim_driver:main'
        ],
    },
)
