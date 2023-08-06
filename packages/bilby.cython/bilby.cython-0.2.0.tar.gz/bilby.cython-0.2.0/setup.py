import os
import subprocess
import sys

import numpy as np
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext


python_version = sys.version_info
min_python_version = (3, 8)
min_python_version_str = f"{min_python_version[0]}.{min_python_version[1]}"
if python_version < min_python_version:
    sys.exit(f"Python < {min_python_version_str} is not supported, aborting setup")


class LazyImportBuildExtCmd(build_ext):
    def finalize_options(self):
        from Cython.Build import cythonize

        compiler_directives = dict(
            language_level=3,
            boundscheck=False,
            wraparound=False,
            cdivision=True,
            initializedcheck=False,
            embedsignature=True,
        )
        if os.environ.get("CYTHON_COVERAGE"):
            compiler_directives["linetrace"] = True
            annotate = True
        else:
            annotate = False
        self.distribution.ext_modules = cythonize(
            self.distribution.ext_modules,
            compiler_directives=compiler_directives,
            annotate=annotate,
        )
        super(LazyImportBuildExtCmd, self).finalize_options()


def write_version_file(version):
    """Writes a file with version information to be used at run time

    Parameters
    ----------
    version: str
        A string containing the current version information

    Returns
    -------
    version_file: str
        A path to the version file

    """
    try:
        git_log = subprocess.check_output(
            ["git", "log", "-1", "--pretty=%h %ai"]
        ).decode("utf-8")
        git_diff = (
            subprocess.check_output(["git", "diff", "."])
            + subprocess.check_output(["git", "diff", "--cached", "."])
        ).decode("utf-8")
        if git_diff == "":
            git_status = "(CLEAN) " + git_log
        else:
            git_status = "(UNCLEAN) " + git_log
    except Exception as e:
        print(f"Unable to obtain git version information, exception: {e}")
        git_status = "release"

    version_file = ".version"
    long_version_file = f"bilby_cython/{version_file}"
    if os.path.isfile(long_version_file) is False:
        with open(long_version_file, "w+") as f:
            f.write(f"{version}: {git_status}")

    return version_file


def get_long_description():
    """Finds the README and reads in the description"""
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, "README.md")) as f:
        long_description = f.read()
    return long_description


VERSION = "0.2.0"
version_file = write_version_file(VERSION)

if os.environ.get("CYTHON_COVERAGE"):
    macros = [
        ("CYTHON_TRACE", "1"),
        ("CYTHON_TRACE_NOGIL", "1"),
    ]
else:
    macros = list()
extensions = [
    Extension(
        "bilby_cython.geometry",
        ["bilby_cython/geometry.pyx"],
        include_dirs=[np.get_include()],
        define_macros=macros,
    ),
]

setup(
    author="Colm Talbot",
    author_email="colm.talbot@ligo.org",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    cmdclass={"build_ext": LazyImportBuildExtCmd},
    description="Optimized functionality for Bilby",
    ext_modules=extensions,
    install_requires=["numpy", "lalsuite"],
    license="MIT",
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    name="bilby.cython",
    packages=["bilby_cython"],
    package_data=dict(bilby_cython=["*.pyx"]),
    python_requires=f">={min_python_version_str}",
    setup_requires=["numpy", "cython", "setuptools_scm"],
    url="https://git.ligo.org/colm.talbot/bilby-cython",
    use_scm_version={
        "write_to": "bilby_cython/_version.py",
        "local_scheme": "dirty-tag",
    },
)
