from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="pyzooms2s",
    version="0.1.2",
    author="Michael Ralston",
    author_email="michaelaaralston2@gmail.com",
    description="Zoom Python Server-to-Server OAuth SDK",
    license="MIT",
    url="https://github.com/MikeRalston98/pyzooms2s",
    keywords=["Zoom", "Server-To-Server"],
    packages=["pyzooms2s"],
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)