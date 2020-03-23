from setuptools import find_packages, setup
from pypis import __version__

with open("README.md") as f:
    readme = f.read()


setup(
    name="pypis",
    version=__version__,
    description="Pypi secure server",
    long_description=readme,
    author="jurelou",
    author_email="louis@jurczyk.fr",
    url="https://github.com/jurelou/pypis",
    install_requires=[
        "fastapi  >= 0.52.0",
        "dynaconf[yaml] >= 2.2.3",
        "uvicorn  >= 0.11.3",
        "loguru   >= 0.4.1",
        "asyncpg  >= 0.20.1"
    ],
    extras_require={
        "test" : [
        "coverage==4.5.1",
        "isort==4.3.4",
        "mccabe==0.6.1",
        "pyflakes==2.0.0",
        "flake8",
        "pytest",
        "tox==3.0.0",
        ]
    },
    python_requires=">=3.7.*, <4",
)
