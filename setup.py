from setuptools import setup, find_namespace_packages
import sys

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
    "pyod"
]

setup(
    name="basys4ipps-ifw-agent",
    install_requires=required,
    extras_require={
        "dev": ["pylint", "black", "sphinx"],
    },
    entry_points={"console_scripts": ["basys-agent = cli:main"]},
)
# winget install graphviz
