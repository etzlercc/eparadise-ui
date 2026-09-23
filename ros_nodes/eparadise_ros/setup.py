from setuptools import setup

package_name = 'eparadise_ros'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='eParadise',
    maintainer_email='dev@localhost',
    description='HTTP gateway for Odoo commands and ROS 2 integration.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'eparadise_gateway = eparadise_ros.__main__:main',
        ],
    },
)
