from pathlib import Path

from setuptools import setup

# injected version
__version__ = "v0.0.6"

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="dyff",
    version=__version__,
    description="CLI for interfacing with the Dyff evaluation system",
    keywords="machinelearning testing interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/AlignmentLabs/dyff-cli",
    author="Sean McGregor",
    author_email="pypi@seanbmcgregor.com",
    packages=["dyff"],
    include_package_data=True,
    test_suite="nose2.collector.collector",
    install_requires=["click==8.1", "python-decouple==3.6", "requests==2.28.1"],
    extras_require={"dev": []},
    entry_points={
        "console_scripts": ["dyff=dyff.cli:cli_main"],
    },
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 1 - Planning",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
