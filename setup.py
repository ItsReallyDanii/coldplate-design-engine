"""Setup script for coldplate-design-engine Stage 1."""

from setuptools import setup, find_packages

setup(
    name="coldplate-design-engine",
    version="0.1.0",
    description="2D cold-plate evaluation engine for Stage 1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.8.0",
        "pyyaml>=5.4",
        "matplotlib>=3.3.0",
        "scikit-image>=0.18.0",
        "pandas>=1.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.12",
        ],
    },
)
