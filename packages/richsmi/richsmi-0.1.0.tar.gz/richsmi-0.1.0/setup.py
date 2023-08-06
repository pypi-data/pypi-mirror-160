"""setup.py"""

from setuptools import setup
from build import CMakeExtension, CMakeBuild

VERSION = "0.1.0"

with open("README.md") as f:
    long_description = f.read()

with open("requirements.txt") as requirements_file:
    install_requirements = requirements_file.read().splitlines()

setup(
    name="richsmi",
    version=VERSION,
    author="urasaki",
    author_email="urasakikeisuke.ml@gmail.com",
    url='https://github.com/urasakikeisuke/richsmi',
    description="A terminal based graphical GPU monitoring tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    ext_modules=[CMakeExtension("librichsmi")],
    cmdclass={"build_ext": CMakeBuild},
    zip_safe=False,
    python_requires=">=3.8",
    license="MIT",
    install_requires=install_requirements,
    packages=["librichsmi", "richsmi"],
    package_data={
        "librichsmi": ["py.typed", "*.pyi"],
    },
    entry_points={
        "console_scripts": [
            "richsmi=richsmi.richsmi:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
