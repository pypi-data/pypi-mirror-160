from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Works similar to how Vlookup works in Excel'
LONG_DESCRIPTION = 'A package that allows to do Vlookup in different dataframe and intsert the output in the new dataframe'




# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="pypylookup",
        version=VERSION,
        author="CreatorGhost (Aditya Pratap Singh)",
        author_email="<adityapratap2307@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
         install_requires=['pandas'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'Excel', 'Vlookup', 'Lookup', 'dataframe'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
