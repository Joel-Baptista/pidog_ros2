from setuptools import find_packages, setup

package_name = 'pidog_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Joel-Baptista',
    maintainer_email='joelbaptista@ua.pt',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pidog_gait_control = pidog_control.pidog_gait_control:main'
        ],
    },
)
