from setuptools import setup, find_namespace_packages
import sys

from basys4ipps_ifw_agent import VERSION
required = [
    "matplotlib",
    "pyyaml",
    "statsmodels",
    "scipy",
    "sklearn",
    "click",
    "tqdm",
    "numpy<=1.22",
    "pandas",
    "graphviz",
    "sympy",
    "pyod",
    "failure-recognition@git+https://github.com/Gerrino/failure-recognition/#egg=failure-recognition"
]

setup(
    name="basys4ipps_ifw_agent",
    packages=find_namespace_packages(include=['failure_recognition.*']),
    version=VERSION,
    install_requires=required,
    url="https://github.com/Hendrik2606/BaSys4IPPS_IFW_Agent",
    extras_require={
        "dev": ["pylint", "black", "sphinx"],
    },
    entry_points={"console_scripts": ["basys-agent = cli:main"]},
    py_modules=['basys4ipps_ifw_agent'],    
)
# winget install graphviz
