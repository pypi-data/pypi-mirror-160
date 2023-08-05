import os
import io
from setuptools import setup, find_packages


# Import the README and use it as the long-description.
here = os.path.abspath(os.path.dirname(__file__))
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = 'Classify the name based on given name.'

setup(name='GenderPrediction',  # This is the name of your PyPI-package.
      version='3.0.1',  # Update the version number for new releases
      description='Classify the name based on given name',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Sounak-Mukherjee',
      author_email='sounak@pratilipi.com',
      license='MIT',
      packages=['GenderPrediction'],
      include_package_data=True,
      install_requires=['numpy==1.19.2', 'tensorflow-cpu==2.5.0']
      )
