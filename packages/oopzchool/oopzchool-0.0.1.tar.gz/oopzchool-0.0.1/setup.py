import io
from os.path import abspath, dirname, join
from setuptools import find_packages, setup


HERE = dirname(abspath(__file__))
LOAD_TEXT = lambda name: io.open(join(HERE, name), encoding='UTF-8').read()
DESCRIPTION = '\n\n'.join(LOAD_TEXT(_) for _ in [
    'README.rst'
])

setup(
  name = 'oopzchool',      # Name the same with folder
  packages = ['oopzchool'], 
  version = '0.0.1',  
  license='MIT', 
  description = 'OOPzchool learning to upload to PyPI',    #Show on PyPi
  long_description=DESCRIPTION,
  author = 'Tun Kedsaro',                 
  author_email = 'Tun.k@ku.th',     
  url = 'https://github.com/Tun555/zchool',  
  download_url = 'https://github.com/Tun555/zchool/archive/refs/tags/v0.0.1.zipp',  
  keywords = ['OOP', 'zhcool', 'Tun'], 
  install_requires=[            # I get to this in a second
        'numpy',
        'matplotlib',
    ],  
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Developers',   
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Version pathon that we test 
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)