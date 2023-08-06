from setuptools import setup, find_packages

with open(
 '/home/horvat/VIPCOAT/Gitlab-OIP/testing/packaging_modena/requirements.txt',
 'r'
 ) as f:
    required = f.read().splitlines()

with open(
 '/home/horvat/VIPCOAT/Gitlab-OIP/testing/packaging_modena/README.md',
 'r'
 ) as f:
    long_description = f.read()

print(required)

setup(    
    name='modena',
    version='0.0.1',
    description='Simulation framework application facilitating\
     simulation of interconnected models',
    packages=find_packages(),
    install_requires=required,
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown"
)
