from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.4'
DESCRIPTION = 'Converts py to ipynb and vice versa, also syncs them'

# Setting up
setup(
    name="py2ipynb2py",
    version=VERSION,
    author="harshit5674 (Harshit Verma)",
    author_email="<verma08harshit@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
	long_description="""# Py2ipynb2Py

__py2ipynb2py__ is a python module which aims to bridge the gap between Python scripts and Python notebooks by letting the user convert .py to .ipynb and vice versa and lets the user keep both the files in sync.

# Why use it

Python notebooks and scripts serve almost the same function that is running python code, yet they appear to be such different entities with different pros and cons.

## Jupyter notebooks disadvantages
* __Dependencies__ -> In some cases, the notebook imports libraries that are only installed on the computer of a data analyst (locally). The issue with such a scenario is that a programmer using a different version of the same library, such as NumPy, may experience the setback of the actual 
production calculations not agreeing with those in the research.
* __Object Oriented Paradigm__ -> Difficult to follow using notebooks
* Not possible to reproduce the outcomes from Jupyter Notebook received from a local execution.
* Cannot give a definite structure we can give by maintaining scripts
* Notebook results performed by one machine might differ when running on another computer in the same group bearing in mind that the machines might have some caching differences.

## Jupyter notebook Advantages
* You can execute the code and see the magic instantly.
* You can run cells independently and see several outputs without running all of the program.
* Easy and coonvinient to use.

With py2ipynb2py you can easily convert .py to .ipynb and vice versa, it also then keeps both the files in sync. Markdows are preserved, i.e. even if your jupyter notebook has images these are conserved when you convert it to .py and that .py file is compilable even while maintaining all the markdowns. You can even add markdows in python files using py2ipynb2py's special syntax.

While the famouse nbconvert library lets you convert .ipynb to .py, it does not let you convert .py to .ipynb and there is no feature to keep both the file in sync and maintainble.

# Installation
```
pip3 install py2ipynb2py
```

# Documentation
When writing you python script if you leave a blank between two lines those two lines will be in __different cells__.

First __import__ py2ipynb2py
```
import py2ipynb2py
```
then add the following function
```
py2ipynb2py.convertor('PATH_OF_FILE')
```
__Note that__
* __PATH_OF_FILE__ represents path of your notebook or script.
* One just has to add this path to only one time either to you notebook or script, when you convert the respective one time it automatically takes care of the path.
* __Windows Users__ when adding path use '\\\\' instead of '\\'

One can add this function anywhere in his/her program.

## Markdown

Whenever one wants to do markdown in his/her python script
Use
```
'''--Markdown--
Whatever you want to 
write in the markdown.
--Markdown--'''
```

Note that this will also be the syntax when a markdown in converted from .ipynb to .py.

One additional feature of Notebooks is you can just write variable name at the end of the cell and it will print the value of that variable, this does not serve any purpose in the python script, so these would be removed during conversion.

__Just Remember to SAVE the file before running it for the purpose of conversion.__""",
    long_description_content_type='text/markdown',
    keywords=['python','jupyter','convertor','python to jupyter notebook','jupyter notebook to python'],
    classifiers=[
	"Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]

)
