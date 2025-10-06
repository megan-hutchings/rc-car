# setup.py

from setuptools import setup, find_packages

setup(
    name="rc_handlers",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "http.client",
    ],
)