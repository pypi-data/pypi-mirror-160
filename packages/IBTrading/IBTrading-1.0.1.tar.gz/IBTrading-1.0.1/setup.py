from setuptools import setup

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    name="IBTrading",
    version="1.0.1",
    description="MT5 automation",
    py_modules=["IBTrading"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = [
        "MetaTrader5 ~= 5.0.37",
    ],
    extras_require={
        "dev":[
            "pytest>=3.7",
        ],
    },
    url="https://github.com/IB-Solution/IBTrading",
    author="Hamidou Alix",
    author_email="alix.hamidou@gmail.com",  
)