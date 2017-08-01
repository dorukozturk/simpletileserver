from setuptools import setup

setup(name='simple-tile-server',
      version='0.0',
      description='Minimalistic tile server to inspect geospatial files',
      url='https://gitlab.com/dorukozturk/simple-tile-server',
      author='Doruk Ozturk',
      author_email='doruk.ozturk@kitware.com',
      license='Apache 2.0',
      packages=['simpletileserver'],
      zip_safe=False,
      entry_points={
          'console_scripts': [
              "simple-tile-server=simpletileserver.cli:main"
          ]
      }
)
