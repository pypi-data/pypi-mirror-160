from setuptools import setup, find_packages

setup(name='GenderPrediction',  # This is the name of your PyPI-package.
      version='2.0.2',  # Update the version number for new releases
      description='Classify the name based on given name',
      author='Sounak-Mukherjee',
      author_email='sounak@pratilipi.com',
      license='MIT',
      packages=['GenderPrediction'],
      include_package_data=True,
      install_requires=['numpy==1.19.2', 'tensorflow-cpu==2.5.0']
      )
