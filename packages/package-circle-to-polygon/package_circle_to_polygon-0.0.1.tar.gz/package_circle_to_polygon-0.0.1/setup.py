from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as f:
  long_description = f.read()

setup(name='package_circle_to_polygon',
      version='0.0.1',
      description='A small example package',
      long_description=long_description,
      author='leihb',
      author_email='leihaibo1992@gmail.com',
      install_requires=[],
      license='MIT License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.10',
          'Topic :: Software Development :: Libraries'
      ],
      )
