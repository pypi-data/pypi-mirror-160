from setuptools import setup, find_packages

setup(name="pymzl",
      version="0.0.6",
      description="calculation",
      py_modules={"pymzl"},
      package_dir={"":"."},
      url="https://github.com/ZiluM/uti",
      download_url="https://github.com/ZiluM/uti/archive/refs/tags/pymzl_0.03.tar.gz",
      author="Zilu Meng",
      author_email="mzll1202@163.com",
      install_requires=["numpy"
      ],
      packages=find_packages(),
      license="MIT")
