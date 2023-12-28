from setuptools import find_packages, setup

requirements = [line.strip() for line in open("requirements.txt").readlines()]

setup(
    name='BCCancerAPI',
    version='1.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
)