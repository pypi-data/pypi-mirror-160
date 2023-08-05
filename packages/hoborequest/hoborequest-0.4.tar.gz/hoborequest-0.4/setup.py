#!/usr/bin/env python3

from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

classifiers = [
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Natural Language :: English",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS",
    "Programming Language :: Python :: 3",
    "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
    "Topic :: Scientific/Engineering",
]

install_requires = [
    "h5py",
    "h5pyd",
    "oauthlib",
    "aiofiles",
    "requests",
    "numpy",
    "cryptography",
    "numcodecs",
    "numpy",
    "psutil",
    "pyjwt",
    "pytz",
    "pyyaml",
]

setup(
    name="hoborequest",
    version="0.4",
    description="HOBOLink API client with HDF5/HSDS integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="environmental-monitoring HDF5 HSDS HOBOLink",
    url="https://gitlab.com/uva-arc/hobo-request",
    author="LF Murillo",
    author_email="lrosadom@nd.edu",
    license="GPLv3",
    packages=["hoborequest", "hoborequest.lib", "hoborequest.tools"],
    package_dir={"": "src"},
    install_requires=install_requires,
    setup_requires=["setuptools"],
    extras_require={},
    zip_safe=False,
    classifiers=classifiers,
    include_package_data=True,
    data_files=[
        (
            "conf",
            [
                "conf/hobo-connect.conf-SAMPLE",
            ],
        )
    ],
    entry_points={
        "console_scripts": [
            "hoboconfig = hoborequest.hoboconfig:main",
            "hoboconnect = hoborequest.hoboconnect:main",
            "checkdups = hoborequest.tools.check_dups:main",
            "check_gaps = hoborequest.tools.check_gaps:main",
            "get_logger_sn = hoborequest.tools.get_logger_sn:main",
            "get_root_attrs = hoborequest.tools.get_root_attrs:main",
            "get_stats = hoborequest.tools.get_stats:main",
        ]
    },
)
