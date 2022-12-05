from setuptools import setup

setup(name="common",
      version="0.0.2",
      description="A common Python package for whole organization.",
      url="https://github.com/hajle-silesia/common.git",
      py_modules=["common/storage", "common/notifier", "common/utils"],
      install_requires=["requests", "parameterized"]
      )
