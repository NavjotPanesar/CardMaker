from setuptools import setup, find_packages

def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()

def read_file(file):
   with open(file) as f:
        return f.read()
    
requirements = read_requirements("./requirements.txt")

setup(
    name = 'cardmaker',
    version = "1.0.1",
    author = 'Example',
    author_email = 'example@example.com',
    description = 'A simple example python package.',
    include_package_data = True,
    license = "MIT license",
    packages = find_packages(),
    package_data = {
        '': ['*.png'],
    },
    install_requires = requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)