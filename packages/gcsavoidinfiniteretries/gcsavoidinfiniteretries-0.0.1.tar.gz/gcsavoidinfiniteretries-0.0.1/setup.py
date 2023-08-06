from setuptools import setup, find_packages


VERSION = '0.0.1' 
DESCRIPTION = 'Avoid infinite retries Python package'
LONG_DESCRIPTION = 'A Python package for avoiding infinite retries while deploying Google Cloud Functions.'

# Setting up
setup(
        name="gcsavoidinfiniteretries", 
        version=VERSION,
        author="Omar Fateh",
        author_email="fatehomar0@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['python-dateutil'], 
        
        keywords=['python', 'Google Cloud'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)