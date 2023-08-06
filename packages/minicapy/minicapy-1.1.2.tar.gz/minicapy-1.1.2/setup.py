import shutil
from dataclasses import dataclass
from distutils.util import get_platform
from pathlib import Path
from subprocess import run

from setuptools import setup
from setuptools.command.build_ext import build_ext as BuildCommand

version = "1.1.2"


@dataclass
class MissingDependencyException(Exception):
    dependency: str


class MyBuild(BuildCommand):
    def run(self):
        make = shutil.which("make")
        go = shutil.which("go")

        if not go:
            raise MissingDependencyException("go")
        if not make:
            raise MissingDependencyException("make")

        proc = run([make, "minicapy/minica.dll"], capture_output=True)
        if proc.returncode > 0:
            print(proc.stderr)
            raise Exception

        build_lib = Path(self.build_lib)
        if not build_lib.exists():
            build_lib.mkdir(parents=True)
        self.copy_file(
            "minicapy/minica.dll", str(build_lib / "minicapy" / "minica.dll")
        )


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="minicapy",
    description="Minica python lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer="Bjørn Snoen",
    maintainer_email="bjorn.snoen+minica@gmail.com",
    url="https://github.com/bjornsnoen/minicapy",
    license="GPLv3",
    version=version,
    packages=["minicapy"],
    platforms=[get_platform()],
    package_data={"minicapy": ["minica.dll"]},
    has_ext_modules=lambda: True,
    python_requires=">=3.7",
    cmdclass={"build_ext": MyBuild},
)
