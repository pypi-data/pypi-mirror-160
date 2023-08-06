import io
from os.path import abspath, dirname, join
from setuptools import find_packages, setup


HERE = dirname(abspath(__file__))
LOAD_TEXT = lambda name: io.open(join(HERE, name), encoding='UTF-8').read()
DESCRIPTION = '\n\n'.join(LOAD_TEXT(_) for _ in [
    'README.rst'
])

setup(
  name = 'lazyemployee',                # Name project the same with folder
  packages = ['lazyemployee'],          # Name project the same with folder
  version = '0.0.5',                 # 
  license='MIT', 
  description = 'lazyemployee learning to upload to PyPI',    #Show on PyPi
  long_description=DESCRIPTION,
  author = 'Tun Kedsaro',            #          
  author_email = 'Tun.k@ku.th',      #
  url = 'https://github.com/Tun555/Lazyemployee',  #
  download_url = 'https://github.com/Tun555/Lazyemployee/archive/refs/tags/v0.0.2.zip',                                      #  
  keywords = ['OOP','Employee'],      # When someone search
  install_requires=[                 # Package that use
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