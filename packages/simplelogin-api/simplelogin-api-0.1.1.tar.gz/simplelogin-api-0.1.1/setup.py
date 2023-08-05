from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='simplelogin-api',
    version='0.1.1',
    author="vixfwis",
    description="SimpleLogin API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vixfwis/simplelogin-api",
    packages=find_packages(),
    install_requires=[
        'attrs==21.4.0',
        'certifi==2021.10.8',
        'charset-normalizer==2.0.12',
        'idna==3.3',
        'iniconfig==1.1.1',
        'packaging==21.3',
        'pluggy==1.0.0',
        'py==1.11.0',
        'pyparsing==3.0.8',
        'pytest==7.1.1',
        'requests==2.27.1',
        'schematics==2.1.1',
        'tomli==2.0.1',
        'urllib3==1.26.9',
    ]
)
