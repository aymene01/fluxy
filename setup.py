from requests import packages
from setuptools import setup, find_packages

setup(
    name="dags",
    packages=find_packages(where="dags"),
    package_dir={"": "dags"},
    packages_data={"dags": ["py.typed"]},
)
