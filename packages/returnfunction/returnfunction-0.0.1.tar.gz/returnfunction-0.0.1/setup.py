from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Returns a function '
LONG_DESCRIPTION = 'Python implementation of a function that returns a function to be stored inside a variable from returnfunction import rf or import returnfunction'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="returnfunction", 
        version=VERSION,
        author="Jamell Samuels",
        author_email="<jamellsamuels@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'return package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)