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
    packages=find_packages(),
    install_requires=[
        "fastapi==0.52.0",
        "dynaconf[yaml]==2.2.3",
        "uvicorn==0.11.3",
        "loguru==0.4.1",
        "asyncpg==0.20.1",
        "sqlalchemy==1.3.15",
        "psycopg2-binary==2.8.4",
        "httpx==0.12.1",
        "packaging==20.3",
        "stdlib-list>=0.6.0",
        "email-validator==1.0.5",
    ],
    extras_require={
        "dev": [
            "coverage==4.5.1",
            "mccabe==0.6.1",
            "tox==3.0.0",
            "requests==2.23.0",
            "httpx==0.12.1",
        ],
        "test": ["requests==2.23.0"],
    },
    python_requires=">=3.7.*, <4",
)
