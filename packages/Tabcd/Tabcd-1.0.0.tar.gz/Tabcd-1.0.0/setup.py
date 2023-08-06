from distutils.core import setup
from setuptools import find_packages

with open("README.rst","r")as f:
    long_description=f.read()

setup(name="Tabcd",
      version="1.0.0",
      description="A small example package",
      long_description=long_description,
      author="wl",
      author_email="3022949584@qq.com",
      url="https://mp.weixin.qq.com/s",
      install_requires=[],
      license="DBC License",
      packages=find_packages(),
      platforms=["all"])

