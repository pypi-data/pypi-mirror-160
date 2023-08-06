from distutils.core import setup
with open("README.md", "r",encoding='UTF-8') as f:
  long_desc = f.read()

setup(name='shijie',
      version='1.3',
      description='Secuer: ultrafast, scalable and accurate clustering of single-cell RNA-seq data',
      author='nnwei',
      long_description=long_desc,
      url='https://github.com/nanawei11/Secuer',
      packages=['secuer'],
      license='MIT',
      entry_points={
            'console_scripts': ['secuer = secuer_console.console:main']}# linux
      )

