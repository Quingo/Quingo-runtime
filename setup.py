from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="quingo",
    version="0.4.0",
    author="Xiang Fu",
    author_email="gtaifu@gmail.com",
    description="Quingo Runtime System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/quingo/quingo-runtime",
    project_urls={
        "Bug Tracker": "https://gitee.com/quingo/quingo-runtime/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "numpy",
        "scipy",
        "pyqcisim >= 1.3.1",
        "symqc >= 1.1.1",
        "colorama",
        "termcolor",
        "requests",
        "tqdm",
        "pyquiet >= 0.0.4",
        "pycim-simulator"
    ],
    extras_require={
        ':sys_platform == "linux"': [
            "qualesim >= 1.0.2",
            "qualesim-tequila >= 1.0.2",
        ],
    },
)
