from setuptools import setup, find_namespace_packages
import sys

from basys4ipps_ifw_agent import VERSION
required = [
    "matplotlib",
    "pyyaml",
    "statsmodels",
    "scipy",
    "scikit-learn",
    "click",
    "tqdm",
    "numpy<=1.22",
    "pandas",
    "graphviz",
    "sympy",
    "pyod",
    "packaging",
    "failure-recognition-signal-processing@git+https://github.com/Gerrino/failure_recognition_signal_processing/#egg=failure-recognition-signal-processing"
]

setup(
    name="basys4ipps_ifw_agent",    
    version=VERSION,
    install_requires=required,
    url="https://github.com/Hendrik2606/BaSys4IPPS_IFW_Agent",
    extras_require={
        "dev": ["pylint", "black", "sphinx"],
    },
    entry_points={"console_scripts": ["basys-agent = cli:main"]},
    py_modules=['basys4ipps_ifw_agent'],
    include_package_data=True
)
# winget install graphviz
