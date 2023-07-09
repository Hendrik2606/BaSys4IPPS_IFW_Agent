from setuptools import setup, find_namespace_packages
import sys
required = ['sklearn', 'click', 'tqdm', 'numpy', 'pandas', 'graphviz', 'sympy']

setup(
    name='basys4ipps-ifw-agent',  
    install_requires=required,
    extras_require = {
       'dev': ['pylint', 'black', 'sphinx'],     
   }
)
#winget install graphviz