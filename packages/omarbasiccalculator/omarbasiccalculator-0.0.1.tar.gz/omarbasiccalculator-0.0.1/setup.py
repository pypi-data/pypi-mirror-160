from setuptools import setup, find_packages


VERSION = '0.0.1' 
DESCRIPTION = 'Basic calculator Python package'
LONG_DESCRIPTION = 'A Python package for calculating numbers.'

# Setting up
setup(
       # the name must match the folder name 'basiccalculator'
        name="omarbasiccalculator", 
        version=VERSION,
        author="Omar Fateh",
        author_email="fatehomar0@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'calculator package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)